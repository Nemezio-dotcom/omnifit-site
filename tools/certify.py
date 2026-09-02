"""Certification per CANON.md. Reports exactly three categories:
(a) compliance strikes  (b) stale canon  (c) broken structure.
Nothing else is a finding. Em-dashes are NOT scanned (voice preference).
Every rule is expressed as a rule, never a line number, and negative-tested."""
import re, glob, json, hashlib, html, html.parser, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import faq

OUT_OF_SCOPE = ("the-30-minute-executive-reset", "footer")

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

def _near(t, m, window):
    return ' '.join(t[:m.start()].split()[-window:] + t[m.end():].split()[:window])

def guarantee_near_outcome(text, window=30):
    t = _flat(text); out = []
    for m in re.finditer(r'guarantee[ds]?', t, re.I):
        o = re.search(OUTCOME, _near(t, m, window), re.I)
        if o: out.append(("outcome guarantee", f"'{m.group(0)}' near '{o.group(0)}'",
                          t[max(0, m.start()-100):m.end()+140].strip()))
    return out

# ─── DOCUMENTED CASE-STUDY EXCEPTION (Andrew Flores, Sept 2026) ────
# CANON's CANONICAL TRUTH records documented client figures WITH timeframes as
# canonical fact while the COMPLIANCE SCREEN banned lbs-near-timeframe outright.
# Resolution: an individual, attributed, documented client outcome with
# substantiation on file is a different object from a claim about what a
# PROSPECTIVE client can expect. The first is a fact about a named person; the
# second is a projection, and only the projection is what these two rules exist
# to prevent. Exempts lbs_near_timeframe and result_near_timeframe ONLY.
#
# Keyed off the disclaimer TEXT PRESENT ON THE PAGE, never off the filename:
# that is what makes condition 2 enforceable rather than decorative. The same
# figure on a page without the disclaimer is still a strike.
DISCLAIMER_VARIES = (r'\b(?:vary|varies|varied|depends?|depending|'
                     r'not a projection|not projections|not typical)\b')

# The disclaimer must be the POINT of its own block, not an aside inside another
# one. Tightened Sept 2026: the loose version accepted any occurrence anywhere on
# the page, so how-we-measure-your-progress qualified off a chart caption
# ("Sample layout only. The values shown are illustrative, and individual results
# vary..."). Two conditions, both structural:
#   · the containing element is a block that can hold a disclaimer on its own -
#     p / div / aside / section / blockquote. li, td, th, caption, figcaption and
#     small are excluded by not being on this list, which is what "not a caption,
#     list item, or table cell" means mechanically.
#   · the block's text STARTS with the phrase. A note that merely mentions
#     individual results partway through a sentence about something else is a
#     caption, whatever element it sits in.
DISCLAIMER_BLOCK = re.compile(
    r'<(p|div|aside|section|blockquote)\b[^>]*>\s*'
    r'(?:<(?:strong|em|b|i|span|small)\b[^>]*>\s*)?'      # a lead-in inline wrapper is fine
    r'individual results?\b', re.I)

def _has_results_disclaimer(text, window=40):
    """The individual-results disclaimer: a dedicated block whose text opens with
    'individual result(s)' and carries a statement that outcomes vary or depend on
    the individual. A bare mention of the words is not a disclaimer, and neither
    is one embedded in a caption, list item or table cell."""
    for m in DISCLAIMER_BLOCK.finditer(text):
        tag = m.group(1)
        end = text.lower().find(f'</{tag}>', m.end())
        block = _flat(text[m.start():end if end != -1 else m.end() + 800])
        if re.search(DISCLAIMER_VARIES, ' '.join(block.split()[:window]), re.I):
            return True
    return False

# Condition 1: attributed to a specific individual - a named client beside a
# role/profile, or an explicit anonymisation that still states a profile.
# A role/profile noun is required after the name. Without it, "San Diego, lost
# 27 pounds" would read as an attribution and condition 1 would be decorative.
ROLE = (r'(?:\d{1,2}-year-old|owner|founder|co-founder|CEO|CTO|CFO|COO|chief|'
        r'executive|director|manager|officer|board member|business owner|'
        r'nurse|RN|auditor|Marine|veteran|engineer|physician|therapist|attorney|'
        r'lawyer|teacher|realtor|entrepreneur|consultant|accountant|bookkeeper|'
        r'professional|client|mother|father|mom|dad|retiree|athlete|'
        r'(?:his|her|their) \d{2}s)')
NAMED_ATTRIB = (r'\b[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]+)?\s*(?:·|&middot;|&#183;)'   # "Mark ·", "Dave Rendo ·"
                r'|\b[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]+)?,\s+(?:an?|the)?\s*'
                r'(?:\w+[\s-]+){0,2}?' + ROLE + r'\b'                             # "Annie, a registered nurse"
                r'|\b[A-Z][a-z]{2,}\s+(?:is|was|runs|ran|came|started|joined)\s+an?\b')
PROFILE = r'\b(?:male|female|man|woman|\d{2}-year|\d{2}\s*,\s*\d|aged?)\b'
# Aggregate or typical-results framing is NEVER exempt, on any page.
AGGREGATE = (r'\b(?:typical|typically|average|averages|averaged|'
             r'most clients|our clients|every client|everyone|anyone|'
             r'clients\s+(?:lose|gain|drop|see|can|will)|'
             r'you\s+(?:\w+\s+){0,2}?(?:lose|gain|drop|expect|see|will|can)|'
             r"you'll|expect to|up to)\b")

def _case_study_exempt(t, m, page_disclaimed, window=45):
    """True when this match is a documented individual case-study figure on a
    page carrying the individual-results disclaimer. Fails CLOSED: anything the
    attribution test cannot confirm stays a strike."""
    if not page_disclaimed:                       # condition 2
        return False
    w = ' '.join(t[:m.start()].split()[-window:] + t[m.end():].split()[:window])
    if re.search(AGGREGATE, w, re.I):             # never exempt, on any page
        return False
    if re.search(r'\banonymi[sz]ed\b', w, re.I):  # condition 1, anonymised form
        return bool(re.search(PROFILE, w, re.I))  #   ... with a stated profile
    return bool(re.search(NAMED_ATTRIB, w))       # condition 1, named form

def lbs_near_timeframe(text, window=15):
    t = _flat(text); out = []
    disclaimed = _has_results_disclaimer(text)
    for m in re.finditer(r'\d[\d,]*(?:\s*(?:–|-|&ndash;|to)\s*\d[\d,]*)?\s*(?:lbs?|pounds?)', t, re.I):
        w = _near(t, m, window)
        for tf in re.finditer(TIMEFRAME, w, re.I):
            if re.search(CONTRAST, w[:tf.start()], re.I): continue
            if _case_study_exempt(t, m, disclaimed): break
            out.append(("lbs near timeframe", f"'{m.group(0).strip()}' near '{tf.group(0)}'",
                        t[max(0, m.start()-100):m.end()+140].strip()))
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
                        t[max(0, m.start()-100):m.end()+140].strip()))
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
                    t[max(0, m.start()-100):m.end()+140].strip()))
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
                    t[max(0, m.start()-100):m.end()+140].strip()))
    for m in re.finditer(r'\b(?:we|omnifit(?: performance)?)\s+(?:\w+\s+){0,2}?'
                         r'(?:provide|provides|offer|offers|deliver|delivers|perform|performs|do|does)\s+'
                         r'(?:\w+\s+){0,2}?(physical therapy|chiropractic)\b', t, re.I):
        if re.search(NEGATED, m.group(0) + ' ' + _near(t, m, 6), re.I): continue
        out.append(("uncertified specialty claim", m.group(0).strip(),
                    t[max(0, m.start()-100):m.end()+140].strip()))
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
                        t[max(0, m.start()-100):m.end()+140].strip()))
    return out

RESULT = (r'(?:measurable|visible|noticeable|significant|dramatic)\s+\w*\s*'
          r'(?:increase|improvement|change|gain|loss|reduction|progress|result)\w*'
          r'|(?:see|seeing|achiev\w+|produc\w+|deliver\w+)\s+(?:\w+\s+){0,3}?'
          r'(?:result|results|change|changes|improvement|improvements|transformation)')

def result_near_timeframe(text, window=12):
    """A result paired with a promised window, in any units. The lbs rule is the
    specific case; results must be framed against the client's own baseline."""
    t = _flat(text); out = []
    disclaimed = _has_results_disclaimer(text)
    for m in re.finditer(RESULT, t, re.I):
        # a result stated as absent ("produces no change", "don't have ... producing
        # visible results") promises nothing
        before = ' '.join(t[:m.start()].split()[-8:])
        if re.search(NEG_WIDE, m.group(0) + ' ' + before, re.I): continue
        w = _near(t, m, window)
        for tf in re.finditer(TIMEFRAME, w, re.I):
            if re.search(CONTRAST, w[:tf.start()], re.I): continue
            if _case_study_exempt(t, m, disclaimed): break
            out.append(("result promised within a window", f"'{m.group(0).strip()}' near '{tf.group(0).strip()}'",
                        t[max(0, m.start()-100):m.end()+140].strip()))
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

def run():
    # archive/ is retired content kept as a historical record - never globbed,
    # never certified, never corrected. See CANON REPO STATE.
    ALL = sorted(glob.glob('pages/**/*.html', recursive=True))
    assert not any(f.startswith('archive/') for f in ALL), "archive/ must never enter scope"
    files = [f for f in ALL if not any(k in f for k in OUT_OF_SCOPE)]
    skipped = [f for f in ALL if f not in files]
    assert files, "GLOB MATCHED ZERO FILES - run from repo root"
    # Where two in-scope files are BYTE-IDENTICAL, certify one and reference the
    # other: home-3.html is the case-studies block pasted into the homepage, and
    # certifying both double-counted every finding on it. The kept file is the
    # alphabetically first, so the choice is deterministic, and the pairing is
    # printed rather than silently applied.
    seen, dup = {}, {}
    for f in files:
        h = hashlib.sha256(open(f, 'rb').read()).hexdigest()
        if h in seen: dup[f] = (seen[h], h)
        else: seen[h] = f
    files = [f for f in files if f not in dup]
    A=B=C=0
    print(f"### SCOPE: {len(files)} certified, {len(skipped)} not yet certified, "
          f"{len(dup)} byte-identical duplicate(s)")
    for k in skipped: print(f"   not certified: {k}")
    for k, (src, h) in sorted(dup.items()):
        print(f"   duplicate: {k}  ==  {src}  (sha256 {h[:16]}…) - certified via source")

    print("\n### (a) COMPLIANCE STRIKES")
    for f in files:
        t = open(f).read()
        for fn in COMPLIANCE:
            for kind, what, ctx in fn(t):
                print(f"   {f}\n      [{kind}] {what}\n      …{ctx[:130]}…"); A+=1
    print("   none" if not A else f"   {A} strike(s)")

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
    inv={}; notrun=[]
    for f in files:
        s=open(f).read()
        p=_P(); p.feed(s)
        if p.st or p.err:
            print(f"   {f}  [tag balance] unclosed={p.st} errors={p.err[:3]}"); C+=1
        if '/headers/' in f:
            m=re.search(r'<script type="application/ld\+json">\s*(.*?)\s*</script>',s,re.S)
            if not m: print(f"   {f}  [no ld+json block]"); C+=1; continue
            try: doc=json.loads(m.group(1))
            except Exception as e: print(f"   {f}  [invalid JSON] {e}"); C+=1; continue
            # Not every header in the repo is a Batch-3-shaped @graph document
            # (the homepage header IS the LocalBusiness definition, and several
            # uploaded headers are a single bare node). A check that cannot be
            # applied is recorded as NOT RUN, never silently skipped: the shape
            # is outside what CANON specifies for page headers, so calling it a
            # violation would be inventing a rule, and calling it a pass is how
            # three earlier checks came to report success without looking.
            graph = doc["@graph"] if isinstance(doc, dict) and "@graph" in doc else [doc]
            n={x["@type"]:x for x in graph if isinstance(x, dict) and "@type" in x}
            if "@graph" not in doc:
                notrun.append(f"{f}  ld+json is a single bare node, not an @graph document"
                              f" - LocalBusiness/about checks not applicable")
            else:
                if "LocalBusiness" in n: print(f"   {f}  [LocalBusiness redefined]"); C+=1
                if "WebPage" not in n:
                    notrun.append(f"{f}  @graph has no WebPage node ({sorted(n)}) - "
                                  f"about-references-homepage-LocalBusiness check could not run")
                elif not n["WebPage"].get("about",{}).get("@id","").endswith("#localbusiness-of"):
                    print(f"   {f}  [about not referencing homepage LocalBusiness]"); C+=1
            slug=re.sub(r'-header\.html$','',f.split('/')[-1])
            pg=f"pages/{slug}.html"
            sq=[q["name"] for x in graph if x.get("@type")=="FAQPage" for q in x["mainEntity"]]
            sa=[q["acceptedAnswer"]["text"] for x in graph if x.get("@type")=="FAQPage"
                for q in x["mainEntity"]]
            try: pagesrc=open(pg).read()
            except FileNotFoundError: print(f"   {f}  [no matching page {pg}]"); C+=1; continue
            # An extractor that cannot read the page's FAQ has not verified the
            # mirror; it has declined to look. Never let that count as a pass.
            try: pairs=faq.qa(pagesrc)
            except faq.ExtractorFailure as e:
                notrun.append(f"{f}  FAQ mirror NOT VERIFIED - extractor failed on {pg}: {e}")
                continue
            pq=[q for q,_ in pairs]; pa=[a for _,a in pairs]
            if not pq and not sq:
                notrun.append(f"{f}  no FAQ found on either side (page 0, schema 0) - "
                              f"mirror check compared nothing")
            if pq!=sq:
                print(f"   {f}  [FAQPage questions do not mirror page] page={len(pq)} schema={len(sq)}"); C+=1
            # CANON (c) requires count, order AND text: answers are part of the mirror.
            if len(pa)!=len(sa) or any(_norm(a)!=_norm(b) for a,b in zip(pa,sa)):
                d=[i for i,(a,b) in enumerate(zip(pa,sa)) if _norm(a)!=_norm(b)]
                print(f"   {f}  [FAQPage answers do not mirror page] differing index={d}"); C+=1
            a=[x for x in sa if x.startswith("OmniFit Performance publishes its rates in full.")]
            if a: inv.setdefault("header pricing",set()).add(hashlib.sha256(a[0].encode()).hexdigest()[:16])
            continue
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

    print("\n### INVARIANT HASHES (CANON.md records these; five expected)")
    for k in ("page pricing","header pricing","credentials","archetypes","9-point"):
        v=inv.get(k)
        print(f"   {k:16} {'MISSING - not found on any file' if not v else ' '.join(sorted(v))}")
        if not v: notrun.append(f"invariant '{k}' matched no file - hash not verified")

    # NOT a fourth certification category: these are checks that could not be
    # applied, reported so a green result can never mean "nothing was looked at".
    print("\n### CHECKS THAT COULD NOT RUN")
    for x in notrun: print(f"   {x}")
    print("   none" if not notrun else f"   {len(notrun)} check(s) not verified")

    result = "FAILED" if (A or B or C) else ("INCOMPLETE" if notrun else "PASSED")
    print(f"\n### RESULT: {result}"
          f"  (compliance {A} · stale canon {B} · structure {C} · not-run {len(notrun)})")
    return A,B,C

if __name__ == "__main__":
    run()
