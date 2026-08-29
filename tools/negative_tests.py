"""Negative tests for the rule changes made in the Ingest Consolidation run.

tools/README.md: "a green result means nothing until you have seen the check
fail on purpose", and every rule change must be tested in BOTH directions —
it flags a real violation, AND it passes the legitimate copy next to it.
Rules that NARROW scope are the dangerous ones, so every exemption added in
this run carries a fixture proving a real violation in the same shape still
flags on the same page.

    python3 tools/negative_tests.py     # from the repo root
"""
import sys, os, glob, json, re, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import certify, faq

FAILS = []

def check(name, cond, detail=""):
    print(f"  {'ok  ' if cond else 'FAIL'}  {name}" + (f"   {detail}" if detail and not cond else ""))
    if not cond: FAILS.append(name)

# ── faq.py: <summary> widened to <summary ...> ──────────────────────────────
print("\nfaq.py — <summary ...> with attributes")
HSA = open('pages/hsa-fsa-personal-training.html').read()
check("POSITIVE: attribute-carrying <summary class=...> is now extracted",
      len(faq.questions(HSA)) == 9, f"got {len(faq.questions(HSA))}")
check("POSITIVE: every extracted question still pairs with an answer",
      all(a for _, a in faq.qa(HSA)))
check("NEGATIVE: bare <summary> still extracted (territory-page shape)",
      faq.questions("<details><summary>Q one?</summary>"
                    "<div class='x-faq-body'><p>A one.</p></div></details>") == ["Q one?"])
check("NEGATIVE: a <summary> outside any FAQ still yields exactly one question, "
      "not a swallowed block",
      len(faq.questions("<summary data-x='1'>Only me?</summary>")) == 1)

# ── certify: _flatmap must equal _flat on every file in the repo ────────────
print("\ncertify._flatmap — line mapping must not drift from the rule input")
drift = []
for f in sorted(glob.glob('pages/**/*.html', recursive=True)) + \
         sorted(glob.glob('archive/**/*.html', recursive=True)):
    t = open(f).read()
    flat, off = certify._flatmap(t)
    if flat != certify._flat(t) or len(off) != len(flat): drift.append(f)
check("POSITIVE: flattened text identical to _flat() on every file", not drift, str(drift[:3]))
_src = "line one\n<p>line two has WORD here</p>\nline three\n"
_fl, _of = certify._flatmap(_src)
check("POSITIVE: a known token maps back to its real source line",
      certify._line(_src, _of, _fl.find("WORD")) == 2,
      f"got {certify._line(_src, _of, _fl.find('WORD'))}")
_c = "a\n<!-- hidden\nstill hidden -->\n<p>after WORD</p>"
_fl, _of = certify._flatmap(_c)
check("NEGATIVE: a token after a multi-line comment still maps past it",
      certify._line(_c, _of, _fl.find("WORD")) == 4,
      f"got {certify._line(_c, _of, _fl.find('WORD'))}")

# ── certify: accepted exceptions ────────────────────────────────────────────
print("\ncertify.ACCEPTED — named exceptions must not swallow anything else")
FSA = ("FSA funds are typically use-it-or-lose-it within the plan year, so timing "
       "matters more than it does with an HSA")
DISC = ("does not determine eligibility, issue Letters of Medical Necessity, "
        "diagnose conditions, or provide medical or tax advice")
_f, _p = f"pages/hsa-fsa-personal-training.html", 0
check("POSITIVE: the listed phrase on the listed page and rule is excused",
      certify._accepted(_f, "result promised within a window", FSA, 10))
check("POSITIVE: the second listed phrase is excused",
      certify._accepted(_f, "uncertified specialty claim", DISC, 10))
check("NEGATIVE: the same phrase under a DIFFERENT rule is not excused",
      not certify._accepted(_f, "outcome guarantee", FSA, 10))
check("NEGATIVE: the same phrase on a DIFFERENT page is not excused",
      not certify._accepted("pages/about.html", "result promised within a window", FSA, 10))
check("NEGATIVE: a real violation of the same shape on the SAME page still flags",
      not certify._accepted(
          _f, "result promised within a window",
          "See measurable results in 6 weeks with our FSA-eligible program", 10))
check("NEGATIVE: an exception cannot reach a hit far from its phrase",
      not certify._accepted(_f, "result promised within a window", FSA + " " * 900, 950))

# ── certify: header structure exemptions ────────────────────────────────────
print("\ncertify — header/page structural exemptions")

def struct(files):
    """Run the structure section over an explicit file list, return its output."""
    buf = io.StringIO()
    real = glob.glob
    glob.glob = lambda *a, **k: files
    try:
        with contextlib.redirect_stdout(buf): certify.run()
    finally:
        glob.glob = real
    return buf.getvalue()

out = struct(sorted(glob.glob('pages/**/*.html', recursive=True)))
check("POSITIVE: known orphan headers are noted, not counted as findings",
      "known orphan header" in out
      and "[no matching page" not in out)
check("POSITIVE: case-studies and home-3 are not reported as missing a header",
      "pages/case-studies.html  [no header file" not in out
      and "pages/home-3.html  [no header file" not in out)
check("POSITIVE: home-1..home-5 are not reported as missing a header",
      not re.search(r'pages/home-\d\.html  \[no header file', out))
check("POSITIVE: the homepage header is not reported as redefining LocalBusiness",
      "pages/headers/home-header.html  [LocalBusiness redefined]" not in out)
check("NEGATIVE: home-header's FAQ mirror is still CHECKED, against all five bodies",
      "pages/headers/home-header.html  [FAQPage questions do not mirror page] page=11" in out,
      "the shared-header map must not turn the mirror check off")

TMP = 'pages/_negtest_tmp.html'
TMPH = 'pages/headers/_negtest_tmp2-header.html'
try:
    open(TMP, 'w').write("<p>a page with no header at all</p>")
    out2 = struct(sorted(glob.glob('pages/**/*.html', recursive=True)) + [TMP])
    check("NEGATIVE: an unexempted page with no header IS reported",
          f"{TMP}  [no header file" in out2)
finally:
    os.path.exists(TMP) and os.remove(TMP)

try:
    open(TMPH, 'w').write(
        '<script type="application/ld+json">{"@graph":[{"@type":"WebPage",'
        '"about":{"@id":"https://www.omnifittraining.com/#localbusiness-of"}},'
        '{"@type":"LocalBusiness","name":"x"}]}</script>')
    out3 = struct(sorted(glob.glob('pages/**/*.html', recursive=True)) + [TMPH])
    check("NEGATIVE: LocalBusiness redefined in a NON-home header still flags",
          f"{TMPH}  [LocalBusiness redefined]" in out3)
    check("NEGATIVE: a header with no page still reports the missing page",
          f"{TMPH}  [no matching page" in out3)
finally:
    os.path.exists(TMPH) and os.remove(TMPH)

try:
    open(TMPH, 'w').write(
        '<script type="application/ld+json">{"@graph":[{"@type":"WebPage",'
        '"about":{"@id":"https://example.com/#something-else"}}]}</script>')
    out4 = struct(sorted(glob.glob('pages/**/*.html', recursive=True)) + [TMPH])
    check("NEGATIVE: a WebPage whose about does not reference the homepage flags",
          f"{TMPH}  [about not referencing homepage LocalBusiness]" in out4)
finally:
    os.path.exists(TMPH) and os.remove(TMPH)

try:
    open(TMPH, 'w').write('<script type="application/ld+json">{"@type":"Service"}</script>'
                          '<script type="application/ld+json">{ not json }</script>')
    out5 = struct(sorted(glob.glob('pages/**/*.html', recursive=True)) + [TMPH])
    check("NEGATIVE: invalid JSON in a SECOND ld+json block still flags",
          "invalid JSON in block 2" in out5)
finally:
    os.path.exists(TMPH) and os.remove(TMPH)

print("\ncertify.ld_nodes / faq_pairs — multi-block headers")
DW = open('pages/headers/desk-worker-posture-pain-header.html').read()
n, e = certify.ld_nodes(DW)
check("POSITIVE: a FAQPage living in the SECOND block is found",
      not e and any(x.get("@type") == "FAQPage" for x in n))
check("POSITIVE: pairs come back from that second block",
      len(certify.faq_pairs(n)) == 6, f"got {len(certify.faq_pairs(n))}")
ABOUT = open('pages/headers/about-header.html').read()
n2, e2 = certify.ld_nodes(ABOUT)
check("NEGATIVE: an @graph with AboutPage and no WebPage no longer raises",
      not e2 and {x.get('@type') for x in n2} == {"AboutPage", "BreadcrumbList", "Person"})
check("NEGATIVE: a file with no ld+json at all still reports one",
      certify.ld_nodes("<p>nothing</p>")[1] == ["no ld+json block"])

# ── certify: the archive is out of scope by construction ────────────────────
print("\nscope")
check("POSITIVE: no archive/ file can enter the glob certify.py runs on",
      not any(f.startswith('archive/')
              for f in glob.glob('pages/**/*.html', recursive=True)))
check("NEGATIVE: archive/ really does still contain the retired pages",
      len(glob.glob('archive/**/*.html', recursive=True)) == 6)

print("\n" + ("ALL NEGATIVE TESTS PASSED" if not FAILS
              else f"{len(FAILS)} FAILED: {FAILS}"))
sys.exit(1 if FAILS else 0)
