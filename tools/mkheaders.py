"""Generate Batch 3 page headers. FAQPage mirrors the on-page FAQ verbatim, in
page order. LocalBusiness is referenced by @id from the homepage, never redefined."""
import sys, json, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import faq

BASE = "https://www.omnifittraining.com"
META = {
 "the-omnifit-method": ("The OmniFit Method: Assess, Correct, Build, Sustain | OmniFit Performance", "Personal Training Method",
   "OmniFit Performance's four-phase training method for busy professionals 30+ in San Diego: Assess, Correct, Build, Sustain. Corrective-first programming with a 3/10 pain ceiling, led by a NASM Elite Trainer."),
 "how-we-measure-your-progress": ("How We Measure Your Progress | OmniFit Performance San Diego", "How We Measure Progress",
   "How OmniFit Performance tracks client progress in San Diego: standardized metrics, progress reviews every 4 weeks, and program adjustments driven by trend data rather than guesswork."),
 "omnifit-vs-competitors": ("OmniFit vs F45, Orangetheory, Big Box Gyms & Equinox | San Diego Personal Training Comparison", "OmniFit vs Other Options",
   "Honest comparison: OmniFit Performance vs F45, Orangetheory, 24 Hour Fitness, and Equinox. Find the right fit for busy professionals 30+ in San Diego."),
 "weight-loss": ("Sustainable Fat Loss for Busy Professionals 30+ | OmniFit Performance San Diego", "Fat Loss Coaching",
   "Structured fat loss coaching in 4S Ranch, San Diego for busy professionals over 30. Joint-friendly strength training, individualized nutrition coaching, and behavior change systems instead of crash diets."),
 "strength-training-1": ("Strength Training for Professionals 30+ | OmniFit Performance San Diego", "Strength Training",
   "Progressive, joint-friendly strength training in San Diego for professionals 30+. Corrective-first programming that builds real strength while protecting joints, led by a NASM Elite Trainer."),
 "hiit-personal-trainer-san-diego": ("HIIT Personal Training in San Diego | OmniFit Performance", "HIIT Personal Training",
   "Coached 1-on-1 HIIT and conditioning in San Diego, at the studio inside Teqneeq FHC in 4S Ranch, in-home across North County, or live virtual. Time-efficient sessions for busy professionals 30+."),
 "personal-training-services": ("Personal Training Services for Professionals 30+ | OmniFit Performance San Diego", "Personal Training Services",
   "OmniFit Performance's personal training services in San Diego: private studio sessions at Teqneeq FHC in 4S Ranch, in-home training across North County, and virtual coaching for professionals 30+."),
 "body-composition-testing": ("Body Composition Testing in San Diego | Bodystat QuadScan 4000 | OmniFit Performance", "Body Composition Testing",
   "Multi-frequency Bodystat QuadScan 4000 body composition testing in San Diego at Teqneeq FHC in 4S Ranch. The $150 Performance Assessment includes a 9-point movement screen and expert interpretation."),
 "partners": ("Trusted Clinical Partners | OmniFit Performance — San Diego", "Clinical Partners",
   "OmniFit Performance partners with board-certified physical therapists and licensed massage therapists in San Diego to bridge rehabilitation, recovery, and corrective strength training for busy professionals 30+."),
}
# Real partner entities carried over from the page's embedded schema. Kept because
# they are partner facts that exist nowhere else; OmniFit's own business node is
# NOT carried over, since CANON forbids redefining LocalBusiness in a page header.
KEEP_ENTITIES = {"partners": ["Person"]}
CLOSE_PUNCT = {"weight-loss", "omnifit-vs-competitors"}
# Header comments rewritten after Batch 3. The default note below is the
# August 2026 text; a slug listed here gets its later note instead.
NOTE = {
 "how-we-measure-your-progress":
   "<!-- HOW-WE-MEASURE-YOUR-PROGRESS PAGE HEADER JSON-LD · OCT 2 2026\n"
   "  Paste into /how-we-measure-your-progress → Page Settings → Advanced → Page Header Code Injection,\n"
   "  replacing any previous block entirely.\n"
   "  FAQPage mirrors the on-page FAQ verbatim (tags stripped), in page order.\n"
   "  LocalBusiness is referenced by @id from the site-wide header, never redefined here.\n",
}

def build(slug, check=False):
    page = open(f'pages/{slug}.html').read()
    title, crumb, desc = META[slug]
    graph = [
      {"@type": "WebPage", "@id": f"{BASE}/{slug}#webpage", "url": f"{BASE}/{slug}",
       "name": title, "description": desc,
       "about": {"@id": f"{BASE}/#localbusiness-of"},
       "breadcrumb": {"@id": f"{BASE}/{slug}#breadcrumb"}, "inLanguage": "en-US"},
      {"@type": "BreadcrumbList", "@id": f"{BASE}/{slug}#breadcrumb", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
        {"@type": "ListItem", "position": 2, "name": crumb, "item": f"{BASE}/{slug}"}]},
    ]
    for kind in KEEP_ENTITIES.get(slug, []):
        for b in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', page, re.S):
            d = json.loads(b)
            if d.get("@type") == kind:
                d.pop("@context", None)
                graph.append(d)
    # qa_strict, not qa: this result is WRITTEN TO A FILE. A None answer here is
    # how the header re-mirror incident wrote null over the canonical pricing block.
    pairs = faq.qa_strict(page)
    # The tag strip leaves a space where a link closed before punctuation
    # ("(see Outcomes) ."). The headers in CLOSE_PUNCT were hand-corrected
    # to close it up; the others still carry the space.
    if slug in CLOSE_PUNCT:
        pairs = [(q, re.sub(r' +([.,;:!?])', r'\1', a)) for q, a in pairs]
    if pairs:
        graph.append({"@type": "FAQPage", "@id": f"{BASE}/{slug}#faq",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]})
    doc = {"@context": "https://schema.org", "@graph": graph}
    note = NOTE.get(slug) or (f"<!-- {slug.upper()} PAGE HEADER JSON-LD · BATCH 3, AUGUST 2026\n"
            f"  Paste into /{slug} → Page Settings → Advanced → Page Header Code Injection,\n"
            f"  replacing any previous block entirely.\n\n"
            f"  FAQPage mirrors the patched on-page FAQ verbatim (tags stripped), in page order.\n"
            f"  LocalBusiness is referenced by @id from the homepage, never redefined here.\n")
    if slug in ("weight-loss", "hiit-personal-trainer-san-diego", "partners"):
        note += ("\n  MOVED: this page previously carried its JSON-LD inline in the page body.\n"
                 "  That markup has been removed from the page and now lives only here.\n")
    note += "-->\n"
    out = note + '<script type="application/ld+json">\n' + json.dumps(doc, indent=2, ensure_ascii=False) + '\n</script>\n'
    path = f'pages/headers/{slug}-header.html'
    if check:
        return open(path).read() == out
    open(path, 'w').write(out)
    return len(pairs), len(graph)

if __name__ == "__main__":
    if "--check" in sys.argv[1:]:
        # Writes nothing. Every header must equal what a run would write.
        drift = [s for s in META if not build(s, check=True)]
        for s in drift: print(f"  DRIFT  pages/headers/{s}-header.html differs from mkheaders.py output")
        print("MKHEADERS: " + ("FAILED" if drift else f"PASSED ({len(META)} headers reproduce byte-for-byte)"))
        sys.exit(1 if drift else 0)
    for slug in META:
        n, g = build(slug)
        print(f"  pages/headers/{slug}-header.html   FAQs={n}  graph nodes={g}")
