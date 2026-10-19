"""Certification per CANON.md. Reports exactly three categories:
(a) compliance strikes  (b) stale canon  (c) broken structure.
Nothing else is a finding. Em-dashes are NOT scanned (voice preference).
Every rule is expressed as a rule, never a line number, and negative-tested."""
import re, glob, json, hashlib, html, html.parser, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import faq

# Headers whose page is not pages/<slug>.html. Only the homepage: it lives
# as the home-0..6 fragments and its FAQ is in home-5 (CANON, ORPHAN HEADERS).
HEADER_PAGE = {"home": "pages/home-5.html"}

# schema.org subtypes of WebPage that count as a header's page node.
# about-header uses AboutPage; it carries the same "about" reference.
PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage")

# Pages that have no FAQ BY DESIGN (CANON, "PAGES WITH NO FAQ"). For these an
# empty mirror is not "compared nothing": certify scans the page body for any
# FAQ-shaped markup and the header for any FAQPage, and passes only when both
# are absent. Anything FAQ-shaped on a declared page is a finding, so a page
# that later grows an FAQ cannot hide behind this list. Pages NOT on the list
# still report an empty mirror under CHECKS THAT COULD NOT RUN.
NO_FAQ = {"about", "contactform", "fit-check", "personal-training-services",
          "privacy-policy", "terms-and-conditions"}
FAQ_SHAPED = (r'<details\b|<summary\b|class="[^"]*(?:faq|accordion)|class="fq\b|'
              r'Frequently Asked Questions|"FAQPage"')

# the-30-minute-executive-reset left this list in the October Card run's
# follow-up, once its content was brought to the card and its RED-PEN flags
# closed. footer.html is site-wide and in no batch.
OUT_OF_SCOPE = ("footer",)

# ─── (a) compliance shapes ─────────────────────────────────────────
OUTCOME = (r'stronger|leaner|energized|energised|more in control|lose|losing|lost|fat loss|'
           r'transformation|results?|pounds?|lbs|body fat|inches')
_UNIT = r'(?:day|week|month|year)s?'
# A timeframe bounds an outcome window only when it is numerically quantified
# ("4-6 months", "Weeks 5-8", "Month 3") or rate-framed ("per week", "/week").
# Bare duration nouns ("after years of inactivity") do not bound a window.
# Any dash character counts as a range separator (Oct 18 2026 audit run): the
# hyphen, en dash and em dash, raw or as an HTML entity, and "to". The em dash
# was missing, so "4—6 months" was not a timeframe.
_DASH = r'(?:[-–—‒]|&ndash;|&mdash;|&#821[12];|to)'
TIMEFRAME = (r'(?:\b\d[\d,]*\+?\s*(?:' + _DASH + r')?\s*\d*\+?\s*' + _UNIT + r'\b'
             r'|\b' + _UNIT + r'\s*\d+(?:\s*' + _DASH + r'\s*\d+)?\b'
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

# negation incl. contractions, checked only on the PRECEDING words so a trailing
# "...and we don't cut corners" cannot exempt a real promise
NEG_WIDE = (r"\b(?:not|never|no|cannot|without|n't|don'?t|doesn'?t|didn'?t|won'?t|"
            r"isn'?t|aren'?t|haven'?t|hasn'?t)\b")

# ─── TIER 1 item 1 ─────────────────────────────────────────────────
# NARROWED Sept 12 2026 by owner decision. Two draftings, both wrong once:
#   v1  "guarantee" within ~30 words of an outcome word - missed the
#       DEFERRED-01 wording, which was written not to sit near one.
#   v2  any "guarantee" at all - caught that wording, and everything else,
#       including a refund policy that promises no result whatsoever.
# What makes a guarantee a TIER 1 violation is the RESULT it promises, not
# that it is called a guarantee. A promise about MONEY - a refund, an exit -
# is CANON TIER 2 item 6 and is legal. So the rule asks whether a RESULT NOUN
# is the object of the guarantee, or sits anywhere in the same sentence.
RESULT_NOUN = (r'\b(?:fat loss|weight loss|lose|losing|lost|drop\w*|shed\w*|'
               r'pounds?|lbs|inches|body fat|strength|stronger|muscle|'
               r'pain reduction|pain relief|posture|leaner|'
               r'results?|outcomes?|transformation|gains?|'
               r'improvement|progress)\b')

def guarantee_any(text, window=12):
    t = _flat(text); out = []
    for m in re.finditer(r'\bguarantee[ds]?\b', t, re.I):
        # A guarantee stated as ABSENT ("reimbursement is not guaranteed") is
        # the opposite of the banned shape. Preceding words only, so a trailing
        # "...but nothing is guaranteed" cannot launder a promise ahead of it.
        if re.search(NEG_WIDE, ' '.join(t[:m.start()].split()[-4:]) + ' ' + m.group(0), re.I):
            continue
        # The SENTENCE the guarantee sits in, not a word window: "guarantee"
        # and the result it promises can sit either side of a comma or colon
        # ("30-Day Fit Guarantee: you will be stronger"), and a fixed window
        # either clips the promise or reaches into the next sentence.
        lo = max((t.rfind(c, 0, m.start()) for c in '.!?'), default=-1) + 1
        hi = min((x for x in (t.find(c, m.end()) for c in '.!?') if x != -1), default=len(t))
        sentence = t[lo:hi + 1]
        r = re.search(RESULT_NOUN, sentence, re.I)
        if r:
            out.append(("outcome guarantee (T1-1)",
                        f"'{m.group(0)}' promising '{r.group(0)}'", sentence.strip()))
    return out

# ─── ATTRIBUTED INDIVIDUAL OUTCOMES (owner approval; CANON TIER 2 item 2a) ──
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
             r'most clients|our clients|every client|'
             # "putting everyone else first" describes a client's life, not a
             # population: the Oct 17 2026 over-50 proof card sat 45 words from
             # it and lost its TIER 2 item 2a exemption. "everyone loses" fires.
             r'everyone(?!\s+else)|anyone(?!\s+else)|'
             r'clients\s+(?:lose|gain|drop|see|can|will)|'
             r'you\s+(?:\w+\s+){0,2}?(?:lose|gain|drop|expect|see|will|can)|'
             r"you'll|expect to|up to)\b")

# TIER 2 item 2a relaxes condition 2 from a DEDICATED BLOCK to anywhere on the
# page. The dedicated-block test was written to counsel's standard and is
# withdrawn for this item (it still governs nothing else: TIER 2 item 1 states
# its own three conditions). Attribution and the never-exempt aggregate test
# are UNCHANGED, which is why how-we-measure-your-progress and
# desk-worker-posture-pain do not gain an exemption from the relaxation - both
# fail attribution independently.
# The condition word may sit in the SAME sentence or the NEXT one (Oct 17
# 2026): "Individual results. Outcomes depend on starting point ... and vary
# between clients." is the over-50 page's disclaimer, and the one-sentence
# reading stopped at the first period and called the page undisclaimed. Still
# bounded: one sentence break, 160 characters either side of it.
DISCLAIMER_ANYWHERE = re.compile(
    r'individual results?\b[^.]{0,160}?(?:\.[^.]{0,160}?)?\b(?:vary|varies|varied|depends?|depending|'
    r'not a projection|not projections|not typical)\b', re.I)

def _selftest_case_study_exempt():
    """Both directions, every run, for the two Oct 17 2026 fixes above."""
    d = '<p>Individual results. Outcomes depend on starting point and vary between clients.</p>'
    assert _has_results_disclaimer_anywhere(d), "two-sentence disclaimer not recognised"
    assert not _has_results_disclaimer_anywhere('<p>Individual results. Call us today. We train in 4S Ranch.</p>'), \
        "disclaimer recognised with no condition word"
    card = ('<p>Years of putting everyone else first.</p><div>−11 lb bodyweight, 6 months</div>'
            '<div>Ken · CTO · 50s</div>')
    assert lbs_near_timeframe(card + d) == [], "attributed, disclaimed card still fired"
    assert lbs_near_timeframe(card), "attributed card with no page disclaimer did not fire"
    assert lbs_near_timeframe('<p>Everyone loses 11 lb in 6 months.</p><div>Ken · CTO</div>' + d, outcomes=''), \
        "aggregate framing ('everyone loses') was exempted"
    assert lbs_near_timeframe('<p>Clients lose 11 lb in 6 months.</p>' + d, outcomes=''), "unattributed figure was exempted"
    # Owner decision, homepage rebuild Oct 17 2026: the verbatim 2a disclosure
    # pointer is not aggregate wording; anything else still is.
    p2a = ('<p>Individual result, measured by OmniFit. How clients typically progress: '
           '<a href="/outcomes">omnifittraining.com/outcomes</a>.</p>')
    named = '<div>Mark · Board member</div><p>Mark came in at 248 lbs and went to 231 lbs over 4 months.</p>'
    # (1) a named card carrying the verbatim disclosure passes
    assert lbs_near_timeframe(named + p2a + d, outcomes='') == [], "named card with the verbatim 2a disclosure fired"
    #     ... wherever the 45-word window edge falls across the sentence
    for n in range(25, 55):
        pad = '<p>' + 'word ' * n + '</p>'
        assert lbs_near_timeframe(named + pad + p2a + d, outcomes='') == [], \
            f"verbatim 2a disclosure split by the window edge fired (pad {n})"
    # (2) a named card beside "clients typically lose 10 lbs in 3 months" still fails, on the named figure too
    agg = lbs_near_timeframe(named + '<p>Our clients typically lose 10 lbs in 3 months.</p>' + p2a + d, outcomes='')
    assert any('231' in x[1] or '248' in x[1] for x in agg), "aggregate 'typically' beside a named card was exempted"
    # (3) the disclosure with one word changed is NOT exempt
    p2a_bad = p2a.replace('typically progress', 'typically improve')
    assert lbs_near_timeframe(named + p2a_bad + d, outcomes=''), "near-verbatim 2a pointer was exempted"

def _selftest_lbs_fragment():
    """Oct 18 2026 audit (item 9), both directions, every run: a pounds range
    with a "+", any dash character and a quantified timeframe after in / over /
    within is a T1-2 strike in a list item or a bare fragment."""
    for bad in ('<li>20–30+ lbs in 4–6 months</li>',          # the exact retired line (en dash)
                '<li>20-30+ lbs in 4-6 months</li>',          # hyphen
                '<li>20—30+ lbs in 4—6 months</li>',          # em dash
                '<li>20&ndash;30 lbs in 4&ndash;6 months</li>',
                '<li>15-20 lbs within 8-12 weeks</li>', '<span>10 to 15 pounds over 3 to 6 months</span>',
                '<li>Lose 20+ lb in 12 weeks</li>', '<p>Lose 10 lbs every 4 weeks.</p>',
                '<p>From $200 per 4 weeks. Lose 20 lbs in 8 weeks.</p>'):    # run 7: a price beside a real claim
        assert lbs_near_timeframe(bad, outcomes=''), f"T1-2 fragment passed: {bad}"
    d = '<p>Individual results. Outcomes depend on starting point and vary between clients.</p>'
    p2a = ('<p>Individual result, measured by OmniFit. How clients typically progress: '
           '<a href="/outcomes">omnifittraining.com/outcomes</a>.</p>')
    for ok in ('<li>Sustainable fat loss, no crash diets</li>',
               '<p>sustainable fat loss of 20-30 lbs</p>',      # TIER 2 item 3: no timeframe
               '<p>Virtual Executive Reset from $200 per 4 weeks.</p><p>Lose 20–30+ lbs sustainably.</p>',  # billing cadence
               # run 7: the cadence split from its price by the window edge
               '<p>Virtual Executive Reset from $200 per 4 weeks</p><a>Explore Virtual Coaching →</a><h3>📉 Weight Loss Coaching</h3><p>For professionals aiming to lose 20–30 lbs sustainably: progressive training.</p>',
               '<div>Mark · Board member</div><p>Mark came in at 248 lbs and went to 231 lbs over 4 months.</p>' + p2a + d):
        assert lbs_near_timeframe(ok, outcomes='') == [], f"legitimate copy fired: {ok[:60]}"

def _has_results_disclaimer_anywhere(text):
    return bool(DISCLAIMER_ANYWHERE.search(_flat(text)))

DISCLOSURE_2A_POINTER = re.compile(r'How clients typically progress:\s*omnifittraining\.com/outcomes\s*\.')

def _case_study_exempt(t, m, page_disclaimed, window=45):
    """True when this match is a documented individual case-study figure on a
    page carrying the individual-results disclaimer. Fails CLOSED: anything the
    attribution test cannot confirm stays a strike."""
    if not page_disclaimed:                       # condition 2
        return False
    # OWNER DECISION, homepage rebuild Oct 17 2026 (the T2-1 checker fix's
    # twin): the verbatim TIER 2 item 2a disclosure sentence "How clients
    # typically progress: omnifittraining.com/outcomes." points AWAY from the
    # figure and is not aggregate wording. ONLY that exact sentence is blanked
    # for this test, on the whole text BEFORE the window is cut (same length,
    # so positions hold; a window edge must not split the sentence and leave a
    # bare "typically"). t is flattened, so a link-wrapped URL reads
    # "outcomes ."; any other "typically" / "most clients" / "on average"
    # still fails.
    a = DISCLOSURE_2A_POINTER.sub(lambda x: ' ' * len(x.group(0)), t)
    w = ' '.join(a[:m.start()].split()[-window:] + a[m.end():].split()[:window])
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
# Oct 18 2026 (external audit): "<li>20–30+ lbs in 4–6 months</li>" - the
# exact TIER 1 item 2 example - sat on six town pages and certified clean. Root
# cause: the "+" after the range ("30+") broke the unit match (the pattern
# wanted the unit straight after the digits), and the em dash was not a range
# separator. A "+" may now follow either number, and any dash counts
# (_DASH). Self-tested both ways in _selftest_lbs_fragment.
_T1_UNITS = (r'\d[\d,]*\+?(?:\s*' + _DASH + r'\s*\d[\d,]*\+?)?\s*'
             r'(?:lbs?\b|pounds?\b|inches\b|inch\b)'
             r'|\d[\d.,]*\s*%\s*(?:of\s+)?body[\s-]?fat'
             r'|body[\s-]?fat[^.]{0,20}?\d[\d.,]*\s*%')

BILLING_CADENCE = r'\$\s?[\d,]+(?:\.\d\d)?\s*(?:/\s*|(?:per|every|each|a)\s+)$'

# A price with its billing cadence ("$200 per 4 weeks"), blanked to spaces of
# the same length before the window is cut (positions hold). The in-window
# BILLING_CADENCE test below misses it when the window edge splits the price
# from its cadence: run 7 (Oct 18 2026) moved the Carmel Valley figure four
# words later ("For professionals aiming to lose 20–30 lbs"), the window then
# began at "per 4 weeks", and the neighbouring card's Reset price read as an
# outcome window. Self-tested both ways in _selftest_lbs_fragment.
BILLED_TIMEFRAME = (r'\$\s?[\d,]+(?:\.\d\d)?\s*(?:/\s*|(?:per|every|each|a)\s+)'
                    r'(?:\d[\d,]*\s*)?' + _UNIT + r'\b')

def lbs_near_timeframe(text, window=15, outcomes=None):
    t = _flat(text); out = []
    t = re.sub(BILLED_TIMEFRAME, lambda x: ' ' * len(x.group(0)), t, flags=re.I)
    disclaimed = _has_results_disclaimer_anywhere(text)   # TIER 2 item 2a
    for m in re.finditer(_T1_UNITS, t, re.I):
        w = _near(t, m, window)
        for tf in re.finditer(TIMEFRAME, w, re.I):
            if re.search(CONTRAST, w[:tf.start()], re.I): continue
            # A billing cadence ("$200 per 4 weeks", "$640 every 4 weeks") is a
            # price, not an outcome window. Surfaced when the "+" fix (Oct 18
            # 2026) let "Lose 20–30+ lbs sustainably" match on Carmel Valley,
            # 15 words from the neighbouring card's "$200 per 4 weeks".
            if re.search(BILLING_CADENCE, w[:tf.start()], re.I): continue
            if _case_study_exempt(t, m, disclaimed): break
            # TIER 1 item 2 carve-out (Outcome Claims Amendment, Oct 1 2026):
            # an aggregate figure with a timeframe stays banned UNLESS it is
            # published on /outcomes with its method, n and date range.
            # `outcomes` overrides the live page for the self-test only.
            if _published_with_method(m.group(0), outcomes): break
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
    attributed case-study language is TIER 2 item 2a and is not this rule."""
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
    # The TIER 2 item 2a disclosure says "How clients typically progress" and
    # points AWAY from the figure; it is the individual-result label, not
    # aggregate framing. Only that verbatim pointer (link-wrapped or not) is
    # blanked, same length so positions hold, and only for the framing test:
    # any other "typically" near a figure still reads as aggregate.
    framing = re.sub(r'How clients typically progress:\s*(?:<a\b[^>]*>\s*)?omnifittraining\.com/outcomes',
                     lambda x: re.sub(r'[^\n]', ' ', x.group(0)), text)
    for m in re.finditer(r'\d[\d.,]*\s*%', text):
        ctx = _flat(framing[max(0, m.start()-900):m.end()+900])
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

REVIEW_CADENCE = r'\breview(?:ed|s)?\b(?:\s+\S+){0,4}?\s+(?:every|each)\s+$'
# Promise verbs that void the REVIEW_CADENCE exemption when they share the
# result's sentence (owner follow-up to run 7B, Oct 18 2026).
PROMISE_VERB = r"\b(?:will|you'll|you\u2019ll|expect\w*|see|seeing|sees|guarantee\w*)\b"

def _promise_in_sentence(t, m):
    """True when the sentence around result match m carries a promise verb.
    The sentence runs from the last . ! or ? before the match to the next one
    after it, in the flattened copy."""
    a = max(t.rfind(c, 0, m.start()) for c in '.!?') + 1
    ends = [i for i in (t.find(c, m.end()) for c in '.!?') if i != -1]
    return bool(re.search(PROMISE_VERB, t[a:min(ends) if ends else len(t)], re.I))

def _selftest_result_review_cadence():
    """Both directions, every run (run 7B): a review cadence passes; a result
    promised within a window still fires, beside a cadence or not."""
    ok = ('<p>This is where most of the measurable progress is built, reviewed against '
          'your baseline every 4 weeks.</p>')
    assert result_near_timeframe(ok) == [], "review cadence fired as an outcome window"
    for bad in ('<p>You will see measurable progress every 4 weeks.</p>',
                '<p>Measurable progress in 8 weeks, reviewed every 4 weeks.</p>',
                '<p>Measurable progress, reviewed every 4 weeks, within 8 weeks.</p>',
                '<p>Visible results every 4 weeks, review included.</p>',
                '<p>You will see dramatic results at each review every 4 weeks.</p>',   # promise verb voids the cadence
                '<p>Expect measurable progress, reviewed every 4 weeks.</p>',
                '<p>We guarantee measurable progress, reviewed every 4 weeks.</p>'):
        assert result_near_timeframe(bad), f"T1-2 window promise passed: {bad}"

def result_near_timeframe(text, window=12):
    """A result paired with a promised window, in any units. The lbs rule is the
    specific case; results must be framed against the client's own baseline."""
    t = _flat(text); out = []
    disclaimed = _has_results_disclaimer_anywhere(text)   # TIER 2 item 2a
    for m in re.finditer(RESULT, t, re.I):
        # a result stated as absent ("produces no change", "don't have ... producing
        # visible results") promises nothing
        before = ' '.join(t[:m.start()].split()[-8:])
        if re.search(NEG_WIDE, m.group(0) + ' ' + before, re.I): continue
        w = _near(t, m, window)
        for tf in re.finditer(TIMEFRAME, w, re.I):
            if re.search(CONTRAST, w[:tf.start()], re.I): continue
            # A REVIEW CADENCE is not an outcome window (run 7B, Oct 18 2026):
            # "progress ... reviewed against your baseline every 4 weeks" says
            # how often progress is checked, not what it will be by when. Only
            # "review(ed|s)" up to four words before "every/each <n> <unit>"
            # qualifies; every other timeframe in the window is still checked.
            # ... unless the sentence carrying the result also makes a promise
            # ("You will see dramatic results at each review every 4 weeks").
            if re.search(REVIEW_CADENCE, w[:tf.start()], re.I) and not _promise_in_sentence(t, m): continue
            if _case_study_exempt(t, m, disclaimed): break
            out.append(("result promised within a window (T1-2)", f"'{m.group(0).strip()}' near '{tf.group(0).strip()}'",
                        t[max(0, m.start()-100):m.end()+140].strip()))
            break
    return out

# ─── OUTCOME CLAIMS AMENDMENT (owner-approved Oct 1 2026; applied Oct 17 2026) ──
# CANON TIER 2 item 2a (attributed individual outcomes: five conditions) and
# item 2g (data-backed figures), plus the TIER 1 item 2 carve-out for an
# aggregate figure that is published on /outcomes with its method, n and date
# range. Conditions (1) consent and (2) measured-by-OmniFit-with-dates are
# human warranties; (1) is checked against the OWNER-ATTESTED CONSENT LIST
# below because certify cannot read a consent form, and (2) is not checked.
# Conditions (3), (4) and (5) are machine-checkable and are checked here.
#
# These two rules COUNT toward the result. The amendment run (Oct 17 2026)
# recorded them with AMENDMENT_COUNTS = False and listed the 17 instances the
# site failed; the follow-up run the same day brought the copy to 2a and
# flipped it to True (owner decision). Set it back to False only to report a
# new rule's first sweep without failing the run; the findings print in full
# either way and the RESULT line carries their count.
AMENDMENT_COUNTS = True

# Owner-attested written consent (CANON TIER 2 item 2a, Oct 17 2026). First
# name, optional initial. A figure attributed to anyone else - or to an
# anonymised profile, which no list can vouch for - is a consent finding.
CONSENT_LIST = ["Isaac M.", "Egor B.", "Chad C.", "Alo S.", "Mark M.", "Vincent", "Ken", "Dave R.", "Mariano G."]
_CONSENT_FIRST = sorted({n.split()[0] for n in CONSENT_LIST}, key=len, reverse=True)
_CONSENT_RX = re.compile(r'\b(' + '|'.join(map(re.escape, _CONSENT_FIRST)) + r')\b(?:\s+[A-Z]\.)?')

# Condition (4), verbatim, on the same surface as the figure.
DISCLOSURE_2A = ("Individual result, measured by OmniFit. How clients typically progress: "
                 "omnifittraining.com/outcomes.")
_OUTCOMES_FILES = ("outcomes.html", "outcomes-header.html")
# ON /outcomes ONLY (owner, Oct 17 2026) the disclosure is its first sentence
# alone: the full line points the reader at the page they are already on.
# Page-scoped to outcomes.html and its header, and exact both ways: the full
# line there is NOT the /outcomes disclosure, and the short line anywhere else
# is not the disclosure at all.
DISCLOSURE_2A_OUTCOMES = "Individual result, measured by OmniFit."
_SHORT_ONLY = re.compile(re.escape(DISCLOSURE_2A_OUTCOMES) + r'(?!\s*How clients typically progress)')

def _has_disclosure(surface, page=None):
    """Condition (4) on one flattened, normalised surface. `page` is the file's
    basename; None means an ordinary page."""
    if page in _OUTCOMES_FILES:
        return bool(_SHORT_ONLY.search(surface))
    return DISCLOSURE_2A in surface

# Condition (3): elapsed time stated as fact. "in just" is the owner's named
# shape; "in only" and "in as little as" are the same minimiser with a
# different word and are caught with it, because a rule that matches one
# literal string is the literal-string free-framing miss again.
_MINIMISER = r'\bin\s+(?:just|only|as little as)\b'
# Condition (5): third person, past tense, no projection, no "you".
_SECOND_PERSON = r"\b(?:you|your|yours|yourself|you'?ll|you'?re|you'?ve)\b"
_FIRST_PERSON  = r"\bI\b|\bI'?(?:m|ve|d)\b|(?i:\b(?:my|me|mine|myself)\b)"
_PROJECTION    = r"\b(?:will|would|can|could|should|expect\w*|typical\w*|up to|on average|projected)\b"
_PRESENT_TENSE = (r"\b(?:he|she|they|clients?|who)\s+(?:lose|gain|drop|shed|build|add)s?\b"
                  r"|(?<!muscle )(?<!strength )(?<!lean )(?<!mass )\b(?:loses|gains|drops|sheds)\b"
                  r"|\b(?:is|are)\s+(?:losing|gaining|dropping|shedding|building|adding)\b")

# A client-results FIGURE: pounds, inches, body-fat %, or a bare percentage.
_FIGURE = re.compile(_T1_UNITS + r'|\d[\d.,]*\s*%', re.I)

_NONPERSON = {"San", "Diego", "OmniFit", "Omnifit", "Teqneeq", "Nemezio", "Coach", "Performance",
              "Bodystat", "Ranch", "North", "County", "The", "Our", "Every", "Executive",
              "Client", "Clients", "Most", "Results", "Individual", "Google", "Yelp", "Bark",
              "Thumbtack", "Precision", "Nutrition", "Trainerize", "Program", "Foundation",
              "This", "That", "These", "Those", "There", "Here", "What", "Which", "When",
              "Where", "Why", "How", "Each", "Some", "Many", "Other", "Another", "Illustrative",
              "Trials", "Research", "Published", "Measured", "Between", "Among", "After",
              "Before", "Since", "During", "Within", "Also", "Then", "Still", "Because",
              "While", "Although", "Training", "Strength", "Progress", "Session", "Sessions",
              "Body", "Weight", "Muscle", "Posture", "Example", "Summary", "Note", "Method",
              "Age", "Rate", "Share", "Profile", "Goal", "Reset", "Momentum", "Peak", "Full",
              "Coached", "Train", "Studio", "Home", "Virtual", "Hybrid", "Phase", "Class",
              "Case", "Study", "Proof", "Documented", "Outcomes", "Real", "Verified"}

def _blank_noncopy(text):
    """Comments, <style> and non-ld+json <script> bodies replaced by spaces of
    the same length, so positions and line numbers survive and CSS percentages
    never read as figures."""
    def blank(m): return re.sub(r'[^\n]', ' ', m.group(0))
    text = re.sub(r'<!--.*?-->', blank, text, flags=re.S)
    # inline style attributes carry bar widths ("width:94%") that are not copy
    text = re.sub(r'\sstyle="[^"]*"', blank, text, flags=re.I)
    text = re.sub(r'<style\b[^>]*>.*?</style>', blank, text, flags=re.S | re.I)
    return re.sub(r'<script\b(?![^>]*ld\+json)[^>]*>.*?</script>', blank, text, flags=re.S | re.I)

def _in_tag(raw, pos):
    """True when pos sits inside a tag (an alt, aria-label or data-tip
    attribute). Attribute text is not copy for any rule here: _flat() drops
    it, so the figure rules skip it too rather than screening text the rest
    of the file never sees."""
    return raw.rfind('<', 0, pos) > raw.rfind('>', 0, pos)

def _window_raw(text, pos, chars=1200):
    """(flattened copy around a raw position, index of the figure in it). The
    slice is cut on tag boundaries so a half tag never leaks attribute junk
    into the words."""
    lo = text.rfind('>', 0, max(0, pos - chars)) + 1
    hi = text.find('<', min(len(text), pos + chars))
    flat = html.unescape(_flat(text[lo:hi if hi != -1 else len(text)]))
    approx = len(html.unescape(_flat(text[lo:pos])))
    fig = html.unescape(_flat(text[pos:pos + 40])).split()[:1]
    idx = flat.find(fig[0], max(0, approx - 12)) if fig else approx
    return flat, (idx if idx != -1 else approx)

def _words_around(flat, idx, n=80):
    """(the n words either side of idx, idx within that slice)."""
    pre = flat[:idx].split()[-n:]
    post = flat[idx:].split()[:n]
    return ' '.join(pre + post), len(' '.join(pre)) + (1 if pre else 0)

_BLOCK_TAGS = r'p|h[1-6]|li|td|th|figcaption|div|blockquote|dd|dt|summary|section|article|caption'
def _block_sentence(raw, pos):
    """The sentence the figure sits in, scoped to its innermost BLOCK element
    so a stat card's label cannot run into the next card's copy. Falls back
    to 40 words either side (headers are ld+json and have no blocks)."""
    opens = list(re.finditer(r'<(?:' + _BLOCK_TAGS + r')\b[^>]*>', raw[:pos], re.I))
    close = re.search(r'</(?:' + _BLOCK_TAGS + r')>', raw[pos:], re.I)
    lo = opens[-1].end() if opens else max(0, pos - 600)
    hi = pos + close.start() if close else min(len(raw), pos + 600)
    flat = html.unescape(_flat(raw[lo:hi]))
    i = len(html.unescape(_flat(raw[lo:pos])))
    a = max((flat.rfind(c, 0, i) for c in '.!?'), default=-1) + 1
    b = min((x for x in (flat.find(c, i) for c in '.!?') if x != -1), default=len(flat))
    return ' '.join(flat[a:i].split()[-40:] + flat[i:b + 1].split()[:40])

# Attribution shapes, CASE-SENSITIVE on the name (a sentence-start "That is
# a ..." or "This ... client" is not a person): a capitalised name beside a
# role noun after a comma, a middle dot or a dash ("Dave, business owner",
# "Vincent · Registered Nurse", "Alo — Chief Technology Officer"), "Name is a
# <role>", or "Name, <age>". Names in _NONPERSON are copy, not people.
_NAME = r'([A-Z][a-z]{2,})(?:\s+[A-Z]\.|\s+[A-Z][a-z]+)?'
_ATTRIB_SHAPES = re.compile(
    _NAME + r'\s*(?:,|·|&middot;|&#183;|—|–|-)\s*(?:an?\s+|the\s+)?(?:[\w-]+\s+){0,3}?(?i:' + ROLE + r')\b'
    + '|' + _NAME + r'\s+(?:is|was)\s+an?\s+(?:[\w-]+\s+){0,2}?(?i:' + ROLE + r')\b'
    + '|' + _NAME + r'\s*(?:,|:)\s*\d{2}\b(?!\d|%|-)')

def _attributed_name(window, idx=0):
    """The individual a figure is attributed to, or None. Candidates are the
    consent-list names and the _ATTRIB_SHAPES names within the window; the
    nearest PRECEDING candidate within 12 words wins (a table row or a
    "Name: figure" caption puts the name first), else the nearest overall (a
    stat card puts the name after the figure). 'anonymised' when the copy
    says so and names nobody. Returned as the first name."""
    cands = [(m.start(), m.group(1)) for m in _CONSENT_RX.finditer(window)]
    for m in _ATTRIB_SHAPES.finditer(window):
        name = next(g for g in m.groups() if g)
        if name not in _NONPERSON: cands.append((m.start(), name))
    if not cands:
        return "anonymised" if re.search(r'\banonymi[sz]ed\b', window, re.I) else None
    before = [(idx - p, n) for p, n in cands if p < idx and len(window[p:idx].split()) <= 12]
    if before: return min(before)[1]
    return min((abs(p - idx), n) for p, n in cands)[1]

_CONSENT_DISPLAY = {n.split()[0]: n for n in CONSENT_LIST}
def _on_consent_list(name):
    return name.split()[0] in _CONSENT_FIRST

def attributed_outcome_conditions(text, page=None):
    """TIER 2 item 2a, conditions (3), (4), (5) and the consent list, on every
    attributed individual figure. Returns (line, client, condition, detail).
    Unattributed figures are TIER 1 item 2 / TIER 2 item 1 / item 2g territory
    and are not this rule's. Deduplicated on (line, client, condition)."""
    raw = _blank_noncopy(text); out = []; seen = set()
    for m in _FIGURE.finditer(raw):
        if _in_tag(raw, m.start()): continue
        w, idx = _window_raw(raw, m.start(), 700)
        w, idx = _words_around(w, idx)
        name = _attributed_name(w, idx)
        if name is None: continue
        name = _CONSENT_DISPLAY.get(name.split()[0], name.split()[0])
        line = raw[:m.start()].count('\n') + 1
        fig = html.unescape(_flat(m.group(0))).strip()
        sent = _block_sentence(raw, m.start())
        findings = []
        if not _on_consent_list(name):
            findings.append(("consent", f"'{name}' is not on the owner-attested consent list"))
        if re.search(_MINIMISER, sent, re.I):
            findings.append(("(3) elapsed time as fact", f"'{re.search(_MINIMISER, sent, re.I).group(0)}' beside '{fig}'"))
        surface = _norm(html.unescape(_flat(_surface(raw, m.start()))))
        if not _has_disclosure(surface, page):
            findings.append(("(4) verbatim disclosure", "disclosure missing or not verbatim on the surface"))
        for rx, what in ((_SECOND_PERSON, "second person"), (_FIRST_PERSON, "first person"),
                         (_PROJECTION, "projection"), (_PRESENT_TENSE, "present tense")):
            h = re.search(rx, sent, 0 if rx is _FIRST_PERSON else re.I)
            if h:
                findings.append(("(5) third person, past tense", f"{what}: '{h.group(0)}' in the figure's sentence"))
        for cond, detail in findings:
            key = (line, name, cond)
            if key in seen: continue
            seen.add(key)
            out.append((line, name, cond, f"{detail}  …{sent[:110]}…"))
    return out

# ─── TIER 2 item 2g - data-backed figures ─────────────────────────
# Every client-results number must either appear on /outcomes or meet 2a. A
# figure attributed to an individual is 2a's; this rule takes the rest: a
# figure framed as a recorded aggregate client result (a past-tense result
# verb or a statistic word beside a client word) must be on /outcomes. Goals
# ("want to lose 20-30 lbs", TIER 2 item 3), published-trial figures and
# labelled illustrative samples are not client results. Adherence
# percentages are findings on sight until attendance is logged.
OUTCOMES_PAGE = "pages/outcomes.html"
_RESULT_VERB = (r'\b(?:lost|gained|dropped|shed|added|achieved|rose|fell|reached|recorded|measured|'
                r'stronger|improved|increased|decreased|reduced|median|average[ds]?|mean|'
                r'fully or partly|retention)\b')
# "members" is a gym word, not an OmniFit one: "80% of members quit by month
# 3" on the comparison table is a big-box statistic, not a client result.
_CLIENT_WORD = r'\b(?:clients?|client base|of those|cohort)\b'
_GOAL_FRAME  = r'\b(?:wants?|wanted|needs?|looking|aim\w*|goal\w*|target\w*)\s+(?:to\s+)?(?:\w+\s+){0,3}$'
_TRIAL_WORDS = r'\b(?:trial|trials|study|studies|published|research|participants|DXA|meta-analysis)\b'
_ADHERENCE   = r'\b(?:adherence|attendance|sessions?\s+completed|completion rate)\b'

_outcomes_cache = {}
def _outcomes_text(override=None):
    if override is not None: return override
    if "flat" not in _outcomes_cache:
        try: raw = open(OUTCOMES_PAGE).read()
        except OSError: raw = ""
        _outcomes_cache["raw"] = raw
        _outcomes_cache["flat"] = html.unescape(_flat(raw))
    return _outcomes_cache["flat"]

_DATE_RANGE = (r'\b(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\s+(?:to|through|–|-)\s+'
               r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}'
               r'|between\s+(?:\w+\s+)?\d{4}\s+and\s+(?:\w+\s+)?\d{4}|\b\d{4}\s+to\s+\d{4})\b')

def _figure_rx(fig):
    """A regex for the same figure in any of its spellings: sign dropped,
    lb/lbs/pounds and in/inch/inches unified, thousands commas kept."""
    f = html.unescape(fig)
    num = re.search(r'\d[\d.,]*', f)
    if not num: return None
    n = re.escape(num.group(0).rstrip('.,'))
    if '%' in f:                                   return re.compile(r'(?<![\d.])' + n + r'\s*%')
    if re.search(r'lb|pound', f, re.I):            return re.compile(r'(?<![\d.])' + n + r'\s*(?:lbs?|pounds?)\b', re.I)
    if re.search(r'\binch|\bin\b', f, re.I):       return re.compile(r'(?<![\d.])' + n + r'\s*(?:in|inch|inches)\b', re.I)
    return re.compile(r'(?<![\d.])' + n + r'(?![\d.])')

def _published_on_outcomes(fig, outcomes=None):
    """True when the figure appears on /outcomes at all (item 2g's test)."""
    rx = _figure_rx(fig)
    return bool(rx and rx.search(_outcomes_text(outcomes)))

def _published_with_method(fig, outcomes=None):
    """TIER 1 item 2 carve-out: the figure appears on /outcomes AND its surface
    there carries a sample size AND the page carries a date range. Surface =
    the enclosing <section> of the first occurrence, falling back to the page;
    the date range is accepted page-wide because /outcomes states it once in
    its meta line for every section below."""
    if outcomes is None:
        _outcomes_text(); raw = _outcomes_cache["raw"]
    else:
        raw = outcomes
    rx = _figure_rx(fig)
    if not rx: return False
    blanked = _blank_noncopy(raw)
    hit = rx.search(blanked)
    if not hit: return False
    surface = html.unescape(_flat(_surface(blanked, hit.start())))
    return bool(re.search(_C_SAMPLE, surface, re.I) and re.search(_DATE_RANGE, html.unescape(_flat(raw)), re.I))

def data_backed_figures(text, outcomes=None):
    """TIER 2 item 2g on one file: (line, figure, kind, detail)."""
    raw = _blank_noncopy(text); out = []; seen = set()
    for m in _FIGURE.finditer(raw):
        if _in_tag(raw, m.start()): continue
        w, idx = _window_raw(raw, m.start(), 700)
        w, idx = _words_around(w, idx)
        fig = html.unescape(_flat(m.group(0))).strip()
        line = raw[:m.start()].count('\n') + 1
        surface = _surface(raw, m.start())
        if _is_illustrative(surface): continue                       # TIER 2 item 5
        before = ' '.join(w[:idx].split()[-20:])
        after  = ' '.join(w[idx:].split()[:20])
        local = before + ' ' + after
        if '%' in fig and re.search(_ADHERENCE, local, re.I):
            key = (line, fig, "adherence")
            if key not in seen:
                seen.add(key); out.append((line, fig, "adherence percentage", "no adherence % until attendance is logged"))
            continue
        if _attributed_name(w, idx) is not None: continue            # item 2a's
        if re.search(_TRIAL_WORDS, local, re.I): continue             # not an OmniFit client result
        if re.search(_GOAL_FRAME, before, re.I) or re.match(r'\s*(?:\w+\s+){0,2}to\s+(?:lose|drop|gain)\b', after[len(fig):], re.I):
            continue                                                  # a goal, TIER 2 item 3
        if not (re.search(_CLIENT_WORD, local, re.I) and re.search(_RESULT_VERB, local, re.I)): continue
        if _published_on_outcomes(fig, outcomes): continue
        key = (line, fig, "2g")
        if key in seen: continue
        seen.add(key)
        out.append((line, fig, "not on /outcomes", f"aggregate client figure absent from /outcomes  …{local[:110]}…"))
    return out

def _selftest_amendment():
    """Both directions, every run, for every condition the amendment encodes."""
    D = '<p>' + DISCLOSURE_2A + '</p>'
    ok = '<section><p>Alo S., CTO, added 18 lbs of lean muscle between June 2023 and June 2024.</p>' + D + '</section>'
    assert attributed_outcome_conditions(ok) == [], "compliant 2a card reported: %r" % attributed_outcome_conditions(ok)
    linked = ('<section><p>Vincent, a registered nurse, dropped 8% body fat from March 2025 to March 2026.</p>'
              '<p>Individual result, measured by OmniFit. How clients typically progress: '
              '<a href="/outcomes">omnifittraining.com/outcomes</a>.</p></section>')
    assert attributed_outcome_conditions(linked) == [], "link-wrapped disclosure not accepted"
    conds = lambda t: {c for _, _, c, _ in attributed_outcome_conditions(t)}
    assert "(3) elapsed time as fact" in conds('<section><p>Alo S., CTO, added 18 lbs in just 6 months.</p>' + D + '</section>'), "'in just' not caught"
    assert conds('<section><p>Alo S., CTO, added 18 lbs over 6 months.</p>' + D + '</section>') == set(), "'over 6 months' flagged"
    assert "(4) verbatim disclosure" in conds('<section><p>Alo S., CTO, added 18 lbs over 6 months.</p><p>Individual result, measured by OmniFit; see aggregate outcomes above.</p></section>'), "near-verbatim disclosure accepted"
    assert "(4) verbatim disclosure" in conds('<section><p>Alo S., CTO, added 18 lbs over 6 months.</p></section>' + D), "disclosure on another surface accepted"
    for bad in ('Alo S., CTO, added 18 lbs; you can too.', 'Alo S., CTO: "I added 18 lbs."',
                'Alo S., CTO, will add 18 lbs.', 'Alo S., CTO, gains 18 lbs every year.'):
        assert "(5) third person, past tense" in conds('<section><p>' + bad + '</p>' + D + '</section>'), f"(5) missed: {bad}"
    # Dave joined the consent list Oct 17 2026; the negative case needs a name that is not on it
    assert "consent" in conds('<section><p>Marco, business owner, lost 27 lbs over 8 months.</p>' + D + '</section>'), "unlisted name passed consent"
    assert "consent" in conds('<section><p>An anonymised male client, 29, gained 10 lb over 12 weeks.</p>' + D + '</section>'), "anonymised profile passed consent"
    assert "consent" not in conds('<section><p>Ken · CTO · 50s</p><div>−11 lb bodyweight, 6 months</div>' + D + '</section>'), "listed name failed consent"
    assert attributed_outcome_conditions('<section><p>Clients lose 20 lbs in 6 months.</p></section>') == [], "unattributed figure read as 2a"
    assert "consent" not in conds('<section><p>Dave R., business owner, lost 27 lbs over 8 months.</p>' + D + '</section>'), "Dave R. (consent list, Oct 17 2026) failed consent"
    # /outcomes exemption: the first sentence alone, on that page only, both ways
    card = '<section><p>Isaac M., attorney, went from 28.2% to 19.8% body fat between 2024 and 2025.</p>'
    short = '<p>' + DISCLOSURE_2A_OUTCOMES + '</p></section>'
    oc = lambda t, pg: {c for _, _, c, _ in attributed_outcome_conditions(t, pg)}
    assert oc(card + short, "outcomes.html") == set(), "/outcomes short disclosure not accepted on /outcomes"
    assert oc(card + short, "outcomes-header.html") == set(), "/outcomes short disclosure not accepted in its header"
    assert "(4) verbatim disclosure" in oc(card + short, "weight-loss.html"), "short disclosure accepted off /outcomes"
    assert "(4) verbatim disclosure" in oc(card + short, None), "short disclosure accepted with no page"
    assert "(4) verbatim disclosure" in oc(card + D + '</section>', "outcomes.html"), "full disclosure accepted on /outcomes (the exemption is the first sentence alone)"
    assert oc(card + D + '</section>', "weight-loss.html") == set(), "full disclosure rejected off /outcomes"
    assert "(4) verbatim disclosure" in oc(card + '<p>Individual result, measured by OmniFit; see aggregate outcomes above.</p></section>', "outcomes.html"), "near-verbatim short disclosure accepted on /outcomes"
    assert "(4) verbatim disclosure" in oc(card + '</section>' + short.replace('</section>', ''), "outcomes.html"), "short disclosure on another surface accepted on /outcomes"
    # the 2a disclosure's "typically" is not T2-1 aggregate framing; any other "typically" still is
    vin = '<div><div>−8% body fat</div><div>Vincent · Registered Nurse · Age 59</div></div>'
    assert aggregate_metric_conditions(vin + '<p>Individual result, measured by OmniFit. How clients typically progress: <a href="/outcomes">omnifittraining.com/outcomes</a>.</p>') == [], "2a disclosure read as T2-1 aggregate framing"
    assert aggregate_metric_conditions(vin + '<p>Clients typically see this.</p>'), "'typically' beside a figure stopped reading as aggregate"
    # 2g
    syn = ('<section><p>Between January 2023 and September 2026, 72 clients. Median strength change +13.7% across 38 clients. '
           'Clients lost 40 lb in 6 months (n=47).</p></section>')
    kinds = lambda t, o: {k for _, _, k, _ in data_backed_figures(t, o)}
    assert "not on /outcomes" in kinds('<section><p>Our clients lost a median 9 lb over 12 weeks.</p></section>', syn), "off-outcomes aggregate passed"
    assert kinds('<section><p>Our clients lost a median 40 lb over 12 weeks.</p></section>', syn) == set(), "on-outcomes aggregate flagged"
    assert kinds('<section><p>Designed for professionals who want to lose 20–30 pounds. The typical client is 45.</p></section>', syn) == set(), "persona goal flagged (TIER 2 item 3)"
    assert kinds('<section><p>In the STEP-1 trial, 45.2% of weight lost by participants was lean mass.</p></section>', syn) == set(), "trial figure flagged"
    assert "adherence percentage" in kinds('<section><p>Session adherence across clients: 94%.</p></section>', syn), "adherence % passed"
    assert kinds('<section><p>Session adherence 94%.</p><p>Illustrative example, not client data.</p></section>', syn) == set(), "illustrative adherence flagged"
    assert kinds('<section><p>Alo S., CTO, added 18 lbs over 6 months.</p></section>', syn) == set(), "attributed figure read as 2g"
    # TIER 1 item 2 carve-out
    agg = '<p>Clients lose 40 lb in 6 months.</p>'
    assert lbs_near_timeframe(agg), "aggregate-with-timeframe stopped firing"
    assert lbs_near_timeframe(agg, outcomes='<p>nothing here</p>'), "carve-out fired with the figure absent from /outcomes"
    assert lbs_near_timeframe(agg, outcomes='<section><p>Clients lost 40 lb (n=47).</p></section>'), "carve-out fired with no date range"
    assert lbs_near_timeframe(agg, outcomes='<section><p>January 2023 to September 2026: clients lost 40 lb.</p></section>'), "carve-out fired with no sample size"
    assert lbs_near_timeframe(agg, outcomes=syn) == [], "published aggregate still fired"

# ─── POSITIONING LINE (CANON ENTITY BLOCK, Oct 17 2026) ───────────
# Wherever the line appears it is verbatim, and it never sits in a title, a
# meta description or an H1 (build.py reads a header's WebPage name and
# description as the title and meta). Keyed on two fragments no other copy
# uses, so a paraphrase that keeps either is a finding and the DESCRIPTION's
# "diagnostic-led personal training practice" is not.
POSITIONING_LINE = ("OmniFit Performance is a diagnostic-led coaching system that takes busy "
                    "professionals over 30 from pain or plateau to lasting, independent strength.")
_POS_ANCHORS = re.compile(r'diagnostic-led coaching system|pain or plateau', re.I)

def positioning_line_verbatim(text):
    """(kind, ctx): 'not verbatim' for a variant, 'in title/meta/H1' for a
    placement CANON bans. The line in an ld+json slogan or a summary block is
    the intended use and is quiet."""
    out = []; last = -10**9
    flat = _norm(html.unescape(_flat(text)))
    for m in _POS_ANCHORS.finditer(flat):
        near = flat[max(0, m.start() - 220):m.end() + 220]
        if POSITIONING_LINE not in near and m.start() - last > 220:   # one finding per sentence
            out.append(("positioning line not verbatim", flat[max(0, m.start() - 90):m.end() + 110].strip()))
            last = m.start()
    for tag in ("title", "h1"):
        for m in re.finditer(r'<' + tag + r'\b[^>]*>(.*?)</' + tag + r'>', text, re.S | re.I):
            if _POS_ANCHORS.search(_flat(m.group(1))):
                out.append((f"positioning line in <{tag}>", _flat(m.group(1))[:120]))
    for m in re.finditer(r'<meta\b[^>]*name="description"[^>]*content="([^"]*)"', text, re.I):
        if _POS_ANCHORS.search(m.group(1)):
            out.append(("positioning line in meta description", m.group(1)[:120]))
    for m in _LDJSON.finditer(text):
        try: doc = json.loads(m.group(1))
        except ValueError: continue
        nodes = doc.get("@graph", [doc]) if isinstance(doc, dict) else doc
        for n in nodes if isinstance(nodes, list) else []:
            if isinstance(n, dict) and n.get("@type") in PAGE_TYPES:
                for k in ("name", "description"):
                    if _POS_ANCHORS.search(str(n.get(k, ""))):
                        out.append((f"positioning line in WebPage {k} (the page title/meta)", str(n.get(k))[:120]))
    return out

def _selftest_positioning():
    kinds = lambda t: [k for k, _ in positioning_line_verbatim(t)]
    assert kinds('<p>' + POSITIONING_LINE + '</p>') == [], "verbatim line flagged"
    assert kinds('<p>Summary: ' + POSITIONING_LINE + ' Book a consultation.</p>') == [], "verbatim line in a summary flagged"
    assert kinds('<script type="application/ld+json">{"@graph":[{"@type":"Organization","slogan":"' + POSITIONING_LINE + '"}]}</script>') == [], "slogan flagged"
    assert kinds('<p>OmniFit Performance is a diagnostic-led coaching system for busy professionals.</p>') == ["positioning line not verbatim"], "paraphrase passed"
    assert kinds('<p>We take you from pain or plateau to strength.</p>') == ["positioning line not verbatim"], "second-anchor paraphrase passed"
    assert kinds('<p>OmniFit Performance is the diagnostic-led personal training practice of Nemezio LopezPerez.</p>') == [], "DESCRIPTION flagged"
    assert "positioning line in <h1>" in kinds('<h1>' + POSITIONING_LINE + '</h1>'), "H1 placement passed"
    assert "positioning line in <title>" in kinds('<title>' + POSITIONING_LINE + '</title>'), "title placement passed"
    assert "positioning line in meta description" in kinds('<meta name="description" content="' + POSITIONING_LINE + '">'), "meta placement passed"
    assert any(k.startswith("positioning line in WebPage") for k in kinds(
        '<script type="application/ld+json">{"@graph":[{"@type":"WebPage","description":"' + POSITIONING_LINE + '"}]}</script>')), "WebPage description passed"

# ─── THE TRAVEL PROTOCOL (CANON, THE OMNIFIT METHOD, Oct 17 2026) ─
# Always "the Travel Protocol" (capital T and P); never a price for it. The
# name went live on the travel-support pages Oct 17 2026 (follow-up run).
def travel_protocol_usage(text):
    t = html.unescape(_flat(text)); out = []
    for m in re.finditer(r'\btravel protocol\b', t, re.I):
        if m.group(0) != "Travel Protocol":
            out.append(("Travel Protocol casing", t[max(0, m.start()-40):m.end()+40].strip()))
    # The price test reads the name's sentence INSIDE its block element
    # (_block_sentence, as 2a condition 5 does). Splitting on punctuation alone
    # ran an unpunctuated <li> back into the price paragraph above its list
    # (omnifit-vs-competitors, Oct 17 2026), which states the tier rates, not
    # a price for the Travel Protocol.
    raw = _blank_noncopy(text)
    for m in re.finditer(r'\btravel protocol\b', raw, re.I):
        if _in_tag(raw, m.start()): continue
        sent = _block_sentence(raw, m.start())
        if re.search(r'\$\s*\d', sent):
            out.append(("price stated for the Travel Protocol", sent.strip()[:140]))
    return out

def _selftest_travel_protocol():
    kinds = lambda t: [k for k, _ in travel_protocol_usage(t)]
    assert kinds('<p>Included in every tier: the Travel Protocol.</p>') == [], "canonical casing flagged"
    assert kinds('<p>Ask about the travel protocol.</p>') == ["Travel Protocol casing"], "lower-case passed"
    assert kinds('<p>The Travel protocol is included.</p>') == ["Travel Protocol casing"], "mixed case passed"
    assert kinds('<p>The Travel Protocol is $95 per trip.</p>') == ["price stated for the Travel Protocol"], "price passed"
    assert kinds('<p>Travel Protocols are included.</p>') == [], "plural word-boundary false positive"
    assert kinds('<p><strong>$640 per 4 weeks</strong> depending on setting</p><ul><li>App logging</li>'
                 '<li>The Travel Protocol: a scheduled session live by video, at no extra cost</li></ul>') == [], "price in the block above the list read as the Travel Protocol's"
    assert kinds('<ul><li>The Travel Protocol, $95 per trip</li></ul>') == ["price stated for the Travel Protocol"], "price in the same list item passed"

# ─── TEQNEEQ HAS NO ON-SITE PT CLINIC (CANON ENTITY BLOCK, Oct 17 2026) ─
# Owner, homepage rebuild run: Teqneeq is a members-only functional health
# facility; OmniFit's physical therapy relationships are EXTERNAL partners
# (e.g. Stoke Physical Therapy). A sentence naming Teqneeq - or the sentence
# right after it - that places a PT / physical therapy / rehab clinic on site
# or in-house is a finding. Negations ("has no on-site physical therapy
# clinic") are the canonical correction and pass.
_TEQ_PT_CLAIM = re.compile(
    r'\b(?:on[- ]?site|in[- ]house)\s+(?:physical[- ]therap\w*|PT|rehab\w*)\b'
    r'|\b(?:physical[- ]therap\w*|PT|rehab\w*)\s+(?:clinic|practice|department|team)s?\s+'
    r'(?:on[- ]?site|in[- ]house|inside|within|under one roof|in the building)'
    r'|\b(?:integrat\w*|hous\w*|includ\w*|has|have|with|offers?)\s+(?:\w+\s+){0,4}?'
    r'(?:physical[- ]therap\w*|PT|rehab\w*)\s+clinics?\b', re.I)
_TEQ_PT_NEG = re.compile(r"\b(?:no|not|never|without|isn't|doesn't|has no)\b(?:\s+\S+){0,5}\s*$", re.I)

def teqneeq_onsite_pt(text):
    t = html.unescape(_flat(text)); out = []
    sents = re.split(r'(?<=[.!?])\s+', t)
    for i, s in enumerate(sents):
        if not re.search(r'\bteqneeq\b', s, re.I): continue
        for cand in sents[i:i + 2]:
            for m in _TEQ_PT_CLAIM.finditer(cand):
                if _TEQ_PT_NEG.search(cand[:m.start()]): continue
                out.append(("on-site PT clinic claimed at Teqneeq", cand.strip()[:160]))
    return list(dict.fromkeys(out))

def _selftest_teqneeq_pt():
    kinds = lambda t: [k for k, _ in teqneeq_onsite_pt(t)]
    bad = "on-site PT clinic claimed at Teqneeq"
    assert kinds('<p>Teqneeq is a members-only facility in 4S Ranch that integrates training with an on-site physical therapy clinic.</p>') == [bad], "integrated on-site PT clinic passed"
    assert kinds('<p>We train at Teqneeq. It houses a physical therapy clinic.</p>') == [bad], "PT clinic in the next sentence passed"
    assert kinds('<p>Teqneeq has a PT clinic on site.</p>') == [bad], "'PT clinic on site' passed"
    assert kinds('<p>Teqneeq offers in-house rehab and recovery.</p>') == [bad], "in-house rehab passed"
    assert kinds('<p>Teqneeq has no on-site physical therapy clinic.</p>') == [], "canonical negation flagged"
    assert kinds('<p>Teqneeq is a members-only functional health facility. We coordinate with Stoke Physical Therapy, an external partner.</p>') == [], "external PT partner flagged"
    assert kinds('<p>An on-site physical therapy clinic is common in big gyms. Teqneeq is in 4S Ranch.</p>') == [], "claim in the sentence BEFORE Teqneeq read as about Teqneeq"

# ─── COACHING TENURE (CANON ENTITY BLOCK, Oct 18 2026) ──────────────────
# Owner fact, final-cleanup run: Nemezio started coaching in 2016, as a hobby
# before turning professional. Never claim a specific number of professional
# years. A sentence carrying "10+ years", "over/more than a decade" or
# "over/more than ten years" beside a coaching / experience / helping /
# training word is a finding. A sentence naming a partner or another
# practitioner (Celeste Esposito's "nearly a decade of clinical bodywork",
# Dr. Damien Jackson-Ricketts, Stoke, a therapist) is not about Nemezio and
# passes. Stat badges flatten into one run of text ("10+ Years Coaching"), so
# they are caught as well.
_TENURE_CLAIM = re.compile(
    r'\b(?:10|ten)\s*\+\s*(?:years?|yrs)\b'
    r'|\b(?:over|more\s+than)\s+(?:a|one)\s+decade\b'
    r'|\b(?:over|more\s+than)\s+(?:10|ten)\s+(?:years?|yrs)\b', re.I)
_TENURE_CTX = re.compile(r'\b(?:coach\w*|experience\w*|help\w*|train\w*)\b', re.I)
_TENURE_THIRD = re.compile(r'\b(?:Celeste|Esposito|Serenity|Damien|Jackson-Ricketts|Stoke|therapist\w*|Dr\.)', re.I)

def coaching_tenure_claim(text):
    t = html.unescape(_flat(text)); out = []
    for sent in re.split(r'(?<=[.!?])\s+', t):
        m = _TENURE_CLAIM.search(sent)
        if m and _TENURE_CTX.search(sent) and not _TENURE_THIRD.search(sent):
            out.append((m.group(0), sent.strip()[:160]))
    return list(dict.fromkeys(out))

def _selftest_coaching_tenure():
    hits = lambda t: [h for h, _ in coaching_tenure_claim(t)]
    assert hits('<p>He has coached for over ten years and holds 190+ reviews.</p>'), "'coached for over ten years' passed"
    assert hits('<div class="stat"><div class="num">10+</div><div class="lbl">Years Coaching</div></div>'), "'10+ Years Coaching' badge passed"
    assert hits("<p>I've spent over a decade helping busy professionals rebuild their bodies.</p>"), "'over a decade helping' passed"
    assert hits('<p>He holds NASM credentials, with 10+ years of coaching experience.</p>'), "'10+ years of coaching experience' passed"
    assert hits('<p>Coaching since 2016 (hobby, then professional).</p>') == [], "'coaching since 2016' flagged"
    assert hits('<p>Celeste is a Licensed Massage Therapist with over a decade of clinical bodywork experience.</p>') == [], "a partner's experience flagged"
    assert hits('<p>Over a decade of desk work leaves the hips tight.</p>') == [], "a decade of desk work (no coaching claim) flagged"

# ─── PLACEHOLDER COPY (Oct 18 2026, external audit item 10) ─────────
# A build placeholder left in VISIBLE copy - "[CASE STUDY SUMMARY: ...]",
# an "Add Image" photo-slot label, "TODO", or a "[" followed by all-caps
# placeholder text ("[CLIENT NAME]", "[INSERT LINK") - is BROKEN STRUCTURE
# (c): the page is unfinished, which is neither a compliance strike nor a
# stale fact. Read on the flattened copy (_flat), so HTML comments, <style>,
# executable <script> and tag attributes are not copy; ld+json IS copy (a
# placeholder in schema is published too). Every file in the glob, frozen
# records INCLUDED: an "Add Image" span is no measurement. Self-tested both
# ways (_selftest_placeholder).
_PLACEHOLDER = re.compile(
    r'\[\s*CASE STUDY'
    r'|\b(?i:add image)\b'
    r'|\bTODO\b'
    r'|\[\s*[A-Z]{2,}(?:[\s_:/&\'.,-]+[A-Z0-9]+)*(?:\]|:|\s|$)')

def placeholder_copy(text):
    t = html.unescape(_flat(text)); out = []
    for m in _PLACEHOLDER.finditer(t):
        out.append((m.group(0).strip(), t[max(0, m.start()-50):m.end()+60]))
    return list(dict.fromkeys(out))

def _selftest_placeholder():
    hits = lambda t: [h for h, _ in placeholder_copy(t)]
    for bad in ('<div class="gq-block">[CASE STUDY SUMMARY: starting diagnostic, rescan data.]</div>',
                '<div class="photo-placeholder"><span>Add Image</span></div>',
                '<p>TODO: write this section</p>', '<p>Hello [CLIENT NAME], welcome.</p>',
                '<p>See [INSERT LINK HERE] for details.</p>',
                '<script type="application/ld+json">{"name": "[PAGE TITLE]"}</script>'):
        assert hits(bad), f"placeholder passed: {bad}"
    for ok in ('<!-- [CASE STUDY SUMMARY: hidden in a comment] TODO -->',
               '<style>#x [data-tag="a"] { color: red; } /* TODO */</style>',
               '<script>var a = [1, 2]; // TODO</script>',
               '<img alt="Add Image" src="a.jpg">', '<p>Results [n=47], measured by OmniFit.</p>',
               '<p>Mark came in at 248 lbs [weighed on the Bodystat].</p>', '<p>Add images of your space to the app.</p>',
               '<script type="application/ld+json">{"knowsAbout": ["NASM CPT", "ACE"]}</script>'):
        assert hits(ok) == [], f"legitimate copy flagged: {ok} -> {hits(ok)}"

# ─── RETIRED SERVICE AREAS (Oct 19 2026) ────────────────────────────
# The Pacific Beach studio era is history (CANON NAP), and so are the beach
# neighbourhoods it served. BANNED caught "Pacific Beach" but nothing else:
# weight-loss carried "Serving PB, Mission Bay, OB, La Jolla" past every run.
# "Mission Bay" and "Ocean Beach" are matched in any casing; the abbreviations
# PB and OB as whole words and case-SENSITIVELY, so "pb" in a slug, "PBS" or
# "OBJECTIVE" is not an area name. VISIBLE PAGE TEXT ONLY: HTML comments,
# <style>, executable <script>, every tag and its attributes (href, src, alt)
# and URLs written out in copy or ld+json are blanked first, positions kept so
# a hit reports its line. _redirects, REPORT.md and archive/ are never read:
# a 301 from /personal-trainer-mission-bay is how a retired URL stays retired.
# Every file in the glob, frozen records INCLUDED. Self-tested both ways
# (_selftest_retired_service_area).
_RETIRED_AREA = re.compile(r'(?i:\bmission(?:\s|&nbsp;|&#160;)+bay\b|\bocean(?:\s|&nbsp;|&#160;)+beach\b)'
                           r'|\bPB\b|\bOB\b')
_URL = re.compile(r'(?:https?://|www\.)[^\s"\'<>]+|(?<![\w/])/[a-z0-9][\w\-./?#=&%]*')
_AREA_SKIP = ("_redirects", "REPORT.md")

def _area_skipped(path):
    p = path.replace(os.sep, '/')
    return os.path.basename(p) in _AREA_SKIP or p.startswith('archive/') or '/archive/' in p

def retired_service_area(text, path=""):
    if _area_skipped(path): return []
    blank = lambda m: re.sub(r'[^\n]', ' ', m.group(0))
    t = _blank_noncopy(text)
    t = re.sub(r'<[^>]*>', blank, t)
    t = _URL.sub(blank, t)
    out = []
    for m in _RETIRED_AREA.finditer(t):
        ln = t.count('\n', 0, m.start()) + 1
        out.append((re.sub(r'(?:\s|&nbsp;|&#160;)+', ' ', m.group(0)), ln,
                    re.sub(r'\s+', ' ', t[max(0, m.start()-50):m.end()+50]).strip()))
    return out

def _selftest_retired_service_area():
    hits = lambda t, p="pages/fixture.html": [h for h, _, _ in retired_service_area(t, p)]
    assert hits('<ul><li>Serving PB, Mission Bay</li></ul>') == ["PB", "Mission Bay"], "'Serving PB, Mission Bay' passed"
    assert hits('<p>Clients from OB and Ocean Beach.</p>') == ["OB", "Ocean Beach"], "OB / Ocean Beach passed"
    assert hits('<p>Serving PB/OB.</p>') == ["PB", "OB"], "'PB/OB' passed"
    assert hits('<p>Near mission\n  bay.</p>') == ["mission bay"], "lower-case Mission Bay across a line break passed"
    assert hits('<script type="application/ld+json">{"areaServed": "Mission Bay"}</script>'), "Mission Bay in ld+json passed"
    assert hits('/personal-trainer-mission-bay  /personal-trainer-la-jolla  301', "public/_redirects") == [], "_redirects was read"
    assert hits('/personal-trainer-mission-bay  /  301', "_redirects") == [], "_redirects was read"
    assert hits('Serving PB, Mission Bay', "REPORT.md") == [] and hits('Serving PB', "archive/old.html") == [], "REPORT.md / archive/ was read"
    for ok in ('<!-- Serving PB, Mission Bay, OB -->', '<a href="/personal-trainer-mission-bay">La Jolla</a>',
               '<img src="/img/ocean-beach.jpg" alt="Mission Bay view">', '<p>See https://example.com/Mission Bay</p>',
               '<p>Watch it on PBS. Our OBJECTIVE is a pb-free slug.</p>', '<p>pb and ob in lower case</p>',
               '<style>/* PB */</style><script>var OB = 1;</script>'):
        assert hits(ok) == [], f"non-copy flagged: {ok} -> {hits(ok)}"

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

# TIER 2 item 2a: historical records, exempt from re-screening ENTIRELY. They
# record measurements that happened; re-screening them would put the run in the
# position of arguing with its own archive.
# home-3.html left this list in the homepage rebuild (Oct 17 2026): it is no
# longer a copy of the case-studies record but three short homepage case
# cards, screened like every other page (CANON REPO STATE).
FROZEN = ("case-studies.html",)

# ─── (b) stale canon ───────────────────────────────────────────────
# ─── (b) stale canon, OCTOBER 2026 CARD ────────────────────────────
# The signal INVERTED on Sept 13 2026. August prices were canonical; they are
# now the stale-canon marker, and October prices are canonical. Two figures
# changed sides and had to be REMOVED from this list rather than added to it:
#   $90   was the retired name-era assessment price. It is now the October
#         guest add-on, canonical in that meaning.
#   $275  was an August month-to-month rate. It is now the October in-home
#         single session.
# $500/mo was banned as Executive Hybrid; the Reset Gold tier is now $500, so
# the figure is dropped here and Executive Hybrid stays caught by its name.
# Banning a bare figure is only safe when it appears in NO October product.
# The safe set was computed by differencing the two blocks in CANON, not by
# reading them - the collision list ($150 $160 $200 $210 $235 $250 $275 $295
# $325 $500 $750 $90 $1,100 $1,250 $3,300 $3,750) is too easy to get wrong by
# eye, and every entry on it would have been a false positive on live copy.
BANNED = ["OmniFit Personal Fitness Training", "Pacific Beach", "ACE OES",
          "Orthopedic Exercise", "Executive Hybrid", "Lopez Perez", "180+",
          "$225", "$299", "$599",
          # RETIRED PRODUCT NAME. The October card calls it the Performance
          # ASSESSMENT; "Performance Diagnostic" was the August name and was
          # left behind on ~28 files by the repricing, which changed figures
          # without touching the product name. Banned so it cannot come back.
          "Performance Diagnostic",
          # BILLING CADENCE. Every OmniFit product bills every 4 weeks - the
          # Program, the Executive Reset and the Tune-Up alike. Nothing bills
          # monthly and there is no month-to-month option, so both phrases are
          # retired from public copy. CANON TERMS carries the rule.
          # NOT banned, deliberately: "per month" and "monthly" on their own.
          # The Teqneeq membership genuinely is $119 per month (Teqneeq's
          # billing, not OmniFit's), and "monthly progress reports" is a
          # cadence, not a billing term. Banning the bare words would flag
          # roughly 150 correct lines.
          "month-to-month", "billed monthly",
          # RETIRED PRODUCT NAME. The product is the "Tune-Up". The old name
          # asserted monthly billing that no longer exists. The LEGACY block in
          # CANON still carries it correctly and is out of this glob's reach.
          "Monthly Tune-Up",
          # August 2026 ladders - retired by the October card.
          # $140 is NOT here (Oct 17 2026): it is the August 10-pack rung, but
          # it is also the Foundation per-session rate (560 / 4), which the
          # rates page now states in static text. Caught by retired_pack_rate
          # below in its August MEANING only - the way $150 is handled.
          "$110", "$115", "$135", "$145", "$155", "$165", "$170",
          "$175", "$195", "$199", "$290", "$335", "$370", "$390", "$449", "$455",
          "$475", "$510", "$550", "$625", "$650", "$675", "$700", "$725",
          "$755", "$875", "$950", "$975", "$995",
          # August add-ons: guest 75 (now 90), referral credit 50
          # $75 is NOT here (Audit Reconciliation run, Oct 18 2026): it is the
          # Virtual Performance Assessment price (CANON CANONICAL FACTS). It
          # stays banned in its August MEANINGS (guest add-on, travel fee) via
          # retired_75 below, which reads context the way retired_pack_rate
          # does for $140.
          "$50",
          "$1,005", "$1,395", "$1,400", "$1,425", "$1,625", "$1,700",
          "$1,725", "$1,860", "$1,950", "$2,150", "$2,700", "$2,850",
          "$4,185", "$5,175", "$5,580"]

# TIER NAMES. "Essential" is unlisted on the October card - graduates and case
# by case only - so it must not appear in public copy. Matched with word
# boundaries and case-sensitively on the capitalised tier name, so "essential"
# as an ordinary adjective ("essential movement patterns") is not a finding.
BANNED_TIERS = ["Essential"]

# CANCELLATION LANGUAGE. The card's rule is "no exit fees". "non-refundable"
# is the one exception and only in its own place: the Foundation policy
# sentence, which says the Foundation is non-refundable and names the 30-Day
# Fit Guarantee as the only exit. That sentence is the negative test.
FEE_TERMS = ["exit fee", "exit fees", "cancellation fee", "cancellation fees",
             "non-refundable", "nonrefundable"]
FOUNDATION_POLICY = re.compile(
    r'non-?refundable[^.]{0,200}?30-Day Fit Guarantee'
    r'|30-Day Fit Guarantee[^.]{0,200}?non-?refundable'
    r'|Foundation[^.]{0,120}?non-?refundable', re.I)

def fee_language(text):
    """'exit fee', 'cancellation fee' and 'non-refundable' are flagged EXCEPT
    inside the Foundation policy sentence. Scoped to the sentence, not the
    page: a Foundation policy elsewhere on the page must not license an exit
    fee in the terms block."""
    t = _flat(text); out = []
    for term in FEE_TERMS:
        for m in re.finditer(re.escape(term), t, re.I):
            lo = max((t.rfind(c, 0, m.start()) for c in '.!?'), default=-1) + 1
            hi = min((x for x in (t.find(c, m.end()) for c in '.!?') if x != -1), default=len(t))
            sentence = t[lo:hi + 1]
            if FOUNDATION_POLICY.search(sentence): continue
            out.append((term, sentence.strip()))
    return out

# ─── (b) RETIRED LAUNCH COPY (owner decisions, Oct 17 2026) ────────
# Literal phrases the launch batch retired. Each is a claim or a surface the
# October 2026 owner decisions replaced (CANON, LAUNCH DECISIONS): the
# deposit is "$30 deposit, refunded the same day you attend your
# consultation" (never "fully refundable", never "applies to your first
# cycle"); the assessment credit is "credited toward your first purchase ..."
# (never "three month program" / "3-month package"); the start date is
# confirmed on the consultation (never "within the week"); the facility line
# is "private 1:1 coaching inside Teqneeq FHC, a members-only facility in 4S
# Ranch" (never "fully private" / "zero crowds"); the 30-Day Fit Guarantee
# reads "within your first 30 days" (never "after your first 30 days");
# nutrition is included in every program (no "add-ons"); the entry point is
# the Calendly consultation (no "Strategy Session"); reviews are 190+; the
# comparison page names Equinox's Equifit assessment; InBody frequencies
# vary by model; ECW/TBW is read as a trend, not an inflammation flag; the
# footer email is the domain address and the reviews link is the plain
# g.page URL; the lowest tier is $200 per 4 weeks, never "$250/month".
# Matched case-insensitively on the FLATTENED copy, so a phrase split by an
# inline tag ("<a>nutrition coaching</a> add-ons") still fires. Frozen
# records are exempt. footer.html IS swept, although it is otherwise out of
# scope, because two of the phrases lived only there. Negative-tested on
# every run by _selftest_retired_copy() before the sweep.
RETIRED_LAUNCH_COPY = [
    "fully refundable", "applies to your first cycle", "within the week",
    "zero crowds", "fully private", "nutrition coaching add-ons",
    "Strategy Session", "133+ Reviews", "three month program",
    "3-month package", "after your first 30 days",
    "no standardized assessment", "Typically single", "flags inflammation",
    "@gmail.com", "g.page/r/CcePeMjnbDe9EBM/review", "$250/month",
    # Calendly follow-up (Oct 17 2026): the territory FAQ answer's old credit
    # sentence. Canonical (run 7): "The Performance Assessment ($150 in person,
    # $75 virtual) is credited toward your first program, Reset cycle or 5-pack."
    "diagnostic fee is credited",
    # Launch decision 19 (Oct 17 2026): the travel-fee variants. Canonical:
    # "No travel fee inside our in-home service area; a travel fee may apply
    # outside it." (territory pages: "No travel fee in [Town]; it's inside our
    # in-home service area.")
    "depending on location", "varies by location",
    # Audit Reconciliation run (Oct 18 2026; CANON CANONICAL FACTS). Each is
    # the retired form of a canonical fact: the consultation is not an
    # assessment; the assessment sets 12 metrics in 7 categories; the travel
    # fee is named by area; reviews are "4.98 average across 190+ reviews";
    # the audience is "built for professionals 30+"; retention is the
    # /outcomes figure; check-ins follow the Dial; sessions are 60 minutes
    # (30 on the Reset); the early exit names statutory rights.
    "45-minute movement assessment", "seven tracked benchmarks",
    "a travel fee may apply outside it", "training throughout San Diego County",
    "available throughout San Diego County",
    "five-star reviews", "5.0 rating", "5.0 · 190+", "Rated 5.0",
    "verified reviews", "verified five-star", "works exclusively with",
    "client tenure", "6 months minimum",
    "Unlimited coach communication", "check-in submissions required",
    "45–60 min", "30 or 45-minute", "30–45 min",
    "is the only exit",
    # Claims & Tone run (6B, Oct 18 2026): the comparison page compares
    # categories, never a named local business; "Elite Training" headings are
    # retired ("Private Coaching in ..." / "1:1 Coaching in ...").
    "Iron Orr", "Elite Training",
    # Run 7 (Oct 18 2026): the consultation is not "paid" (it is a $30
    # deposit, refunded the same day you attend your consultation); studio
    # access is "Private, by appointment" (non-member rates include a Teqneeq
    # day pass); "assessment" names only the Performance Assessment, so the
    # CTA note reads "Straight answer on fit". Case-insensitive, like every
    # term here, so "Paid 45-minute" and "paid 45-minute" both fire.
    "paid 45-minute", "Credentialed access only", "Honest assessment of fit",
    # Run 7C (Oct 18 2026): the rule widened to the bare noun phrase, which
    # survived run 7 on FAQs, partners and the how-it-works step heading.
    # Case-insensitive, so "Paid Consultation" and "paid consultation" fire.
    "paid consultation",
]

def retired_launch_copy(text):
    """Every retired launch phrase in the file: (term, line, ctx). Searched on
    the FLATTENED copy (so a phrase split by an inline tag fires) AND on the
    raw source (so the footer's mailto: address and the review URL, which live
    inside href attributes that the tag strip removes, fire too). line is the
    first raw line carrying the phrase, or None when only the flattened copy
    carries it."""
    t = _flat(text); out = []
    raw = text.splitlines()
    for term in RETIRED_LAUNCH_COPY:
        rx = re.compile(re.escape(term), re.I)
        m = rx.search(t)
        ln = next((i for i, l in enumerate(raw, 1) if rx.search(l)), None)
        if not m and ln is None: continue
        ctx = (t[max(0, m.start()-60):m.end()+60] if m else raw[ln-1].strip()[:140]).strip()
        out.append((term, ln, ctx))
    return out

def _selftest_retired_copy():
    """Both directions, every run: each term must fire on a synthetic line,
    a tag-split phrase must fire, and clean canonical copy must not."""
    for term in RETIRED_LAUNCH_COPY:
        hits = retired_launch_copy(f"<p>Lorem {term.upper()} ipsum.</p>")
        assert [h[0] for h in hits] == [term], f"retired-copy rule did not fire on {term!r}"
    split = retired_launch_copy('<p>dedicated <a href="/x">nutrition coaching</a> add-ons are available.</p>')
    assert [h[0] for h in split] == ["nutrition coaching add-ons"], "tag-split phrase not caught"
    attr = retired_launch_copy('<a href="mailto:omnifittraining@gmail.com">Email</a>'
                               '<a href="https://g.page/r/CcePeMjnbDe9EBM/review">Reviews</a>')
    assert [h[0] for h in attr] == ["@gmail.com", "g.page/r/CcePeMjnbDe9EBM/review"], "attribute phrase not caught"
    clean = ("<p>$30 deposit, refunded the same day you attend your consultation. The $150 "
             "Performance Assessment is credited toward your first purchase: a Foundation or "
             "Program cycle, an Executive Reset cycle, or a 5-session pack. If OmniFit isn't "
             "the right fit within your first 30 days on The Foundation, The Program or the "
             "Executive Reset, tell us in writing and we'll refund the unused portion of your "
             "enrollment. Private 1:1 coaching inside Teqneeq FHC, a members-only facility in "
             "4S Ranch. 190+ Reviews. nemezio@omnifittraining.com $200 per 4 weeks "
             "https://g.page/r/CcePeMjnbDe9EBM No travel fee in Carmel Valley, Santaluz, "
             "Fairbanks Ranch, Rancho Bernardo, 4S Ranch or Poway; elsewhere in our in-home "
             "service area a travel fee applies, confirmed before you book. No travel fee in "
             "Santaluz; it's inside our in-home service area. A travel fee applies in Del Mar, "
             "confirmed before you book. 5-packs run $180 to $250 per session depending on "
             "setting and membership. 4.98 average across 190+ reviews (Google, Yelp, Thumbtack "
             "and Bark). Built for professionals 30+. About half of clients train with OmniFit "
             "for 6 months or longer (see Outcomes). Sessions are 60 minutes; 30 minutes on the "
             "Executive Reset. Apart from your statutory cancellation rights, the 30-Day Fit "
             "Guarantee is the only early exit. A 45-minute consultation, then the Performance "
             "Assessment. In-home training across North County San Diego. 45-minute "
             "consultation · $30 deposit, refunded the same day you attend your consultation "
             "· No commitment · Straight answer on fit. Private, by appointment: no walk-ins, "
             "no crowds. Credentialed professionals only. Sessions are paid in full at "
             "enrollment.</p>")
    for s in ("<h3>Paid Consultation (45 min)</h3>", "<p>Book a 45-minute paid consultation.</p>",
              '<p>Book a <a href="/x">paid</a> consultation.</p>'):
        assert [h[0] for h in retired_launch_copy(s)] == ["paid consultation"], f"paid-consultation rule did not fire on {s!r}"
    for s in ("<h3>Consultation (45 min)</h3>", "<p>Book a consultation ($30 deposit, refunded the same "
              "day you attend your consultation).</p>", "<p>Sessions are paid in full. Consultation first.</p>"):
        assert retired_launch_copy(s) == [], f"paid-consultation rule fired on canonical copy {s!r}"
    assert retired_launch_copy(clean) == [], "retired-copy rule fired on canonical copy"
    return len(RETIRED_LAUNCH_COPY)

# ─── (b) CONSULTATION CTA TO THE CONTACT FORM (owner, Oct 17 2026) ───
# ENTRY = CALENDLY DIRECT (CANON LAUNCH DECISIONS items 1 and 15): a link whose
# visible label offers a consultation goes to the Calendly booking page, never
# to /contactform. The contact form is still linked, but only under labels that
# do not promise a consultation ("Contact", "Get Started", "Start The
# Program"). Reads the RAW source so a JS-template link (fit-check) and a
# multi-line anchor (partners) are both seen; the label is tag-stripped, so an
# icon <svg> inside the anchor does not hide it.
_CONTACT_A = re.compile(r'<a\b[^>]*\bhref="(?:https://www\.omnifittraining\.com)?/contactform/?"[^>]*>(.*?)</a>',
                        re.S | re.I)

def consultation_cta_to_contactform(text):
    out = []
    for m in _CONTACT_A.finditer(text):
        label = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(1))).strip()
        if re.search(r'\bconsult', label, re.I):
            out.append((text[:m.start()].count('\n') + 1, label))
    return out

def _selftest_consultation_cta():
    fire = ['<a class="ab-btn" href="/contactform">Book a Consultation</a>',
            '<a href="/contactform" class="op-cta-btn">\n  Book Your Consultation\n  <svg><line/></svg>\n</a>',
            '<a href="https://www.omnifittraining.com/contactform">Book a paid consultation</a>']
    for f in fire:
        assert consultation_cta_to_contactform(f), f"consultation-CTA rule did not fire: {f[:50]}"
    quiet = ['<a href="/contactform">Contact</a>', '<a class="cp-mini" href="/contactform">Get Started</a>',
             '<a href="https://calendly.com/nemezio-omnifittraining/45min" target="_blank" rel="noopener">Book Your Consultation</a>']
    for q in quiet:
        assert not consultation_cta_to_contactform(q), f"consultation-CTA rule fired on: {q[:50]}"

# ─── (b) BOOKING CTA OR RESERVEACTION TO THE CONTACT FORM (owner, Oct 17 2026) ───
# CANON LAUNCH DECISIONS item 18 extends item 15 from consultation labels to
# every enrolment or booking button: a link labelled "Start ...", "Get
# Started", "Book ..." or "Stay ..." goes to Calendly, never /contactform, and
# no schema ReserveAction may target /contactform either. "Contact" links stay
# on the form and stay quiet. Same raw-source reading as the consultation rule.
_BOOKING_LABEL = re.compile(r'^(?:Start\b|Get Started\b|Book\b|Stay\b)', re.I)
_LDJSON = re.compile(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.S | re.I)

def booking_cta_to_contactform(text):
    out = []
    for m in _CONTACT_A.finditer(text):
        label = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(1))).strip()
        if _BOOKING_LABEL.search(label):
            out.append((text[:m.start()].count('\n') + 1, label))
    return out

def reserve_action_to_contactform(text):
    """ReserveAction nodes whose target (a URL string or an EntryPoint) names
    /contactform: (line of the ld+json block, target). A block that does not
    parse is the structure check's finding, not this rule's."""
    out = []
    def walk(n, ln):
        if isinstance(n, dict):
            t = n.get("@type")
            if (t == "ReserveAction" or (isinstance(t, list) and "ReserveAction" in t)) \
                    and "contactform" in json.dumps(n.get("target", "")):
                out.append((ln, json.dumps(n.get("target"))[:90]))
            for v in n.values(): walk(v, ln)
        elif isinstance(n, list):
            for v in n: walk(v, ln)
    for m in _LDJSON.finditer(text):
        try: data = json.loads(m.group(1))
        except ValueError: continue
        walk(data, text[:m.start()].count('\n') + 1)
    return out

def _selftest_booking_cta():
    fire = ['<a class="rt-btn rt-btn-primary" href="/contactform">Start With the Foundation</a>',
            '<a class="cp-mini" href="/contactform">Get Started</a>',
            '<a href="https://www.omnifittraining.com/contactform">Book Sessions</a>',
            '<a class="rt-btn" href="/contactform/">\n  Stay in the Program\n</a>']
    for f in fire:
        assert booking_cta_to_contactform(f), f"booking-CTA rule did not fire: {f[:50]}"
    quiet = ['<a href="/contactform">Contact</a>', '<a href="/contactform">Contact us to start</a>',
             '<a class="cp-mini" href="https://calendly.com/nemezio-omnifittraining/45min" target="_blank" rel="noopener">Get Started</a>']
    for q in quiet:
        assert not booking_cta_to_contactform(q), f"booking-CTA rule fired on: {q[:50]}"
    ra = lambda tgt: ('<script type="application/ld+json">{"@graph":[{"@type":"Service","potentialAction":'
                      '{"@type":"ReserveAction","target":' + tgt + '}}]}</script>')
    assert reserve_action_to_contactform(ra('"https://www.omnifittraining.com/contactform"')), "ReserveAction rule did not fire on a URL"
    assert reserve_action_to_contactform(ra('{"@type":"EntryPoint","urlTemplate":"https://www.omnifittraining.com/contactform"}')), \
        "ReserveAction rule did not fire on an EntryPoint"
    assert not reserve_action_to_contactform(ra('"https://calendly.com/nemezio-omnifittraining/45min"')), "ReserveAction rule fired on Calendly"
    assert not reserve_action_to_contactform('<script type="application/ld+json">{"@type":"WebPage",'
                                             '"url":"https://www.omnifittraining.com/contactform"}</script>'), \
        "ReserveAction rule fired on a WebPage url"

# ─── (b) KEN'S RETIRED MUSCLE FIGURE (owner, Oct 17 2026) ───
# CANON LAUNCH DECISIONS item 20 consolidates Ken's case to the documented
# bodyweight figure (175 -> 164 lb, 6 months) and retires the "+6 lbs muscle"
# claim. Unlike the retired-copy sweep this rule reads the FROZEN RECORDS too:
# the owner overrode their exemption for Ken's card, and the card is where the
# figure lived. Flattened copy, case-insensitive; the digit guard keeps
# "16 lbs of muscle" or "+6.2 lbs" from firing.
KEN_MUSCLE = [r'\+6 ?lbs?\b', r'(?<![\d.])6 pounds of muscle', r'(?<![\d.])6 lbs of muscle']

def ken_muscle_claim(text):
    t = _flat(text); out = []
    for rx in KEN_MUSCLE:
        for m in re.finditer(rx, t, re.I):
            out.append((m.group(0), t[max(0, m.start()-60):m.end()+40].strip()))
    return out

def _selftest_ken_muscle():
    for f in ['<div class="metric-value">+6 lbs</div>', '<p>−11 lb fat, +6 lb muscle</p>',
              '<p>gained approximately 6 pounds of muscle</p>', '<li>while gaining approximately 6 lbs of muscle</li>']:
        assert ken_muscle_claim(f), f"Ken muscle rule did not fire: {f[:50]}"
    for q in ['<p>lost 11 pounds of bodyweight (175 to 164 lb) in 6 months</p>', '<p>+18 lbs</p>',
              '<p>+6.2 lbs</p>', '<p>16 lbs of muscle</p>', '<p>−11 lb bodyweight, 6 months</p>']:
        assert not ken_muscle_claim(q), f"Ken muscle rule fired on: {q[:50]}"

# RETIRED with the October card: _marker_nearby, _inside_packs_table and the
# CANON_MARKERS / CANON_CARDS tables. All four existed to carve $175 out of the
# retired-rate rule as a legal in-home pack rung and Reset Bronze tier. The
# October card has neither: $175 appears in no product, so it is a plain
# BANNED literal now and needs no context at all. Kept as a note rather than
# code, because a dormant exemption is how a retired figure gets grandfathered
# back in through a context nobody re-reads.

# The October per-session figures. These are canonical AS SESSION RATES:
#   5-pack   180 studio member · 210 studio non-member · 250 in-home
#   single   205 studio member · 235 studio non-member · 275 in-home
#   extra    160 studio · 215 in-home     guest add-on 90
# $150 is the ASSESSMENT, not a session rate. Publishing it as a per-session
# price would be the October equivalent of the old mangled pack rung, so it is
# the one figure this rule still checks for context.
_SESSION_RATE = r'(?:per|a|each|/)\s*session|/\s*session|\bsession\b'

def assessment_as_session_rate(text):
    """$150 presented as a per-session rate. The figure itself is canonical -
    it is the Performance Assessment - so this rule checks the MEANING, not the
    number, which is the opposite shape to the August $150 rule it replaces."""
    t = _flat(text); out = []
    for m in re.finditer(r'\$150\b', t):
        # A RANGE is third-party pricing, not an OmniFit rate. The card's rule
        # is "round numbers only", so every OmniFit figure is a single number;
        # "$150-250/month" and "$150-200/session" are market ranges on the
        # comparison page. This restores, in a form that needs no class-name
        # whitelist, the competitor exemption the August $150 rule carried.
        if re.match(r'\s*[-–]\s*\d', t[m.end():]): continue
        after = ' '.join(t[m.end():].split()[:4])
        if re.search(_SESSION_RATE, after, re.I):
            out.append(t[max(0, m.start()-90):m.end()+90].strip())
    return out

# $140 - the August studio 10-pack rung ($140 per session) - is retired in that
# meaning and that meaning only. The same figure is the FOUNDATION PER-SESSION
# RATE (560 per cycle / 4 sessions), and the rates page states it in static
# text inside the tier-change worked example (CANON TIER CHANGES). So, like
# $150 above, the rule reads the MEANING: $140 presented as a session or pack
# PRICE fires; $140 as a computed figure in the credit arithmetic does not.
# A computed figure is one that sits in an equation: it follows "=" (the
# result of the division, "$560 / 4 sessions = $140 per session") or is
# followed by "=" (a factor in the product, "8 sessions x $140 = $1,120").
# Anything else that puts $140 beside "session" or "pack" - "$140 per
# session", "$140/session", "10-pack at $140" - is the retired rung.
_PACK_WORD = r'\b(?:\d+-?packs?|packs?|rungs?)\b'

def retired_pack_rate(text):
    """$140 as a pack/session price (the August 10-pack rung), not as the
    derived Foundation per-session rate inside the worked example."""
    t = _flat(text); out = []
    for m in re.finditer(r'\$140\b(?![\d,]*\d)', t):
        before = t[max(0, m.start()-40):m.start()]
        after = t[m.end():m.end()+60]
        # third-party range ("$140-200/session") - same exemption as $150
        if re.match(r'\s*[-–]\s*\d', after): continue
        # computed figure: result of, or factor in, an equation
        if re.search(r'=\s*$', before) or re.match(r'\s*=', after): continue
        near_after = ' '.join(after.split()[:4])
        if (re.search(_SESSION_RATE, near_after, re.I) or re.search(_PACK_WORD, near_after, re.I)
                or re.search(_PACK_WORD, before, re.I)):
            out.append(t[max(0, m.start()-90):m.end()+90].strip())
    return out

_VIRTUAL_ASSESS = r'virtual (?:performance )?assessment'

def retired_75(text):
    """$75 anywhere except as the Virtual Performance Assessment price
    (CANON CANONICAL FACTS, Oct 17 2026). The name must sit within 250
    characters before the figure or 120 after it, in the flattened copy, so
    "It is $75, credited ..." after a sentence naming the assessment passes,
    and "$75 guest add-on" or "$75 travel fee" fails."""
    t = _flat(text); out = []
    for m in re.finditer(r'\$75\b(?![\d,]*\d)', t):
        after = t[m.end():m.end()+120]
        if re.match(r'\s*[-–]\s*\d', after): continue      # third-party range
        if re.search(_VIRTUAL_ASSESS, t[max(0, m.start()-250):m.start()] + after, re.I): continue
        # the pricing FAQ shape: "Performance Assessment ($150 in person, $75 virtual)"
        if re.match(r'\s+virtual\b', after, re.I) and re.search(r'Performance Assessment \([^)]{0,40}$', t[max(0, m.start()-80):m.start()]): continue
        # the rates step-card shape (run 7, Oct 18 2026): "Performance Assessment
        # $150 in person · $75 virtual" and its body "... or virtual with
        # self-measurement and video guidance, no body-composition scan ($75)".
        # The assessment must be named within 260 characters before, and the
        # figure must read "$75 virtual" or close a virtual clause that names
        # self-measurement or video guidance (CANON's definition of it).
        before = t[max(0, m.start()-260):m.start()]
        if 'Performance Assessment' in before and (
                re.match(r'\s+virtual\b', after, re.I)
                or re.search(r'\bvirtual\b[^.$]{0,100}(?:self-measure|video guidance)[^.$]{0,60}\($', before, re.I)): continue
        out.append(t[max(0, m.start()-90):m.end()+90].strip())
    return out

def _selftest_retired_75():
    must_fail = ["<p>Guest add-on: $75 per session.</p>",
                 "<p>A $75 travel fee applies outside the area.</p>",
                 "<li>Extra session $75</li>"]
    must_pass = ["<p>Remote clients start with the $75 Virtual Performance Assessment, credited toward the first purchase.</p>",
                 "<p>Remote clients take the Virtual Performance Assessment. It is self-measured with live video guidance. It is $75, credited toward your first purchase.</p>",
                 "<p>Reset Platinum is $750 per 4 weeks.</p>",
                 "<p>Competitors charge $75-120 per session.</p>",
                 "<p>Programs and session packs start with a Performance Assessment ($150 in person, $75 virtual), credited toward your first purchase.</p>"]
    must_fail.append("<p>Guest add-on ($90 member, $75 virtual guest).</p>")
    # step-card shape, run 7: both legitimate forms pass, a lookalike fails
    must_pass += ["<h3>Performance Assessment</h3><div>$150 <span>in person · $75 virtual · credited toward your first purchase</span></div>",
                  "<h3>Performance Assessment</h3><p>In-studio at Teqneeq FHC or in your home ($150), or virtual with self-measurement and video guidance, no body-composition scan ($75).</p>"]
    must_fail += ["<h3>Performance Assessment</h3><p>$150. A virtual guest pass ($75).</p>",
                  "<h3>Performance Assessment</h3><p>$150. Guest add-on $75 per session.</p>"]
    for s in must_fail: assert retired_75(s), f"retired_75 self-test: should fail: {s}"
    for s in must_pass: assert not retired_75(s), f"retired_75 self-test: should pass: {s}"

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

# ─── Ask OmniFit assistant (owner brief, Oct 2026) ─────────────────
# The assistant answers visitors from assistant/knowledge.md, under the system
# prompt in functions/_lib/system-prompt.js, inside the widget copy in
# site/assistant.js (plus the fixed turn-cap reply in functions/_lib/assistant.js).
# None of these files is under pages/, so the glob above never sees them; they
# are screened here with the same rules, and the results count in (a) and (b).
ASSISTANT_KNOWLEDGE = "assistant/knowledge.md"
ASSISTANT_PROMPT = "functions/_lib/system-prompt.js"
ASSISTANT_SURFACES = (ASSISTANT_KNOWLEDGE, ASSISTANT_PROMPT, "site/assistant.js", "functions/_lib/assistant.js")
# The prompt is verbatim from the owner. Wording changes need owner approval
# and a new hash here and in CANON (ASK OMNIFIT).
ASSISTANT_PROMPT_SHA256 = "2ee2a1c006f3a6ef"

def assistant_knowledge_text(raw):
    """What the model actually receives: knowledge.md minus maintainer comments
    (build.py drops <!-- --> blocks the same way)."""
    return re.sub(r"<!--.*?-->\s*", "", raw, flags=re.S)

def assistant_prompt_text(raw):
    m = re.search(r"SYSTEM_PROMPT\s*=\s*`(.*?)`;", raw, re.S)
    if not m:
        raise ValueError(f"{ASSISTANT_PROMPT}: SYSTEM_PROMPT template literal not found")
    return m.group(1)

_NEVER_BLOCK = re.compile(r"^NEVER:\n(?:- .*\n)+", re.M)

def assistant_prompt_screenable(prompt):
    """The prompt minus its NEVER: list. That list names the banned framings in
    order to forbid them ('promise or guarantee results', 'call the consultation
    ... "free"'), so screening it reports the bans as violations. Every other
    line of the prompt is screened. WRONG IF a claim is ever added inside the
    NEVER list; the self-test below proves a claim outside it still fires."""
    out, n = _NEVER_BLOCK.subn("", prompt)
    if n != 1:
        raise ValueError(f"{ASSISTANT_PROMPT}: expected one NEVER: list, found {n}")
    return out

def _canon_card_numbers(canon):
    """Every figure in CANONICAL FACTS and the OCTOBER 2026 CARD block - the
    only places a published price may come from."""
    spans = [(canon.index("CANONICAL FACTS"), canon.index("\nREPO STATE")),
             (canon.index("PRICING — OCTOBER 2026 CARD"), canon.index("\nLEGACY PRICING"))]
    return {n.replace(",", "") for a, b in spans for n in re.findall(r"\d[\d,]*", canon[a:b])}

_PRICE = re.compile(r"\$\s?(\d[\d,]*(?:\.\d\d)?)")

def assistant_price_findings(md, canon):
    card = _canon_card_numbers(canon)
    return sorted({"$" + p for p in _PRICE.findall(md) if p.replace(",", "") not in card},
                  key=lambda x: float(x[1:].replace(",", "")))

# Wording the brief requires in the knowledge file exactly as published.
ASSISTANT_REQUIRED = [
    "If OmniFit isn't the right fit within your first 30 days on The Foundation, The Program or the "
    "Executive Reset, tell us in writing and we'll refund the unused portion of your enrollment.",
    "$30 deposit, refunded the same day you attend your consultation",
    "4.98 average across 190+ reviews",
    "No travel fee in Carmel Valley, Santaluz, Fairbanks Ranch, Rancho Bernardo, 4S Ranch or Poway",
    "a travel fee applies, confirmed before you book",
]
# Internal content that must never reach the assistant: tooling, compliance
# notes, the payment processor, legacy pricing, and client names.
_INTERNAL = re.compile(r"\b(?:Stripe|CANON|certify|certification|REPORT\.md|build\.py|tools/|compliance|"
                       r"Squarespace|legacy|grandfathered|August card|August 2026|counsel|monthly|per month)\b", re.I)
_CLIENT_NAMES = re.compile(r"\b(?:" + "|".join(sorted({n.split()[0] for n in CONSENT_LIST})) + r")\b")

def assistant_internal_findings(md):
    hits = [m.group(0) for m in _INTERNAL.finditer(md)]
    hits += [f"client name {m.group(0)}" for m in _CLIENT_NAMES.finditer(md)]
    return hits

def _selftest_assistant(canon):
    """Both directions for every assistant-only rule; raises on a rule that
    does not fire on a real violation or fires on legitimate copy."""
    bad = []
    if assistant_price_findings("Studio Momentum: $640 per 4-week cycle; $1,680 due at signup; $119/mo.", canon):
        bad.append("price check flagged October card prices")
    if assistant_price_findings("Studio Momentum: $475 per cycle.", canon) != ["$475"]:
        bad.append("price check missed the legacy $475")
    if assistant_price_findings("A 5-pack is $1,050 in total.", canon) != ["$1,050"]:
        bad.append("price check missed a total that is not on the card")
    if assistant_internal_findings("Payments run through Stripe. Mark M. lost weight.") != ["Stripe", "client name Mark"]:
        bad.append("internal-content check missed Stripe or a client name")
    if assistant_internal_findings("Book a consultation. Bodystat QuadScan 4000 reassessments are marked in the app."):
        bad.append("internal-content check flagged ordinary copy")
    prompt = assistant_prompt_text(open(ASSISTANT_PROMPT).read())
    screen = assistant_prompt_screenable(prompt)
    if any(fn(screen) for fn in COMPLIANCE):
        bad.append("prompt outside the NEVER list already fires (see the (a) findings)")
    if not any(fn(screen + "\nThe consultation is free.") for fn in COMPLIANCE):
        bad.append("a free-consultation claim outside the NEVER list did not fire")
    if not any(fn(screen + "\nWe guarantee you will lose 20 lbs.") for fn in COMPLIANCE):
        bad.append("an outcome guarantee outside the NEVER list did not fire")
    if bad:
        raise AssertionError("assistant self-test: " + "; ".join(bad))

def assistant_surface_texts():
    """{path: text as the visitor or the model meets it}."""
    out = {}
    for f in ASSISTANT_SURFACES:
        raw = open(f).read()
        if f == ASSISTANT_KNOWLEDGE: raw = assistant_knowledge_text(raw)
        if f == ASSISTANT_PROMPT: raw = assistant_prompt_screenable(assistant_prompt_text(raw))
        out[f] = raw
    return out


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

# The twelve page/header pairs that carry the canonical pricing FAQ answer
# (CANON INVARIANTS, "Canonical pricing FAQ answer"). Keep in step with CANON.
PRICING_FAQ_CARRIERS = (
    "corrective-exercise-post-rehab", "personal-trainer-4s-ranch", "personal-trainer-carlsbad",
    "personal-trainer-carmel-valley", "personal-trainer-del-mar", "personal-trainer-encinitas",
    "personal-trainer-fairbanks-ranch", "personal-trainer-la-jolla", "personal-trainer-rancho-bernardo",
    "personal-trainer-rancho-santa-fe", "personal-trainer-santaluz", "personal-trainer-solana-beach",
)

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
    # other: home-3.html was once the case-studies block pasted into the
    # homepage, and certifying both double-counted every finding on it. The kept file is the
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
    _selftest_case_study_exempt()   # Oct 17 2026 exemption fixes, both directions
    _selftest_lbs_fragment()        # Oct 18 2026 audit: ranges with '+' and any dash, both directions
    _selftest_retired_75()          # Oct 18 2026 audit: $75 legal only as the Virtual Performance Assessment
    _selftest_result_review_cadence()  # run 7B: review cadence is not an outcome window, both directions
    ciia = {}
    for f in files:
        t = open(f).read()
        # TIER 2 item 2a: frozen historical records are exempt from re-screening.
        if os.path.basename(f) in FROZEN:
            print(f"   {f}  [frozen historical record - not re-screened, CANON TIER 2 item 2a]")
            continue
        for fn in COMPLIANCE:
            for kind, what, ctx in fn(t):
                print(f"   {f}\n      [{kind}] {what}\n      …{ctx[:130]}…"); A+=1
        # TIER 2 item 4, first condition: ONE byte-identical wording of the
        # Class IIa fact everywhere it appears. Cross-file, so it is collected
        # here and judged once below - the same shape as an invariant.
        # Compare THE SENTENCE the fact sits in. CANON T2-4 asks the STATEMENT
        # to be byte-identical wherever it appears; a fixed word window also
        # compares the prose on either side of it, so three different words in
        # the PRECEDING sentence read as three different wordings of the same
        # claim. That is a checker reporting correct copy as a violation.
        # A word window was used first because an earlier sentence split, run
        # when the fact sat mid-sentence inside a header's ld+json, swept up
        # `" } }, { "@type": "Question"`. That is no longer the shape: the
        # canonical block is its own run of sentences on every surface, so the
        # split lands on the statement itself.
        ft = _flat(t)
        for m in re.finditer(r'Class IIa', ft, re.I):
            lo = max((ft.rfind(c, 0, m.start()) for c in '.!?'), default=-1) + 1
            hi = min((x for x in (ft.find(c, m.end()) for c in '.!?') if x != -1), default=len(ft))
            ciia.setdefault(_norm(ft[lo:hi + 1]), []).append(f)
    # Ask OmniFit surfaces (knowledge, system prompt outside its NEVER list,
    # widget copy): the same TIER 1 / TIER 2 rules as the pages.
    canon_text = open("CANON.md").read()
    _selftest_assistant(canon_text)
    for f, t in assistant_surface_texts().items():
        for fn in COMPLIANCE:
            for kind, what, ctx in fn(t):
                print(f"   {f}\n      [{kind}] {what}\n      …{ctx[:130]}…"); A+=1
    print(f"   (assistant: {len(ASSISTANT_SURFACES)} surfaces screened; prompt NEVER-list exemption self-tested both ways)")
    if len(ciia) > 1:
        print(f"   [Class IIa fact not byte-identical across files (T2-4)] "
              f"{len(ciia)} distinct wordings:")
        for w, fs in sorted(ciia.items(), key=lambda x: -len(x[1])):
            print(f"      {len(fs)}x  {', '.join(sorted(set(fs)))}\n         …{w[:160]}…")
        A += 1
    print("   none" if not A else f"   {A} strike(s)")

    # Outcome Claims Amendment (CANON TIER 2 items 2a and 2g). Reported in
    # full on every run; counted toward the result only once AMENDMENT_COUNTS
    # is True (CANON NEXT RUNS), because the amendment was recorded before any
    # page was brought to it and the first run's job is to list the gap.
    print("\n### (a') OUTCOME CLAIMS AMENDMENT - TIER 2 items 2a and 2g"
          + (" (counted)" if AMENDMENT_COUNTS else " (REPORTED, NOT COUNTED this run: AMENDMENT_COUNTS=False)"))
    _selftest_amendment()
    N = 0
    for f in files:
        if os.path.basename(f) in FROZEN: continue
        t = open(f).read()
        for ln, client, cond, detail in attributed_outcome_conditions(t, os.path.basename(f)):
            print(f"   {f}:{ln}  [2a {cond}] client: {client}\n      {detail[:170]}"); N += 1
        if os.path.basename(f) in _OUTCOMES_FILES: continue    # 2g's reference surface
        for ln, fig, kind, detail in data_backed_figures(t):
            print(f"   {f}:{ln}  [2g {kind}] '{fig}'\n      {detail[:170]}"); N += 1
    print(f"   (2a conditions 3/4/5 + consent, 2g: self-tested both ways; consent list: "
          f"{', '.join(CONSENT_LIST)}; frozen records exempt)")
    print("   none" if not N else f"   {N} finding(s)")
    if AMENDMENT_COUNTS: A += N

    print("\n### (b) STALE CANON")
    # A banned FIGURE must not match inside a longer one. Plain substring
    # matching made "$50" fire inside "$500" and "$75" inside "$750" - both
    # October Reset tiers - so the rule reported correct copy as stale on the
    # first run after the ban list was inverted. Figures are matched with a
    # right boundary (no digit or comma-digit may follow); word terms keep
    # plain substring matching, which is what catches "Pacific Beach" inside a
    # longer sentence.
    for term in BANNED:
        # A hyphenated RANGE ("$50-80/session", "$150-250/month") is
        # third-party pricing: the card's rule is round numbers only, so every
        # OmniFit figure is a single number. Same reasoning as the $150 rule,
        # and it is what lets the comparison page quote competitor rates
        # without a class-name whitelist.
        rx = (re.compile(re.escape(term) + r'(?![\d,]*\d)(?!\s*[-–]\s*\d)') if term.startswith('$')
              else re.compile(re.escape(term), re.I))
        for f in files:
            for i,l in enumerate(open(f),1):
                if rx.search(l):
                    print(f"   {f}:{i}  [{term}]"); B+=1
    # Tier names are matched case-SENSITIVELY on the capitalised product name,
    # so "essential movement patterns" is prose and "Essential" is a tier.
    for term in BANNED_TIERS:
        for f in files:
            for i,l in enumerate(open(f),1):
                if re.search(r'\b'+re.escape(term)+r'\b', l):
                    print(f"   {f}:{i}  [{term} is unlisted on the October card]"); B+=1
    for f in files:
        src=open(f).read(); L=src.splitlines(True)
        for term, sentence in fee_language(src):
            print(f"   {f}  [{term} outside the Foundation policy]  …{sentence[:90]}…"); B+=1
        for ctx in assessment_as_session_rate(src):
            print(f"   {f}  [$150 published as a session rate - it is the assessment]  …{ctx[:90]}…"); B+=1
        for ctx in retired_pack_rate(src):
            print(f"   {f}  [$140 as a pack/session price - the retired August 10-pack rung]  …{ctx[:90]}…"); B+=1
        for ctx in retired_75(src):
            print(f"   {f}  [$75 outside the Virtual Performance Assessment - the retired guest add-on / travel fee]  …{ctx[:90]}…"); B+=1
        for i,l in enumerate(L,1):
            # a travel FEE, not any dollar figure sharing a line with the word travel
            if re.search(r'travel[^.<]{0,30}\$(?:50|75)\b|\$(?:50|75)\b[^.<]{0,30}travel', l, re.I):
                print(f"   {f}:{i}  [travel fee dollar figure]"); B+=1
    # Retired launch copy (CANON, LAUNCH DECISIONS): every file in the glob,
    # footer.html included, frozen records exempt. Self-tested first so the
    # sweep below cannot report green without having fired on a known hit.
    n_terms = _selftest_retired_copy()
    swept = [x for x in ALL if os.path.basename(x) not in FROZEN]
    for f in swept:
        for term, ln, ctx in retired_launch_copy(open(f).read()):
            where = f"{f}:{ln}" if ln else f"{f} (phrase spans an inline tag)"
            print(f"   {where}  [retired launch copy: {term}]  …{ctx[:90]}…"); B+=1
    print(f"   (retired launch copy: {n_terms} phrases self-tested both ways, "
          f"{len(swept)} files swept incl. footer.html, frozen exempt)")
    _selftest_consultation_cta()
    for f in swept:
        for ln, label in consultation_cta_to_contactform(open(f).read()):
            print(f"   {f}:{ln}  [consultation CTA to /contactform: '{label}' must go to Calendly]"); B+=1
    print(f"   (consultation CTA rule: self-tested both ways, {len(swept)} files swept)")
    _selftest_booking_cta()
    for f in swept:
        src = open(f).read()
        for ln, label in booking_cta_to_contactform(src):
            print(f"   {f}:{ln}  [booking CTA to /contactform: '{label}' must go to Calendly]"); B+=1
        for ln, tgt in reserve_action_to_contactform(src):
            print(f"   {f}:{ln}  [ReserveAction targets /contactform: {tgt} - must be Calendly]"); B+=1
    print(f"   (booking CTA + ReserveAction rule: self-tested both ways, {len(swept)} files swept)")
    _selftest_positioning(); _selftest_travel_protocol()
    for f in swept:
        src = open(f).read()
        for kind, ctx in positioning_line_verbatim(src):
            print(f"   {f}  [{kind}]  …{ctx[:90]}…"); B+=1
        for kind, ctx in travel_protocol_usage(src):
            print(f"   {f}  [{kind}]  …{ctx[:90]}…"); B+=1
    print(f"   (positioning line + Travel Protocol rules: self-tested both ways, {len(swept)} files swept)")
    _selftest_ken_muscle()
    for f in ALL:
        for hit, ctx in ken_muscle_claim(open(f).read()):
            print(f"   {f}  [Ken's retired muscle figure: {hit}]  …{ctx[:90]}…"); B+=1
    print(f"   (Ken muscle-figure rule: self-tested both ways, {len(ALL)} files swept, frozen records INCLUDED)")
    _selftest_teqneeq_pt()
    for f in ALL:
        for kind, ctx in teqneeq_onsite_pt(open(f).read()):
            print(f"   {f}  [{kind}]  …{ctx[:110]}…"); B+=1
    print(f"   (Teqneeq on-site PT rule: self-tested both ways, {len(ALL)} files swept, frozen records INCLUDED)")
    _selftest_coaching_tenure()
    for f in ALL:
        for hit, ctx in coaching_tenure_claim(open(f).read()):
            print(f"   {f}  [coaching tenure claimed: '{hit}' - CANON: coaching since 2016, never a number of professional years]  …{ctx[:110]}…"); B+=1
    print(f"   (coaching-tenure rule: self-tested both ways, {len(ALL)} files swept, frozen records INCLUDED)")
    _selftest_retired_service_area()
    for f in ALL:
        for hit, ln, ctx in retired_service_area(open(f).read(), f):
            print(f"   {f}:{ln}  [retired service area: '{hit}' - CANON: the Pacific Beach era and its areas are history]  …{ctx[:110]}…"); B+=1
    print(f"   (retired service area rule: self-tested both ways, {len(ALL)} files swept, frozen records INCLUDED; "
          f"comments, attributes, URLs, _redirects, REPORT.md, archive/ ignored)")
    # Ask OmniFit: stale canon on every assistant surface, then the knowledge
    # file's prices against CANON, its required wording, and no internal content.
    for f, t in assistant_surface_texts().items():
        for term in BANNED:
            rx = (re.compile(re.escape(term) + r'(?![\d,]*\d)(?!\s*[-–]\s*\d)') if term.startswith('$')
                  else re.compile(re.escape(term), re.I))
            if rx.search(t): print(f"   {f}  [{term}]"); B+=1
        for term in BANNED_TIERS:
            if re.search(r'\b'+re.escape(term)+r'\b', t): print(f"   {f}  [{term} is unlisted on the October card]"); B+=1
        for term, sentence in fee_language(t):
            print(f"   {f}  [{term} outside the Foundation policy]  …{sentence[:90]}…"); B+=1
        for fn in (assessment_as_session_rate, retired_pack_rate, retired_75):
            for ctx in fn(t): print(f"   {f}  [{fn.__name__}]  …{ctx[:90]}…"); B+=1
        for term, ln, ctx in retired_launch_copy(t):
            print(f"   {f}:{ln}  [retired launch copy: {term}]  …{ctx[:90]}…"); B+=1
        for fn in (positioning_line_verbatim, travel_protocol_usage, ken_muscle_claim, teqneeq_onsite_pt, coaching_tenure_claim):
            for kind, ctx in fn(t): print(f"   {f}  [{kind}]  …{ctx[:90]}…"); B+=1
        for hit, ln, ctx in retired_service_area(t, f):
            print(f"   {f}:{ln}  [retired service area: '{hit}']"); B+=1
    md = assistant_knowledge_text(open(ASSISTANT_KNOWLEDGE).read())
    for price in assistant_price_findings(md, canon_text):
        print(f"   {ASSISTANT_KNOWLEDGE}  [price {price} is not on the CANON October card or in CANONICAL FACTS]"); B+=1
    for phrase in ASSISTANT_REQUIRED:
        if phrase not in md:
            print(f"   {ASSISTANT_KNOWLEDGE}  [required wording missing: {phrase[:70]}…]"); B+=1
    for hit in assistant_internal_findings(md):
        print(f"   {ASSISTANT_KNOWLEDGE}  [internal content must not reach the assistant: {hit}]"); B+=1
    prompt_sha = hashlib.sha256(assistant_prompt_text(open(ASSISTANT_PROMPT).read()).encode()).hexdigest()[:16]
    if prompt_sha != ASSISTANT_PROMPT_SHA256:
        print(f"   {ASSISTANT_PROMPT}  [system prompt changed: sha256 {prompt_sha}, owner-approved {ASSISTANT_PROMPT_SHA256}]"); B+=1
    print(f"   (assistant: {len(ASSISTANT_SURFACES)} surfaces swept for stale canon; knowledge prices vs CANON card, "
          f"{len(ASSISTANT_REQUIRED)} required phrases, internal content: self-tested both ways; prompt sha256 {prompt_sha})")
    print("   none" if not B else f"   {B} hit(s)")

    print("\n### (c) BROKEN STRUCTURE")
    faq.selftest()   # section-toggle summaries (rates V16) are not FAQ questions; both directions
    print("   (FAQ extractor: section-toggle exclusion self-tested both ways)")
    _selftest_placeholder()
    for f in ALL:
        for hit, ctx in placeholder_copy(open(f).read()):
            print(f"   {f}  [placeholder in visible copy: '{hit}']  …{ctx[:110]}…"); C+=1
    print(f"   (placeholder rule: self-tested both ways, {len(ALL)} files swept, frozen records INCLUDED)")
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
                # Sept 20, 2026: the entity graph (Organization / Person /
                # LocalBusiness / WebSite) is defined ONCE, in the site-wide
                # header injection recorded as pages/headers/site-header.html.
                # That file is the only header allowed to carry LocalBusiness;
                # every other header (the homepage page-header included)
                # references it by @id.
                if "LocalBusiness" in n and not f.endswith("/site-header.html"):
                    print(f"   {f}  [LocalBusiness redefined]"); C+=1
                if f.endswith("/site-header.html"):
                    if not n.get("LocalBusiness",{}).get("@id","").endswith("#localbusiness-of"):
                        print(f"   {f}  [site-header LocalBusiness must carry @id #localbusiness-of]"); C+=1
                    continue
                pn = next((n[k] for k in PAGE_TYPES if k in n), None)
                if pn is None:
                    notrun.append(f"{f}  @graph has no WebPage node ({sorted(n)}) - "
                                  f"about-references-homepage-LocalBusiness check could not run")
                elif not pn.get("about",{}).get("@id","").endswith("#localbusiness-of"):
                    print(f"   {f}  [about not referencing homepage LocalBusiness]"); C+=1
            slug=re.sub(r'-header\.html$','',f.split('/')[-1])
            # The homepage exists only as the home-0..6 fragments, so there is
            # no pages/home.html. CANON (ORPHAN HEADERS, home-header.html) says
            # its FAQPage mirrors pages/home-5.html; check it there rather than
            # report "no matching page" for a header that is live and built.
            pg=HEADER_PAGE.get(slug, f"pages/{slug}.html")
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
            if slug in NO_FAQ:
                shaped = re.findall(FAQ_SHAPED, pagesrc, re.I) + re.findall(r'"FAQPage"', open(f).read())
                if pq or sq or shaped:
                    print(f"   {f}  [declared no-FAQ page carries FAQ markup] "
                          f"page={len(pq)} schema={len(sq)} markers={sorted(set(shaped))[:4]}"); C+=1
                continue
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
    # CARRIER LIST of the canonical pricing FAQ answer (CANON INVARIANTS). The
    # hash says the carriers agree; this says WHICH files carry it, so a page
    # dropping the block (or growing a copy) is a finding, not a silent change
    # of scope. The-30-minute-executive-reset left the list in the Audit
    # Reconciliation run (Oct 18 2026, owner-approved): its cost FAQ answers
    # with the Reset tiers only.
    carriers = {os.path.basename(x).replace('-header.html','').replace('.html','') + (' (header)' if '/headers/' in x else '')
                for x in files if 'OmniFit Performance publishes its rates in full.' in open(x).read()}
    want = {s + h for s in PRICING_FAQ_CARRIERS for h in ('', ' (header)')}
    for x in sorted(carriers ^ want):
        print(f"   [pricing FAQ carrier list] {x} {'carries the block but is not a listed carrier' if x in carriers else 'is a listed carrier but no longer carries the block'}"); C+=1
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
          f"  (compliance {A} · stale canon {B} · structure {C} · not-run {len(notrun)}"
          f" · amendment 2a/2g {N}{'' if AMENDMENT_COUNTS else ' NOT COUNTED'})")
    return A,B,C

if __name__ == "__main__":
    run()
