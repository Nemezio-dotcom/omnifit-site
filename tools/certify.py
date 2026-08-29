"""Certification per CANON.md. Reports exactly three categories:
(a) compliance strikes  (b) stale canon  (c) broken structure.
Nothing else is a finding. Em-dashes are NOT scanned (voice preference).
Every rule is expressed as a rule, never a line number, and negative-tested."""
import re, glob, json, hashlib, html, html.parser, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import faq

OUT_OF_SCOPE = ("the-30-minute-executive-reset", "footer",
                # not a page: a retired llms.txt body kept as an HTML artifact.
                # CANON's REPO STATE has never listed it and no run has certified
                # it. It carries the retired brand name, Pacific Beach, the old
                # hello@ address and the JJ4E LLC line, all reported in REPORT.md
                # rather than certified or corrected. If it is ever meant to be a
                # live page, delete this entry — that is the condition under
                # which excluding it is wrong.
                "llms-txt-page-retired")

# ─── structural facts the tooling has to know (CANON: STRUCTURAL EXCEPTIONS) ──
# Headers whose page is built from Squarespace blocks: there is no Code Block to
# retrieve, so no pages/<slug>.html will ever exist. Known orphans, not missing
# files, and NOT to be deleted.
KNOWN_ORPHAN_HEADERS = ("bodybuilding", "energy-protocol-waitlist-form")

# Pages that carry their JSON-LD in the page body and have NO header file at
# all. The header-mirror check must not report these as missing a header.
BODY_EMBEDDED_SCHEMA = ("case-studies", "home-3")

# The homepage ships as five separate Code Blocks, home-1 … home-5, not one
# page. pages/headers/home-header.html is the header for all five, so its FAQ
# mirror is checked against the five bodies concatenated in slug order.
HEADER_PAGES = {"home": ["home-1", "home-2", "home-3", "home-4", "home-5"]}

# LocalBusiness is DEFINED on the homepage and referenced by @id everywhere
# else. CANON (c) bans redefinition "in a page header" — the homepage header is
# the definition site, not a redefinition.
LOCALBUSINESS_DEFINER = ("home",)

# Node types that stand in for WebPage in a header's @graph.
WEBPAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage", "ItemPage")

# ─── named accepted exceptions (CANON: KNOWN DEFERRED ITEMS) ──────────────────
# An ACCEPTED EXCEPTION is an existing violation deliberately tolerated;
# certification must not flag it while listed. Each entry is (slug, rule kind,
# exact phrase). All three must match, and the phrase is matched against the
# flattened source, so an exemption can never swallow a different violation of
# the same shape elsewhere on the same page.
ACCEPTED = [
    ("hsa-fsa-personal-training", "result promised within a window",
     "FSA funds are typically use-it-or-lose-it within the plan year, so timing "
     "matters more than it does with an HSA"),
    ("hsa-fsa-personal-training", "uncertified specialty claim",
     "does not determine eligibility, issue Letters of Medical Necessity, "
     "diagnose conditions, or provide medical or tax advice"),
]

def _accepted(path, kind, flat, pos, span=400):
    """True if this hit is a listed accepted exception. Matched on the slug, the
    rule kind AND the exact phrase in the surrounding flattened text."""
    slug = re.sub(r'(-header)?\.html$', '', path.split('/')[-1])
    near = flat[max(0, pos - span):pos + span]
    return any(s == slug and k == kind and p in near for s, k, p in ACCEPTED)

# ─── (a) compliance shapes ─────────────────────────────────────────
OUTCOME = (r'stronger|leaner|energized|energised|more in control|lose|losing|lost|fat loss|'
           r'transformation|results?|pounds?|lbs|body fat|inches')
_UNIT = r'(?:day|week|month|year)s?'
# A timeframe bounds an outcome window only when it is numerically quantified
# ("4-6 months", "Weeks 5-8", "Month 3") or rate-framed ("per week", "/week").
# Bare duration nouns ("after years of inactivity") do not bound a window.
TIMEFRAME = (r'(?:\b\d[\d,]*\s*(?:[-–]|to)?\s*\d*\s*' + _UNIT + r'\b'
             r'|\b' + _UNIT + r'\s*\d+(?:\s*[-–]\s*\d+)?\b'
             r'|\b(?:per|a|each|every)\s+' + _UNIT + r'\b'
             r'|/\s*' + _UNIT + r'\b)')
NEGATED = r'\b(?:not|never|no|cannot|without|outside|beyond|instead of|rather than|refer)\b'
# A timeframe immediately preceded by a contrastive marker describes what the
# program is NOT ("unlike 6-week challenges"), so it bounds no promise. The
# marker must sit within 2 words of the timeframe, and every other timeframe in
# the window is still checked, so this cannot exempt a real claim beside it.
CONTRAST = r'\b(?:unlike|not|never|no|rather than|instead of|as opposed to)\b[\s,]*(?:\w+\s+){0,2}$'

def _flat(t):
    t = re.sub(r'<!--.*?-->', ' ', t, flags=re.S)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t)).strip()

def _flatmap(t):
    """_flat(t), plus a source offset for every surviving character, so a hit in
    the flattened text can be reported as file:line. Asserted equal to _flat()
    on every file each run — the two must never drift, or the line numbers would
    point somewhere the rule never looked."""
    buf, off, i, n = [], [], 0, len(t)
    while i < n:
        if t.startswith('<!--', i):                     # comment -> single space
            j = t.find('-->', i)
            buf.append(' '); off.append(i); i = n if j < 0 else j + 3
        elif t[i] == '<' and t.find('>', i) > i + 1:    # <[^>]+> -> single space
            j = t.find('>', i)
            buf.append(' '); off.append(i); i = j + 1
        else:
            buf.append(t[i]); off.append(i); i += 1
    out, oo, k = [], [], 0                              # collapse \s+ -> ' '
    while k < len(buf):
        if buf[k].isspace():
            out.append(' '); oo.append(off[k])
            while k < len(buf) and buf[k].isspace(): k += 1
        else:
            out.append(buf[k]); oo.append(off[k]); k += 1
    lo, hi = 0, len(out)                                # .strip()
    while lo < hi and out[lo] == ' ': lo += 1
    while hi > lo and out[hi - 1] == ' ': hi -= 1
    return ''.join(out[lo:hi]), oo[lo:hi]

def _line(src, off, pos):
    """1-indexed source line of flattened-text position `pos`."""
    if not off: return 0
    return src.count('\n', 0, off[min(pos, len(off) - 1)]) + 1

def _near(t, m, window):
    return ' '.join(t[:m.start()].split()[-window:] + t[m.end():].split()[:window])

def guarantee_near_outcome(text, window=30):
    t = _flat(text); out = []
    for m in re.finditer(r'guarantee[ds]?', t, re.I):
        o = re.search(OUTCOME, _near(t, m, window), re.I)
        if o: out.append(("outcome guarantee", f"'{m.group(0)}' near '{o.group(0)}'",
                          t[max(0, m.start()-100):m.end()+140].strip(), m.start()))
    return out

def lbs_near_timeframe(text, window=15):
    t = _flat(text); out = []
    for m in re.finditer(r'\d[\d,]*(?:\s*(?:–|-|&ndash;|to)\s*\d[\d,]*)?\s*(?:lbs?|pounds?)', t, re.I):
        w = _near(t, m, window)
        for tf in re.finditer(TIMEFRAME, w, re.I):
            if re.search(CONTRAST, w[:tf.start()], re.I): continue
            out.append(("lbs near timeframe", f"'{m.group(0).strip()}' near '{tf.group(0)}'",
                        t[max(0, m.start()-100):m.end()+140].strip(), m.start()))
            break
    return out

# Widened Aug 2026: the literal "free"+"consultation" rule missed
# "free 45-minute assessment", which certified clean. The banned shape is a
# free FIRST SESSION of any name, so every name the site uses is listed.
BOOKABLE = (r'consultation|consult\b|assessment|screen|screening|session|'
            r'diagnostic|call\b|intake')

def free_consultation(text, window=6):
    t = _flat(text); out = []
    for m in re.finditer(r'\bfree\b', t, re.I):
        # "feel free to ..." is an idiom, not an offer. Only exempt when "feel"
        # immediately precedes, so "Book a free session" still flags.
        if re.search(r'\bfeels?\s*$', t[:m.start()], re.I): continue
        # hyphenated compound adjective ("distraction-free space", "injury-free",
        # "pain-free") describes a quality, never a price. An actual offer is
        # written "free consultation", unhyphenated.
        if t[:m.start()].endswith('-'): continue
        b = re.search(BOOKABLE, _near(t, m, window), re.I)
        if b:
            out.append(("free-consultation framing", f"'free' near '{b.group(0)}'",
                        t[max(0, m.start()-100):m.end()+140].strip(), m.start()))
    return out

def prenatal_postpartum(text, window=10):
    # attribution markup: a partner's own modality list, not an OmniFit claim
    attributed = set()
    for m in re.finditer(r'itemprop="knowsAbout"[^>]*>([^<]*)<|"knowsAbout"\s*:\s*\[([^\]]*)\]', text, re.I):
        attributed.update(w.lower() for w in re.findall(r'[A-Za-z-]+', (m.group(1) or '') + (m.group(2) or '')))
    t = _flat(text); out = []
    for m in re.finditer(r'\b(?:pre-?natal|post-?partum)\b', t, re.I):
        # legal only as an explicit out-of-scope disclaimer, or attributed to a partner
        if re.search(NEGATED, _near(t, m, window), re.I): continue
        if m.group(0).lower().replace('-','') in {a.replace('-','') for a in attributed}: continue
        out.append(("prenatal/postpartum content", m.group(0),
                    t[max(0, m.start()-100):m.end()+140].strip(), m.start()))
    return out

def uncertified_claims(text, window=8):
    t = _flat(text); out = []
    pat = (r'\b(?:we|omnifit(?: performance)?|i)\s+(?:\w+\s+){0,2}?'
           r'(diagnose|diagnoses|treat|treats|prescribe|prescribes|cure|cures|'
           r'rehabilitate|rehabilitates)\b')
    for m in re.finditer(pat, t, re.I):
        # negation may sit inside the match ("OmniFit does not diagnose") or beside it
        if re.search(NEGATED, m.group(0) + ' ' + _near(t, m, 4), re.I): continue
        out.append(("uncertified specialty claim", m.group(0).strip(),
                    t[max(0, m.start()-100):m.end()+140].strip(), m.start()))
    for m in re.finditer(r'\b(?:we|omnifit(?: performance)?)\s+(?:\w+\s+){0,2}?'
                         r'(?:provide|provides|offer|offers|deliver|delivers|perform|performs|do|does)\s+'
                         r'(?:\w+\s+){0,2}?(physical therapy|chiropractic)\b', t, re.I):
        if re.search(NEGATED, m.group(0) + ' ' + _near(t, m, 6), re.I): continue
        out.append(("uncertified specialty claim", m.group(0).strip(),
                    t[max(0, m.start()-100):m.end()+140].strip(), m.start()))
    return out

# negation incl. contractions, checked only on the PRECEDING words so a trailing
# "...and we don't cut corners" cannot exempt a real promise
NEG_WIDE = (r"\b(?:not|never|no|cannot|without|n't|don'?t|doesn'?t|didn'?t|won'?t|"
            r"isn'?t|aren'?t|haven'?t|hasn'?t)\b")

CLINICAL = (r'(?:pain|injur\w*|recover\w*|heal\w*|rehab\w*|symptom\w*|inflammation|'
            r'range of motion)')
OUTCOME_FRAME = (r'(?:reduc\w*|decreas\w*|improv\w*|resolv\w*|eliminat\w*|relief|relieved|'
                 r'free of|free from|better|gain\w*|less|fewer)')

def clinical_stat(text, window=8):
    """A percentage attached to a clinical RESULT. Behavioural and business stats
    (adherence, compliance, rating, reviews) are not clinical and stay. Process
    statements ('100% of clients get an injury screen') lack an outcome frame."""
    t = _flat(text); out = []
    for m in re.finditer(r'\d[\d.,]*\s*%', t):
        near = _near(t, m, window)
        c = re.search(CLINICAL, near, re.I)
        f = re.search(OUTCOME_FRAME, near, re.I)
        if c and f:
            out.append(("quantified clinical outcome statistic", f"'{m.group(0).strip()}' near '{c.group(0)}'",
                        t[max(0, m.start()-100):m.end()+140].strip(), m.start()))
    return out

RESULT = (r'(?:measurable|visible|noticeable|significant|dramatic)\s+\w*\s*'
          r'(?:increase|improvement|change|gain|loss|reduction|progress|result)\w*'
          r'|(?:see|seeing|achiev\w+|produc\w+|deliver\w+)\s+(?:\w+\s+){0,3}?'
          r'(?:result|results|change|changes|improvement|improvements|transformation)')

def result_near_timeframe(text, window=12):
    """A result paired with a promised window, in any units. The lbs rule is the
    specific case; results must be framed against the client's own baseline."""
    t = _flat(text); out = []
    for m in re.finditer(RESULT, t, re.I):
        # a result stated as absent ("produces no change", "don't have ... producing
        # visible results") promises nothing
        before = ' '.join(t[:m.start()].split()[-8:])
        if re.search(NEG_WIDE, m.group(0) + ' ' + before, re.I): continue
        w = _near(t, m, window)
        for tf in re.finditer(TIMEFRAME, w, re.I):
            if re.search(CONTRAST, w[:tf.start()], re.I): continue
            out.append(("result promised within a window", f"'{m.group(0).strip()}' near '{tf.group(0).strip()}'",
                        t[max(0, m.start()-100):m.end()+140].strip(), m.start()))
            break
    return out

COMPLIANCE = [guarantee_near_outcome, lbs_near_timeframe, free_consultation,
              prenatal_postpartum, uncertified_claims, clinical_stat,
              result_near_timeframe]

# ─── (b) stale canon ───────────────────────────────────────────────
BANNED = ["OmniFit Personal Fitness Training", "Pacific Beach", "ACE OES", "Orthopedic Exercise",
          "Executive Hybrid", "Lopez Perez", "180+", "$90 ", "$225", "$275", "$299",
          "$500/mo", "$599"]
CANON_MARKERS = ("Session packs run", "async programming tier", "Session packs:",
                 "$175 per session for 5", "Paid upfront", "Executive Reset from $175/mo", "Bronze",
                 "virtual from $175")
CANON_CARDS = ("5 Sessions", "10 Sessions", "20 Sessions", "Bronze")

def _marker_nearby(L, i, window=2):
    """A marker on the line itself, or in the `window` lines immediately before
    it — covers a title/price split across adjacent lines (e.g. a Bronze card's
    <h3> title one line above its <div class="...-price">), without the
    same-line requirement missing legitimate multi-line card layouts."""
    lo = max(0, i - 1 - window)
    return any(k in ln for ln in L[lo:i] for k in CANON_MARKERS)

def _inside_packs_table(L, i):
    """True if line i (1-indexed) sits inside <table class="...packs...">...</table>.
    Scans backward from the line before i; a </table> reached before any <table>
    means we are not inside one. Used ONLY to exempt $175 (in-home pack rungs);
    $150 is retired as a pack rung and gets no exemption from this helper."""
    for j in range(i - 2, -1, -1):
        if '</table>' in L[j]:
            return False
        m = re.search(r'<table[^>]*class="([^"]*)"', L[j])
        if m:
            return 'pack' in m.group(1).lower()
    return False

# ─── (c) structure ─────────────────────────────────────────────────
class _P(html.parser.HTMLParser):
    VOID = {'br','img','hr','meta','link','input','source','wbr','area','col','embed','param','track','path','svg'}
    def __init__(s): super().__init__(); s.st=[]; s.err=[]
    def handle_startendtag(s,t,a): pass
    def handle_starttag(s,t,a):
        if t not in s.VOID: s.st.append(t)
    def handle_endtag(s,t):
        if t in s.VOID: return
        if not s.st: s.err.append(f'stray </{t}>'); return
        if s.st[-1]==t: s.st.pop()
        else: s.err.append(f'mismatch {s.st[-1]}/{t}')

def page_questions(s):
    """Delegates to faq.py so certification and header generation can never
    disagree about what a page's FAQ is."""
    return faq.questions(s)

def _norm(x):
    """Stripping <a> tags leaves a space before punctuation; that is a rendering
    artifact of extraction, not a mirroring failure."""
    return re.sub(r'\s+([.,;:])', r'\1', re.sub(r'\s+', ' ', x or '')).strip()

def ld_nodes(s):
    """Every JSON-LD node in a file, from EVERY <script> block, whether the block
    is an @graph or a bare object. The single-block, @graph-only reader this
    replaces crashed with KeyError on the first hand-built header it met
    (about-header: an @graph with AboutPage and no WebPage) and would silently
    have missed desk-worker's FAQPage, which lives in a second block. Returns
    (nodes, errors)."""
    nodes, errs = [], []
    blocks = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', s, re.S)
    if not blocks:
        return nodes, ["no ld+json block"]
    for i, b in enumerate(blocks):
        try:
            doc = json.loads(b)
        except Exception as e:
            errs.append(f"invalid JSON in block {i + 1}: {e}"); continue
        nodes.extend(doc["@graph"] if isinstance(doc, dict) and "@graph" in doc
                     else doc if isinstance(doc, list) else [doc])
    return nodes, errs

def faq_pairs(nodes):
    """(question, answer) pairs from every FAQPage node, in document order."""
    return [(q.get("name"), (q.get("acceptedAnswer") or {}).get("text"))
            for n in nodes if n.get("@type") == "FAQPage"
            for q in n.get("mainEntity", [])]

def run():
    ALL = sorted(glob.glob('pages/**/*.html', recursive=True))
    files = [f for f in ALL if not any(k in f for k in OUT_OF_SCOPE)]
    skipped = [f for f in ALL if f not in files]
    assert files, "GLOB MATCHED ZERO FILES - run from repo root"
    A=B=C=0
    print(f"### SCOPE: {len(files)} certified, {len(skipped)} not yet certified")
    for k in skipped: print(f"   not certified: {k}")

    print("\n### (a) COMPLIANCE STRIKES")
    excused = []
    for f in files:
        t = open(f).read()
        flat, off = _flatmap(t)
        assert flat == _flat(t), f"flatten drift in {f}"
        for fn in COMPLIANCE:
            for kind, what, ctx, pos in fn(t):
                ln = _line(t, off, pos)
                if _accepted(f, kind, flat, pos):
                    excused.append(f"   {f}:{ln}  [{kind}] {what}  (accepted exception)")
                    continue
                print(f"   {f}:{ln}\n      [{kind}] {what}\n      …{ctx[:130]}…"); A+=1
    print("   none" if not A else f"   {A} strike(s)")
    if excused:
        print(f"   ({len(excused)} accepted exception(s) not counted, listed below)")
        for e in excused: print(e)

    print("\n### (b) STALE CANON")
    for term in BANNED:
        for f in files:
            for i,l in enumerate(open(f),1):
                if term.lower() in l.lower():
                    print(f"   {f}:{i}  [{term}]"); B+=1
    for f in files:
        L=open(f).readlines()
        for i,l in enumerate(L,1):
            # a travel FEE, not any dollar figure sharing a line with the word travel
            if re.search(r'travel[^.<]{0,30}\$(?:50|75)\b|\$(?:50|75)\b[^.<]{0,30}travel', l, re.I):
                print(f"   {f}:{i}  [travel fee dollar figure]"); B+=1
            for tok in ("$150","$175"):
                if tok in l:
                    # competitor pricing on the comparison page is not OmniFit pricing
                    ok = '<div class="comp-value">' in l
                    # $175 is a legal in-home pack rung and Reset Bronze tier; $150 is
                    # retired from BOTH ladders and gets no further exemption below
                    if tok == "$175":
                        ok = ok or _marker_nearby(L, i)
                        if not ok:
                            nm = re.findall(r'<div class="pc-name">([^<]*)</div>', "".join(L[max(0,i-12):i]))
                            ok = bool(nm) and nm[-1].strip() in CANON_CARDS
                        ok = ok or _inside_packs_table(L, i)
                    if not ok:
                        print(f"   {f}:{i}  [{tok} outside canonical context]  …{l.strip()[:90]}…"); B+=1
    print("   none" if not B else f"   {B} hit(s)")

    print("\n### (c) BROKEN STRUCTURE")
    inv={}
    for f in files:
        s=open(f).read()
        p=_P(); p.feed(s)
        if p.st or p.err:
            print(f"   {f}  [tag balance] unclosed={p.st} errors={p.err[:3]}"); C+=1
        if '/headers/' in f:
            slug=re.sub(r'-header\.html$','',f.split('/')[-1])
            nodes,errs=ld_nodes(s)
            for e in errs: print(f"   {f}  [{e}]"); C+=1
            if not nodes: continue
            types={x.get("@type") for x in nodes}
            # the homepage header is where LocalBusiness is DEFINED; CANON (c)
            # bans REdefinition in a page header, not the definition itself
            if "LocalBusiness" in types and slug not in LOCALBUSINESS_DEFINER:
                print(f"   {f}  [LocalBusiness redefined]"); C+=1
            wp=next((x for x in nodes if x.get("@type") in WEBPAGE_TYPES), None)
            # only a header that carries a WebPage-shaped node makes a claim about
            # `about`; one that carries only a Service or FAQPage makes none, and
            # inventing a finding there would be a new rule, not this one
            if wp is not None:
                ref=((wp.get("about") or {}).get("@id") or "")
                if not ref.endswith("#localbusiness-of"):
                    print(f"   {f}  [about not referencing homepage LocalBusiness] {ref or 'absent'}"); C+=1
            # KNOWN ORPHAN: the page is built from Squarespace blocks, so there is
            # no Code Block to retrieve and pages/<slug>.html will never exist.
            # Not a missing file, and not to be deleted.
            if slug in KNOWN_ORPHAN_HEADERS:
                print(f"   (known orphan header, no page to mirror: {f})")
                continue
            pgs=[f"pages/{p}.html" for p in HEADER_PAGES.get(slug,[slug])]
            missing=[p for p in pgs if not os.path.exists(p)]
            if missing: print(f"   {f}  [no matching page {', '.join(missing)}]"); C+=1; continue
            body="".join(open(p).read() for p in pgs)
            pq=page_questions(body)
            sq=[q for q,_ in faq_pairs(nodes)]
            if pq!=sq:
                print(f"   {f}  [FAQPage questions do not mirror page] page={len(pq)} schema={len(sq)}"); C+=1
            # CANON (c) requires count, order AND text: answers are part of the mirror.
            pa=[a for _,a in faq.qa(body)]
            sa=[a for _,a in faq_pairs(nodes)]
            if len(pa)!=len(sa) or any(_norm(a)!=_norm(b) for a,b in zip(pa,sa)):
                d=[i for i,(a,b) in enumerate(zip(pa,sa)) if _norm(a)!=_norm(b)]
                print(f"   {f}  [FAQPage answers do not mirror page] differing index={d}"); C+=1
            a=[x for _,x in faq_pairs(nodes)
               if (x or "").startswith("OmniFit Performance publishes its rates in full.")]
            if a: inv.setdefault("header pricing",set()).add(hashlib.sha256(a[0].encode()).hexdigest()[:16])
            continue
        # a page must have a header, unless it carries its schema in the body and
        # has none by design, or a shared header already covers it
        pslug=re.sub(r'\.html$','',f.split('/')[-1])
        if (pslug not in BODY_EMBEDDED_SCHEMA
                and not any(pslug in v for v in HEADER_PAGES.values())
                and not os.path.exists(f"pages/headers/{pslug}-header.html")):
            print(f"   {f}  [no header file pages/headers/{pslug}-header.html]"); C+=1
        for key,rx,grp in [
            ("page pricing", r'-faq-(?:body"><p>|a">)(OmniFit Performance publishes its rates in full\..*?)(?:</p>|</div>)', 1),
            ("credentials",  r'MEET YOUR TRAINER.*?<article class="[a-z]+-card">\s*<p>(.*?)</p>', 1)]:
            m=re.search(rx,s,re.S)
            if m: inv.setdefault(key,set()).add(hashlib.sha256(m.group(grp).encode()).hexdigest()[:16])
        arch=re.findall(r'<article class="[a-z]+-card">\s*<h3>(?:The Desk-Bound Executive|The Post-Rehab Professional|The 50\+ Professional)</h3>\s*<p>(.*?)</p>',s,re.S)
        if arch: inv.setdefault("archetypes",set()).add(hashlib.sha256("".join(arch).encode()).hexdigest()[:16])
        sm=re.search(r'THE 9-POINT MOVEMENT SCREEN.*?<p>(.*?)</p>.*?<ul class="[a-z]+-card-features">(.*?)</ul>\s*<p>(.*?)</p>',s,re.S)
        if sm: inv.setdefault("9-point",set()).add(hashlib.sha256((sm.group(1)+"".join(re.findall(r'<li>(.*?)</li>',sm.group(2)))+sm.group(3)).encode()).hexdigest()[:16])
    for k,v in inv.items():
        if len(v)!=1: print(f"   [invariant mismatch] {k}: {v}"); C+=1
    print("   none" if not C else f"   {C} problem(s)")

    # Printed every run, not only on mismatch: a run has to be able to quote the
    # five hashes back, and a silent invariant is how a check reports success
    # without looking.
    print("\n### INVARIANT HASHES")
    for k in ("page pricing","header pricing","credentials","archetypes","9-point"):
        v=inv.get(k)
        print(f"   {k:<16} {'  '.join(sorted(v)) if v else 'NOT COMPUTED - no file matched'}"
              f"{'' if v and len(v)==1 else '   <-- MISMATCH' if v else ''}")
    print(f"\n### RESULT: {'PASSED' if not (A or B or C) else 'FAILED'}"
          f"  (compliance {A} · stale canon {B} · structure {C})")
    return A,B,C

if __name__ == "__main__":
    run()
