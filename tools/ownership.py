"""Keyword ownership check. Reads the KEYWORD OWNERSHIP table in CANON.md and
fails when an owned phrase appears in the title, H1, H2s or meta description
of any page other than its owner (or a page the table also permits).

    python3 tools/ownership.py              # check public/ (run build.py first)
    python3 tools/ownership.py --selftest   # run the pass/fail fixtures

build.py --check calls check_site() and selftest(), so a check run that cannot
prove its own fixtures still fail is not a passing run.

Why here and not in certify.py: CANON's certification reports exactly three
categories (compliance, stale canon, structure). Keyword ownership is none of
them, and a page's title and meta description are only resolved at build time
(header WebPage node, SEO comment or build.py META_FALLBACK), so the check
reads the RENDERED page in public/, which is what a search engine reads.

Matching rules, recorded in CANON beside the table:
  - Case-insensitive, on tag-stripped text, comments/<style>/<script> removed.
  - Longest match wins: a match lying wholly inside another keyword's match is
    that other keyword's, so "In-Home Personal Trainer in San Diego" counts
    for the in-home keyword only, never for "personal trainer in san diego".
  - Fails closed: the CANON table missing, empty, malformed, or naming an
    owner page that was not built is a problem, never a skipped check.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "ownership"
OWNER_SURFACES = ("title", "meta", "h1", "h2")


class TableError(Exception):
    """The CANON ownership table could not be read. Raised, never defaulted:
    an empty table would make every page pass vacuously."""


# ─── CANON table ───────────────────────────────────────────────────
ENTRY_RE = re.compile(r"^  ([KX]\d+)\s+(.+?)\s*$")
FIELD_RE = re.compile(r"^      (owner|match|also|page|in)\s+(.+?)\s*$")


def read_table(text):
    """Returns (keywords, exclusions). Each keyword: dict(id, label, owner,
    also, rx). Each exclusion: dict(id, label, page, surfaces, rx)."""
    m = re.search(r"^  OWNERSHIP TABLE\b.*?$(.*?)^  END OWNERSHIP TABLE\s*$", text, re.S | re.M)
    if not m:
        raise TableError("no OWNERSHIP TABLE ... END OWNERSHIP TABLE block in CANON.md")
    entries, cur = [], None
    for line in m.group(1).splitlines():
        e, f = ENTRY_RE.match(line), FIELD_RE.match(line)
        if f and cur is not None:
            if f.group(1) in cur:
                raise TableError(f"{cur['id']}: field '{f.group(1)}' given twice")
            cur[f.group(1)] = f.group(2)
        elif e and not line.startswith("      "):
            cur = {"id": e.group(1), "label": e.group(2)}
            entries.append(cur)
    keywords, exclusions = [], []
    for x in entries:
        if "match" not in x:
            raise TableError(f"{x['id']}: no 'match' line")
        try:
            x["rx"] = re.compile(x["match"], re.I)
        except re.error as err:
            raise TableError(f"{x['id']}: match is not a valid regex: {err}")
        if x["id"].startswith("K"):
            if "owner" not in x:
                raise TableError(f"{x['id']}: no 'owner' line")
            x["also"] = x.get("also", "").split() if x.get("also", "-") != "-" else []
            keywords.append(x)
        else:
            if "page" not in x:
                raise TableError(f"{x['id']}: no 'page' line")
            x["surfaces"] = tuple(x.get("in", "title meta h1 h2").split())
            exclusions.append(x)
    if not keywords:
        raise TableError("OWNERSHIP TABLE parsed but holds no keyword entries")
    return keywords, exclusions


def load_table(path=ROOT / "CANON.md"):
    try:
        return read_table(Path(path).read_text(encoding="utf-8"))
    except OSError as err:
        raise TableError(f"cannot read {path}: {err}")


# ─── rendered-page surfaces ────────────────────────────────────────
def _text(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def _strings(node, out):
    """Every human-readable string in a JSON-LD node (ids and URLs skipped)."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ("@id", "@type", "@context", "url", "item", "sameAs", "image", "logo"):
                continue
            _strings(v, out)
    elif isinstance(node, list):
        for v in node:
            _strings(v, out)
    elif isinstance(node, str) and not node.startswith("http"):
        out.append(node)


def surfaces(doc):
    """{surface: [text, ...]} for one rendered page."""
    title = re.search(r"<title>(.*?)</title>", doc, re.S)
    meta = re.search(r'<meta name="description" content="(.*?)">', doc, re.S)
    main = re.search(r'<main id="main">(.*?)</main>', doc, re.S)
    if not (title and meta and main):
        raise ValueError("not a rendered page: <title>, meta description or <main> missing")
    body = re.sub(r"<!--.*?-->", "", main.group(1), flags=re.S)
    body = re.sub(r"<(style|script)\b[^>]*>.*?</\1>", "", body, flags=re.S | re.I)
    out = {"title": [html.unescape(title.group(1)).strip()],
           "meta": [html.unescape(meta.group(1)).strip()]}
    for n in range(1, 7):
        out[f"h{n}"] = [_text(h) for h in re.findall(rf"<h{n}\b[^>]*>(.*?)</h{n}>", body, re.S | re.I)]
    out["faq"] = [_text(q) for q in re.findall(r"<summary\b(?![^>]*\bsection-toggle\b)[^>]*>(.*?)</summary>", body, re.S | re.I)]
    # The page's own header injection, not the site-wide entity graph.
    hdr = re.search(r"Page header injection \(source:.*?-->(.*?)<!-- =+ End page header injection", doc, re.S)
    strings = []
    for block in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', hdr.group(1) if hdr else "", re.S):
        _strings(json.loads(block), strings)
    out["jsonld"] = strings
    # Body copy for reporting only: <main> text with the H1/H2 text taken out.
    rest = re.sub(r"<h[12]\b[^>]*>.*?</h[12]>", " ", body, flags=re.S | re.I)
    out["body"] = [_text(rest)]
    return out


# ─── matching ──────────────────────────────────────────────────────
def find(keywords, text):
    """[(keyword, matched text)] with longest-match attribution: a match lying
    wholly inside another keyword's match belongs to that keyword."""
    hits = []
    for k in keywords:
        for m in k["rx"].finditer(text):
            if m.end() > m.start():
                hits.append((m.start(), m.end(), k, m.group(0)))
    keep = []
    for s, e, k, g in hits:
        if any(s2 <= s and e <= e2 and (s2, e2) != (s, e) and k2 is not k for s2, e2, k2, _ in hits):
            continue
        keep.append((k, g, s))
    return keep


def _ctx(text, start, length):
    lo, hi = max(0, start - 45), start + length + 45
    return ("…" if lo else "") + text[lo:hi] + ("…" if hi < len(text) else "")


def count(keywords, texts):
    """{keyword id: number of attributed matches} across a list of strings."""
    c = {}
    for t in texts:
        for k, _, _ in find(keywords, t):
            c[k["id"]] = c.get(k["id"], 0) + 1
    return c


def check_page(path, doc, keywords, exclusions):
    """(problems, owned) for one page. owned = keyword ids this page carries
    on an owner surface, used for the owner-coverage note."""
    surf = surfaces(doc)
    problems, owned = [], set()
    for name in OWNER_SURFACES:
        for text in surf[name]:
            for k, g, at in find(keywords, text):
                if k["owner"] == "-":
                    continue            # unassigned; reported once by check_site
                if path == k["owner"] or path in k["also"]:
                    owned.add(k["id"])
                    continue
                problems.append(f"{path}: {k['id']} '{k['label']}' in {name}: \"{g}\" "
                                f"(\"{_ctx(text, at, len(g))}\") - owner is {k['owner']}")
    for x in exclusions:
        if x["page"] != path:
            continue
        for name in x["surfaces"]:
            for text in surf.get(name, []):
                for m in x["rx"].finditer(text):
                    problems.append(f"{path}: {x['id']} '{x['label']}' - \"{m.group(0)}\" in {name} "
                                    f"(\"{_ctx(text, m.start(), len(m.group(0)))}\")")
    return problems, owned


def _url_path(public, f):
    rel = f.relative_to(public).parent.as_posix()
    return "/" if rel == "." else "/" + rel


def check_site(public=ROOT / "public", canon=ROOT / "CANON.md"):
    """(problems, notes) for every rendered page in public/."""
    try:
        keywords, exclusions = load_table(canon)
    except TableError as err:
        return [f"KEYWORD OWNERSHIP table not read - {err}; no page was checked"], []
    files = sorted(Path(public).rglob("index.html"))
    if not files:
        return [f"no rendered pages under {public} - ownership not checked"], []
    paths = {_url_path(public, f): f for f in files}
    problems, notes, owned = [], [], {}
    for k in keywords:
        for p in ([k["owner"]] if k["owner"] != "-" else []) + k["also"]:
            if p not in paths:
                problems.append(f"{k['id']} '{k['label']}': owner/permitted page {p} was not built")
        if k["owner"] == "-":
            notes.append(f"{k['id']} '{k['label']}' has no owner yet - exclusivity NOT enforced")
    for x in exclusions:
        if x["page"] not in paths:
            problems.append(f"{x['id']}: page {x['page']} was not built")
    for p, f in paths.items():
        pr, ow = check_page(p, f.read_text(encoding="utf-8"), keywords, exclusions)
        problems += pr
        for kid in ow:
            owned.setdefault(kid, set()).add(p)
    for k in keywords:
        if k["owner"] != "-" and k["owner"] not in owned.get(k["id"], set()):
            notes.append(f"{k['id']} '{k['label']}': owner {k['owner']} does not carry it in "
                         f"title/H1/H2/meta (exclusivity holds; coverage is a content call)")
    return problems, notes


# ─── fixtures ──────────────────────────────────────────────────────
BAD_TABLES = {
    "table missing": "INVARIANTS\n- nothing here\n",
    "table empty": "  OWNERSHIP TABLE\n  END OWNERSHIP TABLE\n",
    "entry without owner": "  OWNERSHIP TABLE\n  K01 x\n      match  x\n  END OWNERSHIP TABLE\n",
    "regex does not compile": "  OWNERSHIP TABLE\n  K01 x\n      owner  /\n      match  (x\n  END OWNERSHIP TABLE\n",
}


def selftest(canon=ROOT / "CANON.md", verbose=True):
    """Every fixture under fixtures/ownership/fail must produce a problem and
    every one under pass must produce none. Returns a list of failures."""
    say = print if verbose else (lambda *a: None)
    bad = []
    for name, text in BAD_TABLES.items():
        try:
            read_table(text)
            bad.append(f"bad CANON table '{name}' parsed without error")
            say(f"  FIXTURE  table/{name:38s} expected TableError, got none   MISBEHAVED")
        except TableError as err:
            say(f"  FIXTURE  table/{name:38s} TableError as expected: {err}")
    keywords, exclusions = load_table(canon)
    for kind in ("fail", "pass"):
        files = sorted((FIXTURES / kind).glob("*.html"))
        if not files:
            bad.append(f"no {kind} fixtures in {FIXTURES / kind}")
        for f in files:
            doc = f.read_text(encoding="utf-8")
            m = re.search(r"<!--\s*fixture-path:\s*(\S+)\s*-->", doc)
            if not m:
                bad.append(f"{f.name}: no fixture-path comment"); continue
            problems, _ = check_page(m.group(1), doc, keywords, exclusions)
            ok = bool(problems) == (kind == "fail")
            if not ok:
                bad.append(f"{kind}/{f.name}: {'no problem reported' if kind == 'fail' else problems}")
            say(f"  FIXTURE  {kind}/{f.name:38s} {'FAILS' if problems else 'passes'}"
                f"{'' if ok else '   MISBEHAVED'}")
            for p in problems:
                say(f"             {p}")
    return bad


def main():
    if "--selftest" in sys.argv[1:]:
        bad = selftest()
        print(f"SELFTEST: {'PASSED' if not bad else str(len(bad)) + ' fixture(s) misbehaved'}")
        for b in bad:
            print("  ", b)
        sys.exit(1 if bad else 0)
    problems, notes = check_site()
    for n in notes:
        print("  note    ", n)
    for p in problems:
        print("  PROBLEM ", p)
    print(f"OWNERSHIP: {'PASSED' if not problems else str(len(problems)) + ' problem(s)'}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
