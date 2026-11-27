"""SEARCH SAFETY check: makes CANON's SEARCH SAFETY rule visible (owner brief,
Nov 27 2026). A WARNING, never a failure.

CANON WORKFLOW, SEARCH SAFETY: "No run removes more than a quarter of an
indexed page's visible copy, changes a title or H1, or takes a keyword phrase
off a page's headings unless the brief names that change and states the
ranking risk." The Oct 17 2026 homepage cut is why the rule exists; this is
the check that would have said so before it shipped.

It compares every built page in public/ with the same file on origin/main (the
live site) and prints a WARNING when:
  - the visible copy inside <main> shrank by more than a quarter (words, with
    tags, comments, <style> and <script> removed);
  - the <title> changed, or the H1 changed;
  - a phrase from CANON's KEYWORD OWNERSHIP table was on one of the page's
    headings (h1 to h6 inside <main>) on origin/main and is on none of them now.
Each warning names the page, the before and the after, and ends "name this
change and its ranking risk in the brief (CANON SEARCH SAFETY)".

    python3 tools/searchsafety.py                    # public/ against origin/main
    python3 tools/searchsafety.py --ref <git ref>    # public/ against another commit
    python3 tools/searchsafety.py --compare MAIN.html BUILD.html [--path /slug]
                                                     # two files (a replay)
    python3 tools/searchsafety.py --selftest         # the fixtures

build.py --check runs selftest() and check_site() and prints what they return
as notes and WARNING lines. Nothing here is ever added to build.py's problems
and this module exits 0 whatever it finds; only `--selftest`, where the tool
itself is under test, exits 1 when a fixture misbehaves.

What it does not do:
  - It does not fetch. It reads the origin/main this checkout already has and
    names the commit and its date in its note, so a stale ref is visible.
  - A page that is not on origin/main is new: one note for all of them.
  - No origin/main at all (a copy of the repo without git, a fresh clone of
    another branch): one note, nothing compared.
  - A page that is noindex on origin/main is not an indexed page and is not
    compared (the founders landing page).
  - A page that was on origin/main and is not built now has lost all of its
    copy: it is a warning too.

Fixtures (tools/fixtures/searchsafety/<case>/main.html and build.html): a case
named warn-<kind>-... must draw exactly one warning of that kind (copy, title,
h1, keyword) and a case named quiet-... must draw none. The copy cases carry
their word counts in their names (2000-to-1400) and the self-test counts them,
so a fixture cannot drift into proving nothing.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ownership  # noqa: E402  (the KEYWORD OWNERSHIP table and its matching)

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "searchsafety"
REF = "origin/main"
QUARTER = 0.25
ENDING = "name this change and its ranking risk in the brief (CANON SEARCH SAFETY)"


# ─── one rendered page ─────────────────────────────────────────────
def _text(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def read_page(doc):
    """What a search engine reads of one rendered page, or None when the file
    is not a rendered page (no <title> or no <main>)."""
    doc = re.sub(r"<!--.*?-->", "", doc, flags=re.S)     # a comment that says "<title>" is not the title
    title = re.search(r"<title>(.*?)</title>", doc, re.S)
    main = re.search(r"<main\b[^>]*>(.*?)</main>", doc, re.S)
    if not (title and main):
        return None
    body = re.sub(r"<(style|script)\b[^>]*>.*?</\1>", "", main.group(1), flags=re.S | re.I)
    return {
        "title": re.sub(r"\s+", " ", html.unescape(title.group(1))).strip(),
        "h1": [_text(h) for h in re.findall(r"<h1\b[^>]*>(.*?)</h1>", body, re.S | re.I)],
        "headings": [_text(h) for n in range(1, 7)
                     for h in re.findall(rf"<h{n}\b[^>]*>(.*?)</h{n}>", body, re.S | re.I)],
        "words": len(_text(body).split()),
        "noindex": bool(re.search(r'<meta\s+name="robots"\s+content="[^"]*noindex', doc, re.I)),
    }


def _keyword_headings(keywords, headings):
    """{keyword id: (label, the first heading that carries it)}."""
    out = {}
    for h in headings:
        for k, _g, _at in ownership.find(keywords, h):
            out.setdefault(k["id"], (k["label"], h))
    return out


def compare(path, before_doc, after_doc, keywords):
    """[(kind, warning)] for one page: before = origin/main, after = the build.
    kind is copy, title, h1 or keyword. Every warning ends with ENDING."""
    b, a = read_page(before_doc), read_page(after_doc)
    if b is None or a is None:
        return []
    out = []
    if b["words"] and a["words"] < b["words"] * (1 - QUARTER):
        gone = round(100 * (b["words"] - a["words"]) / b["words"])
        out.append(("copy", f"{path}: visible copy inside <main> went from {b['words']:,} to {a['words']:,} words "
                            f"({gone}% removed, more than a quarter); {ENDING}"))
    if b["title"] != a["title"]:
        out.append(("title", f"{path}: <title> changed from \"{b['title']}\" to \"{a['title']}\"; {ENDING}"))
    if b["h1"] != a["h1"]:
        show = lambda hs: " | ".join(f'"{h}"' for h in hs) or "(none)"
        out.append(("h1", f"{path}: H1 changed from {show(b['h1'])} to {show(a['h1'])}; {ENDING}"))
    was, now = _keyword_headings(keywords, b["headings"]), _keyword_headings(keywords, a["headings"])
    for kid in sorted(set(was) - set(now)):
        label, heading = was[kid]
        out.append(("keyword", f"{path}: keyword phrase {kid} '{label}' was on a heading on main (\"{heading}\") "
                               f"and is on no heading now ({len(a['headings'])} headings read); {ENDING}"))
    return out


# ─── origin/main ───────────────────────────────────────────────────
def _git(*args):
    try:
        r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    except OSError:
        return None
    return r.stdout if r.returncode == 0 else None


def load_ref(ref=REF):
    """(label, {path under public/: loader}) for a git ref, or None when the
    ref (or git itself) is not there."""
    info = _git("log", "-1", "--format=%h, %cs", ref, "--")
    listing = _git("ls-tree", "-r", "--name-only", ref, "--", "public")
    if info is None or listing is None or not listing.strip():
        return None
    files = {}
    for name in listing.splitlines():
        if name.endswith(".html"):
            files[name[len("public/"):]] = (lambda n=name: _git("show", f"{ref}:{n}"))
    return f"{ref} ({info.strip()})", files


def _url_path(rel):
    rel = rel[:-len(".html")]
    return "/" if rel == "index" else "/" + rel


def _is_page(rel):
    """The files ownership.built_pages() counts as pages: public/index.html,
    public/<slug>.html and public/blog/<slug>.html; never 404.html."""
    parts = rel.split("/")
    return rel != "404.html" and (len(parts) == 1 or (len(parts) == 2 and parts[0] == "blog"))


def check_site(public=ROOT / "public", ref=REF, canon=ROOT / "CANON.md", main=None):
    """(warnings, notes) for every built page against origin/main. `main` may be
    given as (label, {rel: loader}) in place of a git ref (the self-test does)."""
    public = Path(public)
    main = load_ref(ref) if main is None else main
    if not main:
        return [], [f"no {ref} in this checkout to compare against - SEARCH SAFETY not checked"]
    label, main_files = main
    notes = []
    try:
        keywords, _excl = ownership.load_table(canon)
    except ownership.TableError as err:
        keywords = []
        notes.append(f"KEYWORD OWNERSHIP table not read ({err}) - headings were not compared for keyword phrases")
    built = {f.relative_to(public).as_posix(): f for f in ownership.built_pages(public)}
    warnings, new, skipped, compared = [], [], 0, 0
    for rel, f in built.items():
        if rel not in main_files:
            new.append(_url_path(rel)); continue
        before = main_files[rel]()
        if before is None:
            new.append(_url_path(rel)); continue
        b = read_page(before)
        if b is None or b["noindex"]:
            skipped += 1; continue
        compared += 1
        warnings += [w for _kind, w in compare(_url_path(rel), before, f.read_text(encoding="utf-8"), keywords)]
    for rel in sorted(set(main_files) - set(built)):
        if not _is_page(rel):
            continue
        b = read_page(main_files[rel]() or "")
        if b is None or b["noindex"]:
            continue
        warnings.append(f"{_url_path(rel)}: on main with {b['words']:,} words of visible copy, title \"{b['title']}\", "
                        f"and not built now (0 words); {ENDING}")
    notes.append(f"{compared} built page(s) compared with {label}"
                 + (f"; {skipped} not compared (noindex on main)" if skipped else ""))
    if new:
        notes.append(f"{len(new)} new page(s), not on {ref}, nothing to compare: {', '.join(sorted(new))}")
    return warnings, notes


def report(public=ROOT / "public", ref=REF, canon=ROOT / "CANON.md", main=None):
    """(lines to print, exit code). The exit code is 0 whatever was found."""
    warnings, notes = check_site(public, ref, canon, main)
    lines = [f"  note     {n}" for n in notes] + [f"  WARNING  {w}" for w in warnings]
    lines.append("SEARCH SAFETY: " + (f"{len(warnings)} warning(s); nothing fails" if warnings else "no warnings"))
    return lines, 0


# ─── fixtures ──────────────────────────────────────────────────────
def selftest(canon=ROOT / "CANON.md", verbose=True):
    """Every warn-<kind>-* case draws exactly one warning of that kind, every
    quiet-* case none; the copy cases hold the word counts their names say; a
    new page and a missing origin/main are notes; a warning never moves the
    exit code. Returns (misbehaviours, number of cases)."""
    say = print if verbose else (lambda *a: None)
    bad = []
    try:
        keywords, _excl = ownership.load_table(canon)
    except ownership.TableError as err:
        return [f"KEYWORD OWNERSHIP table not read: {err}"], 0
    cases = sorted(d for d in FIXTURES.iterdir() if d.is_dir()) if FIXTURES.is_dir() else []
    if not cases:
        return [f"no fixtures in {FIXTURES}"], 0
    seen = set()
    for d in cases:
        expect, kind = d.name.split("-")[0], d.name.split("-")[1]
        try:
            before = (d / "main.html").read_text(encoding="utf-8")
            after = (d / "build.html").read_text(encoding="utf-8")
        except OSError as err:
            bad.append(f"{d.name}: {err}"); continue
        m = re.search(r"<!--\s*fixture-path:\s*(\S+)\s*-->", after)
        got = compare(m.group(1) if m else "/fixture", before, after, keywords)
        kinds = [k for k, _w in got]
        ok = (kinds == [kind]) if expect == "warn" else (expect == "quiet" and kinds == [])
        if not all(w.endswith(ENDING) for _k, w in got):
            ok = False; bad.append(f"{d.name}: a warning does not end with the SEARCH SAFETY sentence")
        counts = re.search(r"-(\d+)-to-(\d+)$", d.name)
        if counts:
            real = (read_page(before)["words"], read_page(after)["words"])
            if real != (int(counts.group(1)), int(counts.group(2))):
                ok = False; bad.append(f"{d.name}: the pages hold {real[0]} and {real[1]} words, not what the name says")
        if not ok:
            bad.append(f"{d.name}: expected {'one ' + kind + ' warning' if expect == 'warn' else 'no warning'}, got {kinds}")
        if expect == "warn":
            seen.add(kind)
        say(f"  FIXTURE  {d.name:42s} {'WARNS (' + ', '.join(kinds) + ')' if kinds else 'quiet'}{'' if ok else '   MISBEHAVED'}")
        for _k, w in got:
            say(f"             {w}")
    for kind in ("copy", "title", "h1", "keyword"):
        if kind not in seen:
            bad.append(f"no warn-{kind}-* fixture: the {kind} warning was never seen firing")
    # A warning is never a failure; a new page and a missing origin/main are notes.
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        loud = next((d for d in cases if d.name.startswith("warn-copy")), cases[0])
        (tmp / "index.html").write_text((loud / "build.html").read_text(encoding="utf-8"), encoding="utf-8")
        (tmp / "brand-new-page.html").write_text((loud / "build.html").read_text(encoding="utf-8"), encoding="utf-8")
        before = (loud / "main.html").read_text(encoding="utf-8")
        lines, code = report(tmp, canon=canon, main=("fixture main", {"index.html": lambda: before}))
        n_warn = sum(1 for l in lines if l.startswith("  WARNING "))
        new_note = any(l.startswith("  note ") and "1 new page(s)" in l and "/brand-new-page" in l for l in lines)
        say(f"  FIXTURE  a site with a cut homepage and a new page: {n_warn} WARNING line(s), "
            f"new page {'noted' if new_note else 'NOT noted'}, exit code {code}"
            f"{'' if (n_warn == 1 and new_note and code == 0) else '   MISBEHAVED'}")
        if n_warn != 1:
            bad.append(f"a site with one cut page drew {n_warn} warnings, expected 1 (a new page must not warn)")
        if not new_note:
            bad.append("a new page was not reported as a note")
        if code != 0:
            bad.append(f"a warning changed the exit code to {code}")
        lines, code = report(tmp, ref="refs/heads/no-such-branch-for-the-selftest", canon=canon)
        quiet = code == 0 and not any(l.startswith("  WARNING ") for l in lines) \
            and sum(1 for l in lines if l.startswith("  note ")) == 1
        say(f"  FIXTURE  no origin/main to compare against: {'one note, no warning' if quiet else 'MISBEHAVED'}")
        if not quiet:
            bad.append("a missing ref was not reported as exactly one note with exit code 0")
    return bad, len(cases)


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        bad, n = selftest()
        print(f"SELFTEST: {'PASSED' if not bad else str(len(bad)) + ' misbehaviour(s)'} ({n} fixture cases)")
        for b in bad:
            print("  ", b)
        sys.exit(1 if bad else 0)
    if "--compare" in args:
        i = args.index("--compare")
        before, after = (Path(p).read_text(encoding="utf-8") for p in args[i + 1:i + 3])
        path = args[args.index("--path") + 1] if "--path" in args else "/"
        try:
            keywords, _excl = ownership.load_table()
        except ownership.TableError as err:
            keywords = []; print(f"  note     KEYWORD OWNERSHIP table not read ({err})")
        got = compare(path, before, after, keywords)
        for _k, w in got:
            print(f"  WARNING  {w}")
        print("SEARCH SAFETY: " + (f"{len(got)} warning(s); nothing fails" if got else "no warnings"))
        sys.exit(0)
    ref = args[args.index("--ref") + 1] if "--ref" in args else REF
    lines, code = report(ref=ref)
    print("\n".join(lines))
    sys.exit(code)


if __name__ == "__main__":
    main()
