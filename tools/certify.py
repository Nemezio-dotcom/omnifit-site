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
    # <style> and <script> BODIES are not copy. Stripping tags alone left CSS
    # and JS text in the scanned string, which only started to matter once
    # TIER 1 item 1 widened the guarantee rule to any occurrence: a CSS comment
    # `/* GUARANTEE BOX */` on how-it-works-pricing would have read as a
    # customer-facing guarantee. Removed before, not after, the tag strip.
    # ld+json is EXCLUDED from this strip: a header file is nothing BUT one
    # ld+json block, and stripping it blanked every header - ten compliance
    # rules reading an empty string and reporting nothing, the null overwrite
    # in a new costume. Caught by negative-testing the widened guarantee rule
    # against training-rates-san-diego-header, which went silent.
    t = re.sub(r'<style\b[^>]*>.*?</style>', ' ', t, flags=re.S | re.I)
    t = re.sub(r'<script\b(?![^>]*ld\+json)[^>]*>.*?</script>', ' ', t, flags=re.S | re.I)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t)).strip()

# ─── surfaces and TIER 2 conditions ────────────────────────────────
def _surface(text, pos):
    """The copy surface a match sits on: its innermost enclosing <section>,
    falling back to the whole document. TIER 2 conditions must be present ON
    THE SAME SURFACE as the figure they condition - a disclaimer three
    sections away does not condition anything a reader sees."""
    best = None
    for m in re.finditer(r'<section\b[^>]*>', text, re.I):
        if m.start() > pos: break
        depth, i = 0, m.start()
        for t in re.finditer(r'<(/?)section\b[^>]*>', text[m.start():], re.I):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                i = m.start() + t.end(); break
        else:
            i = len(text)
        if m.start() <= pos < i and (best is None or i - m.start() < best[1] - best[0]):
            best = (m.start(), i)
    return text[best[0]:best[1]] if best else text

# TIER 2 item 1 conditions, checked on the surface.
# (a) METHOD - what was measured, sample size, period. Sample size and period
#     are machine-checkable; "what was measured" is prose beside the figure and
#     is the human half of this condition, like substantiation in item 2.
_C_SAMPLE = r'\b(?:n\s*=\s*\d+|\d[\d,]*\+?\s*(?:omnifit\s+)?clients?\b|\d[\d,]*\s*(?:verified\s+)?reviews?\b)'
_C_PERIOD = (r'\b(?:\d+\s*[-–]?\s*(?:day|week|month|year)s?|'
             r'(?:one|two|three|four|six|twelve)[- ](?:day|week|month|year)|'
             r'at time of writing|per month|monthly|each month)\b')
_C_AUDIT  = r'\b(?:not\s+independently\s+audited|company[-\s]reported)\b'
_C_DISCL  = r'individual results?\b[^.]{0,160}?\b(?:vary|varies|depend\w*|not a projection)\b'
# TIER 2 item 5: a surface labelled illustrative is not reporting measurements
# at all, so it is outside item 1 rather than failing it.
_C_ILLUS  = r'\billustrativ\w*\b[^.]{0,60}?\bnot client data\b|\bnot client data\b[^.]{0,60}?\billustrativ\w*\b'

def _t2_conditions(surface):
    """Which of TIER 2 item 1's three conditions the surface carries."""
    f = _flat(surface)
    return {"method":     bool(re.search(_C_SAMPLE, f, re.I) and re.search(_C_PERIOD, f, re.I)),
            "audit note": bool(re.search(_C_AUDIT, f, re.I)),
            "disclaimer": bool(re.search(_C_DISCL, f, re.I))}

def _is_illustrative(surface):
    return bool(re.search(_C_ILLUS, _flat(surface), re.I))

def _near(t, m, window):
    return ' '.join(t[:m.start()].split()[-window:] + t[m.end():].split()[:window])

# ─── TIER 1 item 1 ─────────────────────────────────────────────────
# WIDENED Sept 2026. Was "guarantee within ~30 words of an outcome word".
# TIER 1 bans outcome guarantees OF ANY KIND, conditional and compliance-tied
# included, so proximity to an outcome word is no longer what makes one: the
# approved DEFERRED-01 wording passed the old rule precisely by not sitting
# near an outcome word, and TIER 1 item 1 names DEFERRED-01 as still deferred.
# No approver can clear a TIER 1 finding, so this rule carries no exemption
# list - only the reading of the sentence below.
# negation incl. contractions, checked only on the PRECEDING words so a trailing
# "...and we don't cut corners" cannot exempt a real promise
NEG_WIDE = (r"\b(?:not|never|no|cannot|without|n't|don'?t|doesn'?t|didn'?t|won'?t|"
            r"isn'?t|aren'?t|haven'?t|hasn'?t)\b")

def guarantee_any(text, window=12):
    t = _flat(text); out = []
    for m in re.finditer(r'\bguarantee[ds]?\b', t, re.I):
        # A guarantee stated as ABSENT ("no guarantee", "reimbursement is not
        # guaranteed") is the opposite of the banned shape, not an instance of
        # it. Checked on the PRECEDING words only, so a trailing "...but
        # nothing is guaranteed" cannot launder a real promise ahead of it.
        before = ' '.join(t[:m.start()].split()[-4:])
        if re.search(NEG_WIDE, before + ' ' + m.group(0), re.I): continue
        out.append(("outcome guarantee (T1-1)", f"'{m.group(0)}'",
                    t[max(0, m.start()-100):m.end()+140].strip()))
    return out

# ─── ATTRIBUTED INDIVIDUAL OUTCOMES (owner approval; CANON TIER 2 item 2) ──
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

# TIER 2 item 2 relaxes condition 2 from a DEDICATED BLOCK to anywhere on the
# page. The dedicated-block test was written to counsel's standard and is
# withdrawn for this item (it still governs nothing else: TIER 2 item 1 states
# its own three conditions). Attribution and the never-exempt aggregate test
# are UNCHANGED, which is why how-we-measure-your-progress and
# desk-worker-posture-pain do not gain an exemption from the relaxation - both
# fail attribution independently.
DISCLAIMER_ANYWHERE = re.compile(
    r'individual results?\b[^.]{0,160}?\b(?:vary|varies|varied|depends?|depending|'
    r'not a projection|not projections|not typical)\b', re.I)

def _has_results_disclaimer_anywhere(text):
    return bool(DISCLAIMER_ANYWHERE.search(_flat(text)))

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

# TIER 1 item 2. Units widened Sept 2026 from pounds alone to pounds, INCHES
# and BODY-FAT PERCENTAGE, which the owner's tier names explicitly.
# Inches must be SPELLED. The inch mark (") was tried and withdrawn the same
# run: in ld+json every price is "325.00", so `00"` read as "00 inches" and the
# rule invented 20 findings across three headers out of JSON punctuation. A
# unit symbol that is also the language's most common delimiter cannot be a
# unit token here.
_T1_UNITS = (r'\d[\d,]*(?:\s*(?:–|-|&ndash;|to)\s*\d[\d,]*)?\s*'
             r'(?:lbs?\b|pounds?\b|inches\b|inch\b)'
             r'|\d[\d.,]*\s*%\s*(?:of\s+)?body[\s-]?fat'
             r'|body[\s-]?fat[^.]{0,20}?\d[\d.,]*\s*%')

def lbs_near_timeframe(text, window=15):
    t = _flat(text); out = []
    disclaimed = _has_results_disclaimer_anywhere(text)   # TIER 2 item 2
    for m in re.finditer(_T1_UNITS, t, re.I):
        w = _near(t, m, window)
        for tf in re.finditer(TIMEFRAME, w, re.I):
            if re.search(CONTRAST, w[:tf.start()], re.I): continue
            if _case_study_exempt(t, m, disclaimed): break
            out.append(("lbs/inches/body-fat near timeframe (T1-2)",
                        f"'{m.group(0).strip()}' near '{tf.group(0)}'",
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
            out.append(("free-consultation framing (T1-4)", f"'free' near '{b.group(0)}'",
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
        out.append(("prenatal/postpartum content (T1-3, carried over)", m.group(0),
                    t[max(0, m.start()-100):m.end()+140].strip()))
    return out

# TIER 1 item 3. "Assesses" and "manages" are new to this rule and are SCOPED
# TO A MEDICAL CONDITION: assessing MOVEMENT is what OmniFit does and stays
# legal, so the condition object is required rather than optional. Without that
# scoping the rule would flag "every client starts with a movement assessment"
# across most of the site - a rule failing closed so hard it becomes useless.
# Plurals are explicit: the first version wrote \bmedical condition\b, which does
# not match "medical conditionS" - so "the device is used to diagnose medical
# conditions", the exact sentence TIER 1 item 3 names, passed. Caught by the
# negative test, not by reading the regex.
MEDCOND = (r'\b(?:medical conditions?|health conditions?|diagnos[ei]s|diseases?|'
           r'illness(?:es)?|injur\w+|pain|arthritis|diabet\w+|hypertension|'
           r'blood pressure|insulin resistance|cholesterol|sciatica|'
           r'tendinitis|tendinopathy|herniat\w+|impingement|osteoporosis|'
           r'symptom\w*)\b')

def uncertified_claims(text, window=8):
    t = _flat(text); out = []
    # TIER 1 item 3 - assess / manage a MEDICAL CONDITION
    for m in re.finditer(r'\b(?:we|omnifit(?: performance)?|i)\s+(?:\w+\s+){0,3}?'
                         r'(?:assess|assesses|manage|manages)\b(?:\s+\w+){0,4}', t, re.I):
        if re.search(NEGATED, m.group(0) + ' ' + _near(t, m, 4), re.I): continue
        c = re.search(MEDCOND, m.group(0), re.I)
        if c:
            out.append(("uncertified specialty claim (T1-3) assess/manage a medical condition",
                        f"'{m.group(0).strip()}'",
                        t[max(0, m.start()-100):m.end()+140].strip()))
    # TIER 1 item 3 - a DEVICE used to diagnose / treat / assess a condition
    for m in re.finditer(r'\b(?:device|analyser|analyzer|scanner|bodystat|quadscan)\b'
                         r'[^.]{0,90}?\b(?:diagnos\w+|treat\w+|assess\w+)\b[^.]{0,50}', t, re.I):
        if re.search(NEGATED, m.group(0), re.I): continue
        if re.search(MEDCOND, m.group(0), re.I):
            out.append(("uncertified specialty claim (T1-3) device used to diagnose/assess",
                        m.group(0).strip()[:90],
                        t[max(0, m.start()-100):m.end()+140].strip()))
    pat = (r'\b(?:we|omnifit(?: performance)?|i)\s+(?:\w+\s+){0,2}?'
           r'(diagnose|diagnoses|treat|treats|prescribe|prescribes|cure|cures|'
           r'rehabilitate|rehabilitates)\b')
    for m in re.finditer(pat, t, re.I):
        # negation may sit inside the match ("OmniFit does not diagnose") or beside it
        if re.search(NEGATED, m.group(0) + ' ' + _near(t, m, 4), re.I): continue
        out.append(("uncertified specialty claim (T1-3)", m.group(0).strip(),
                    t[max(0, m.start()-100):m.end()+140].strip()))
    for m in re.finditer(r'\b(?:we|omnifit(?: performance)?)\s+(?:\w+\s+){0,2}?'
                         r'(?:provide|provides|offer|offers|deliver|delivers|perform|performs|do|does)\s+'
                         r'(?:\w+\s+){0,2}?(physical therapy|chiropractic)\b', t, re.I):
        if re.search(NEGATED, m.group(0) + ' ' + _near(t, m, 6), re.I): continue
        out.append(("uncertified specialty claim (T1-3)", m.group(0).strip(),
                    t[max(0, m.start()-100):m.end()+140].strip()))
    return out

CLINICAL = (r'(?:pain|injur\w*|recover\w*|heal\w*|rehab\w*|symptom\w*|inflammation|'
            r'range of motion)')
OUTCOME_FRAME = (r'(?:reduc\w*|decreas\w*|improv\w*|resolv\w*|eliminat\w*|relief|relieved|'
                 r'free of|free from|better|gain\w*|less|fewer)')

# ─── TIER 1 item 5 - phase angle as a RESULT ───────────────────────
# The line CANON draws is description versus outcome, not mention versus
# silence: phase angle may be NAMED as a tracked marker and DESCRIBED as what
# the device measures (TIER 2 item 4), and may not be REPORTED AS A RESULT.
# So the rule keys off a VALUE or a CHANGE word beside the phrase, never on
# the phrase itself - keying on the phrase would make TIER 2 item 4
# unwritable.
_PA_VALUE  = r'\b\d+(?:\.\d+)?\s*(?:°|degrees?|%)|\bphase angle[^.]{0,25}?\b\d+(?:\.\d+)?\b'
_PA_CHANGE = (r'\b(?:improv\w+|increas\w+|ros\w+|rise|risen|gain\w*|up\b|higher|'
              r'better|progress\w*|change[ds]?|delta|from\s+\d|→|->)\b')

def phase_angle_result(text, window=12):
    t = _flat(text); out = []
    for m in re.finditer(r'\bphase angle\b', t, re.I):
        w = _near(t, m, window)
        v = re.search(_PA_VALUE, w, re.I)
        c = re.search(_PA_CHANGE, w, re.I)
        # a value alone can be a device spec; a value WITH a change/outcome word
        # beside it is a result. Requiring both is what keeps "Phase angle - a
        # measurement at 50 kHz relating to cell membrane integrity" legal.
        if v and c:
            out.append(("phase angle reported as a result (T1-5)",
                        f"'{v.group(0).strip()}' + '{c.group(0).strip()}'",
                        t[max(0, m.start()-100):m.end()+140].strip()))
    return out

# ─── TIER 1 item 6 - population-level clinical claims ──────────────
# The part of the old blanket clinical-statistic rule that survives INTACT. No
# method note, sample size or disclaimer clears one: a clinical result rate
# published by a non-clinician is the exposure, which is why this rule is
# consulted BEFORE the TIER 2 item 1 conditions and ignores them.
CLINICAL = (r'(?:pain|injur\w*|recover\w*|heal\w*|rehab\w*|symptom\w*|inflammation|'
            r'range of motion|blood pressure|insulin resistance|cholesterol|'
            r'diabet\w*|hypertension|arthritis|disease)')
OUTCOME_FRAME = (r'(?:reduc\w*|decreas\w*|lower\w*|revers\w*|improv\w*|resolv\w*|'
                 r'eliminat\w*|relief|relieved|free of|free from|better|less|fewer|heal\w*)')
_POP = (r'\b(?:clients?|patients?|people|members|participants|population|'
        r'average|typical|most|\d[\d,]*\s*%|\d[\d,]*\+?\s*clients?)\b')
# The claim must be attributed to OMNIFIT TRAINING, per CANON TIER 1 item 6.
# Without this the rule read a partner's own modality list ("myofascial release
# to improve range of motion") as an OmniFit claim.
_ATTRIB_OF = r'\b(?:omnifit|our (?:training|program|coaching|clients)|the program|our method)\b'
# ANATOMY, not an outcome verb. "lower back pain" is a body part; the rule read
# the "lower" in it as "lowers", and flagged four territory pages describing
# WHO their corrective programming is for. An outcome frame immediately
# followed by one of these is anatomical and never a claim.
_ANATOMY = r'(?:lower|upper)\s+(?:back|body|limb|extremit\w+|trap\w*|ab\w*)'

def population_clinical_claim(text, window=10):
    """A clinical outcome applied at POPULATION scope and attributed to OmniFit
    training. Three conditions, all required: an outcome verb on a clinical
    condition, a population marker, and attribution to OmniFit. Individual
    attributed case-study language is TIER 2 item 2 and is not this rule."""
    t = _flat(text); out = []
    for m in re.finditer(OUTCOME_FRAME + r'\w*\s+(?:\w+\s+){0,3}?' + CLINICAL, t, re.I):
        if re.match(_ANATOMY, m.group(0), re.I): continue          # "lower back pain"
        before = ' '.join(t[:m.start()].split()[-8:])
        if re.search(NEG_WIDE, before + ' ' + m.group(0), re.I): continue
        w = _near(t, m, window)
        if not re.search(_POP, w, re.I): continue                  # population scope
        if not re.search(_ATTRIB_OF, w, re.I): continue            # attributed to OmniFit
        out.append(("population-level clinical claim (T1-6)", m.group(0).strip()[:80],
                    t[max(0, m.start()-100):m.end()+140].strip()))
    return out

# ─── TIER 2 item 1 - aggregate measured metrics, CONDITIONAL ───────
# REPLACES the old blanket clinical_stat ban for everything that is not a
# population-level clinical claim. The old rule banned the figure; this one
# checks the surface for the three conditions and NAMES THE MISSING ONE. A
# finding here is never "you published a number", it is "this number is
# missing its method / audit note / disclaimer".
_AGG = (r'\b(?:average|averages|averaged|median|mean|across\s+\d|our clients|'
        r'client base|typical|typically|per client|of clients)\b')

def aggregate_metric_conditions(text, window=14):
    """Scans the RAW text, not the flattened copy, so each figure's position is
    real and _surface() resolves the section it actually sits in. Flattening
    first and searching back for the figure found the FIRST identical string in
    the document and read the wrong section's conditions."""
    out = []
    for m in re.finditer(r'\d[\d.,]*\s*%', text):
        ctx = _flat(text[max(0, m.start()-900):m.end()+900])
        if not re.search(_AGG, ctx, re.I): continue        # not presented as an aggregate
        surface = _surface(text, m.start())
        if _is_illustrative(surface): continue             # TIER 2 item 5
        missing = [k for k, v in _t2_conditions(surface).items() if not v]
        if missing:
            here = _flat(text[max(0, m.start()-260):m.end()+260])
            out.append((f"aggregate metric missing {' + '.join(missing)} (T2-1)",
                        f"'{m.group(0).strip()}'", here))
    return out

# ─── TIER 2 item 4 - the Class IIa fact and its note ───────────────
_CIIA_NOTE = (r'not a medical provider|not a medical clinic|'
              r'not used to diagnose|does not diagnose')

def class_iia_note(text, window=0):
    """The Class IIa statement is a VERIFIED FACT and stays, but TIER 2 item 4
    attaches two conditions to it. This rule checks the second: the fact must
    carry the not-a-medical-provider note on the same surface. The first
    condition - one byte-identical wording everywhere - is cross-file and is
    checked in run() beside the invariants."""
    out = []
    for m in re.finditer(r'Class IIa', text, re.I):
        surface = _surface(text, m.start())
        if not re.search(_CIIA_NOTE, _flat(surface), re.I):
            f = _flat(text)
            i = f.lower().find('class iia')
            out.append(("Class IIa fact without the not-a-medical-provider note (T2-4)",
                        "'Class IIa medical device'",
                        f[max(0, i-120):i+180].strip()))
    return out

RESULT = (r'(?:measurable|visible|noticeable|significant|dramatic)\s+\w*\s*'
          r'(?:increase|improvement|change|gain|loss|reduction|progress|result)\w*'
          r'|(?:see|seeing|achiev\w+|produc\w+|deliver\w+)\s+(?:\w+\s+){0,3}?'
          r'(?:result|results|change|changes|improvement|improvements|transformation)')

def result_near_timeframe(text, window=12):
    """A result paired with a promised window, in any units. The lbs rule is the
    specific case; results must be framed against the client's own baseline."""
    t = _flat(text); out = []
    disclaimed = _has_results_disclaimer_anywhere(text)   # TIER 2 item 2
    for m in re.finditer(RESULT, t, re.I):
        # a result stated as absent ("produces no change", "don't have ... producing
        # visible results") promises nothing
        before = ' '.join(t[:m.start()].split()[-8:])
        if re.search(NEG_WIDE, m.group(0) + ' ' + before, re.I): continue
        w = _near(t, m, window)
        for tf in re.finditer(TIMEFRAME, w, re.I):
            if re.search(CONTRAST, w[:tf.start()], re.I): continue
            if _case_study_exempt(t, m, disclaimed): break
            out.append(("result promised within a window (T1-2)", f"'{m.group(0).strip()}' near '{tf.group(0).strip()}'",
                        t[max(0, m.start()-100):m.end()+140].strip()))
            break
    return out

# Every rule names the tier it encodes. TIER 1 rules report a violation; TIER 2
# rules report a MISSING CONDITION. See CANON COMPLIANCE SCREEN - TWO TIERS.
COMPLIANCE = [
    guarantee_any,                 # T1-1
    lbs_near_timeframe,            # T1-2
    result_near_timeframe,         # T1-2 (general case)
    uncertified_claims,            # T1-3
    prenatal_postpartum,           # T1-3, carried over
    free_consultation,             # T1-4
    phase_angle_result,            # T1-5
    population_clinical_claim,     # T1-6
    aggregate_metric_conditions,   # T2-1
    class_iia_note,                # T2-4
]

# TIER 2 item 2: historical records, exempt from re-screening ENTIRELY. They
# record measurements that happened; re-screening them would put the run in the
# position of arguing with its own archive.
FROZEN = ("case-studies.html", "home-3.html")

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

class CanonParseFailure(Exception):
    """CANON.md's INVARIANTS block could not be read. Raised rather than
    returning an empty dict: an empty recorded-hash table would make every
    comparison below vacuously true, which is the null-overwrite shape this
    check exists to close."""

# CANON.md records the five invariant hashes in prose, each on its own `- `
# bullet of the INVARIANTS block. Parsed, never hard-coded: a copy of the
# hashes in this file would be a second place to forget to update, and the
# whole point of the check is that CANON is the single recorded source.
#
# Each entry is (bullet anchor, hash pattern) and BOTH are matched inside ONE
# bullet. An earlier version searched the whole block with `.*?` under re.S,
# which let a mangled hash match forward into the NEXT bullet's hash and report
# a neighbouring invariant's value as its own - a parser failing open, exactly
# the shape this check exists to close. Caught by negative-testing a blanked
# archetypes hash, which "parsed" as the 9-point value.
CANON_HASH_PATTERNS = {
    "page pricing":   (r'Canonical pricing FAQ answer:', r'\bpage hash\s+([0-9a-f]{8,64})\b'),
    "header pricing": (r'Canonical pricing FAQ answer:', r'\bheader hash\s+([0-9a-f]{8,64})\b'),
    "credentials":    (r'Credentials block body:',       r'\(([0-9a-f]{8,64})\s*,'),
    "archetypes":     (r'Archetype card bodies',         r'\(hash\s+([0-9a-f]{8,64})\s*;'),
    "9-point":        (r'9-point screen section body',   r'\(hash\s+([0-9a-f]{8,64})\s*;'),
}

def canon_hashes(path="CANON.md"):
    """The five invariant hashes as CANON.md records them.

    Returns (hashes, problems): hashes maps invariant name -> recorded hex
    string, problems lists the names whose recorded value could not be read.
    A name that cannot be parsed is reported, never defaulted - an invariant
    with no recorded hash is an UNVERIFIED invariant, not a matching one."""
    try:
        text = open(path).read()
    except OSError as e:
        raise CanonParseFailure(f"cannot read {path}: {e}")
    m = re.search(r'^INVARIANTS\b.*?(?=^[A-Z][A-Z0-9 ,/&-]+$)', text, re.S | re.M)
    if not m:
        raise CanonParseFailure(f"no INVARIANTS block found in {path}")
    bullets = re.split(r'^- ', m.group(0), flags=re.M)[1:]
    hashes, problems = {}, []
    for key, (anchor, rx) in CANON_HASH_PATTERNS.items():
        owning = [b for b in bullets if re.search(anchor, b, re.I)]
        if len(owning) != 1:
            problems.append(key); continue      # absent, or ambiguous across bullets
        hit = re.search(rx, owning[0], re.S | re.I)
        if hit: hashes[key] = hit.group(1).lower()
        else:   problems.append(key)
    if not hashes:
        raise CanonParseFailure(
            f"INVARIANTS block found in {path} but not one of the five hashes parsed")
    return hashes, problems

def canon_hash_matches(recorded, computed):
    """CANON records some hashes truncated (credentials as `6492e3ca`, the rest
    at 16 hex). Compare on the recorded prefix: a shorter recorded value is a
    weaker check, not a mismatch. CANON_HASH_PATTERNS requires >= 8 hex chars,
    so the prefix is never trivially short."""
    return computed[:len(recorded)] == recorded

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
    ciia = {}
    for f in files:
        t = open(f).read()
        # TIER 2 item 2: frozen historical records are exempt from re-screening.
        if os.path.basename(f) in FROZEN:
            print(f"   {f}  [frozen historical record - not re-screened, CANON TIER 2 item 2]")
            continue
        for fn in COMPLIANCE:
            for kind, what, ctx in fn(t):
                print(f"   {f}\n      [{kind}] {what}\n      …{ctx[:130]}…"); A+=1
        # TIER 2 item 4, first condition: ONE byte-identical wording of the
        # Class IIa fact everywhere it appears. Cross-file, so it is collected
        # here and judged once below - the same shape as an invariant.
        # Compare a WORD WINDOW around the phrase, not the sentence: in a header
        # the fact sits inside ld+json, so a sentence-based split swept up
        # `" } }, { "@type": "Question"` and made the page and its own header
        # look like two different wordings of the same claim.
        ft = _flat(t)
        for m in re.finditer(r'Class IIa', ft, re.I):
            w = ' '.join(ft[:m.start()].split()[-12:] + [m.group(0)] + ft[m.end():].split()[:12])
            ciia.setdefault(_norm(w), []).append(f)
    if len(ciia) > 1:
        print(f"   [Class IIa fact not byte-identical across files (T2-4)] "
              f"{len(ciia)} distinct wordings:")
        for w, fs in sorted(ciia.items(), key=lambda x: -len(x[1])):
            print(f"      {len(fs)}x  {', '.join(sorted(set(fs)))}\n         …{w[:160]}…")
        A += 1
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
    # The hashes CANON.md records, read once per run. A parse failure is
    # recorded, never swallowed: with no recorded table the comparison below
    # would pass vacuously on every invariant.
    try:
        canon_rec, canon_unparsed = canon_hashes()
    except CanonParseFailure as e:
        # One loud line rather than five: it already says every invariant went
        # uncompared, and the hash table below prints NOT RECORDED for each.
        canon_rec, canon_unparsed = {}, []
        notrun.append(f"CANON.md invariant hashes NOT READ - {e}; "
                      f"no invariant was compared against its recorded value")
    for f in files:
        s=open(f).read()
        p=_P(); p.feed(s)
        if p.st or p.err:
            print(f"   {f}  [tag balance] unclosed={p.st} errors={p.err[:3]}"); C+=1
        if '/headers/' in f:
            # EVERY ld+json block, not just the first. A header may carry its
            # nodes across several <script> blocks - desk-worker-posture-pain
            # puts Service in block 1 and its 6-question FAQPage in block 2 -
            # and re.search stopped at block 1, so the mirror check compared 6
            # page questions against 0 schema questions and called the HEADER
            # broken. That was the checker not looking, reported as a defect in
            # the file it failed to read.
            blocks=re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>',s,re.S)
            if not blocks: print(f"   {f}  [no ld+json block]"); C+=1; continue
            graph=[]; graphed=False; bad=False
            for i,b in enumerate(blocks,1):
                try: doc=json.loads(b)
                except Exception as e:
                    print(f"   {f}  [invalid JSON in ld+json block {i} of {len(blocks)}] {e}"); C+=1; bad=True; break
                if isinstance(doc, dict) and "@graph" in doc:
                    graph.extend(doc["@graph"]); graphed=True
                else:
                    graph.append(doc)
            if bad: continue
            # Not every header in the repo is a Batch-3-shaped @graph document
            # (the homepage header IS the LocalBusiness definition, and several
            # uploaded headers are a single bare node). A check that cannot be
            # applied is recorded as NOT RUN, never silently skipped: the shape
            # is outside what CANON specifies for page headers, so calling it a
            # violation would be inventing a rule, and calling it a pass is how
            # three earlier checks came to report success without looking.
            n={x["@type"]:x for x in graph if isinstance(x, dict) and "@type" in x}
            if not graphed:
                notrun.append(f"{f}  ld+json is {len(blocks)} bare node(s), not an @graph document"
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
    # Two distinct failures, deliberately reported as two finding classes.
    # [invariant mismatch]  - the files carrying an invariant disagree with
    #                         EACH OTHER.
    # [canon hash stale]    - the files agree, and what they agree on is not
    #                         what CANON.md records. Files agreeing with one
    #                         another proves only that an edit was applied
    #                         consistently; until this run, a consistently
    #                         edited invariant sailed past with a stale CANON
    #                         value and nothing said a word. Same shape as the
    #                         null overwrite: a comparison that never looked at
    #                         the thing it claimed to check.
    for k in ("page pricing","header pricing","credentials","archetypes","9-point"):
        v=inv.get(k); rec=canon_rec.get(k)
        if rec is None or not v: continue     # reported under CHECKS THAT COULD NOT RUN
        if not any(canon_hash_matches(rec, c) for c in v):
            got = ' '.join(sorted(v))
            how = "files agree on" if len(v)==1 else "files disagree; none of"
            print(f"   [canon hash stale] {k}: {how} {got}, CANON.md records {rec}"); C+=1
    print("   none" if not C else f"   {C} problem(s)")

    print("\n### INVARIANT HASHES (computed, vs the value recorded in CANON.md)")
    for k in ("page pricing","header pricing","credentials","archetypes","9-point"):
        v=inv.get(k); rec=canon_rec.get(k)
        got = 'MISSING - not found on any file' if not v else ' '.join(sorted(v))
        if rec is None:   note = "CANON: NOT RECORDED - not compared"
        elif not v:       note = f"CANON: {rec} - not compared"
        elif any(canon_hash_matches(rec, c) for c in v): note = f"CANON: {rec}  ok"
        else:             note = f"CANON: {rec}  STALE"
        print(f"   {k:16} {got:24} {note}")
        if not v: notrun.append(f"invariant '{k}' matched no file - hash not verified")
        if k in canon_unparsed:
            notrun.append(f"invariant '{k}' has no parseable hash in CANON.md - "
                          f"computed value not compared against any recorded value")

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
