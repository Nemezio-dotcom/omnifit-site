"""Ordered (question, answer) extraction across every FAQ markup pattern in the repo.

Missing a pattern does not fail loudly on its own: it silently yields a question
with no answer, or no question at all, and every downstream check then compares
nothing and calls it a pass. `qa()` therefore refuses to return a page whose
questions all lost their answers, and `qa_strict()` refuses any missing answer.
"""
import re, html


class ExtractorFailure(Exception):
    """The page has FAQ questions the extractor could read and answers it could
    not. An unknown answer-container class is an extractor bug, never a page
    that legitimately has zero answers."""


QPATS = [
    # <summary> carries a class on some pages (hsa-fsa-personal-training uses
    # <summary class="hsa-faq-q">); the attribute-less form matched only the
    # territory pages and silently skipped the rest.
    r'<summary[^>]*>(.*?)</summary>',
    r'<div class="[a-z-]*faq-q">(.*?)</div>',
    r'<button class="fq"[^>]*>(.*?)<span',
    # <button class="faq-q"> - online-training. The `fq` pattern above stops at
    # the icon <span>; this one has no icon and closes normally.
    r'<button class="[a-z-]*faq-q"[^>]*>(.*?)</button>',
    r'<div class="faq-question">(.*?)</div>',
    r'<button class="op-faq-q"[^>]*>(.*?)<svg',
]
APATS = [
    # `[a-z-]*faq-a` covers faq-a, of-faq-a, cx-faq-a, bc-faq-a, fl-faq-a,
    # st-faq-a, hiit-faq-a - every hyphen-prefixed variant in the repo.
    r'<div class="[a-z-]*faq-a"[^>]*>(.*?)</div>',
    r'<div class="[a-z-]*faq-body"[^>]*>(.*?)</div>\s*</details>',
    r'<div class="fa"><p>(.*?)</p></div>',
    r'<div class="faq-answer">(.*?)</div>\s*</div>',
    r'<div class="op-faq-a-inner">(.*?)</div>',
    # bare `answer`, with no faq- prefix at all - home-5
    r'<div class="answer"[^>]*>(.*?)</div>',
]

def _clean(x):
    x = re.sub(r'<[^>]+>', ' ', x)
    return re.sub(r'\s+', ' ', html.unescape(x)).strip()

def _hits(s, pats):
    """All container matches, ordered by document position.

    Two patterns can match the SAME container - `op-faq-q` is read both by the
    `<svg` pattern and by the generic `</button>` one. Both start at the same
    offset, so the container is deduplicated on its start position and the
    SHORTEST match wins: the shorter stop point is the more specific reading of
    the same element. Without this, one container yields two questions and the
    pairing walks off by one for the rest of the page."""
    best = {}
    for p in pats:
        for m in re.finditer(p, s, re.S):
            cur = best.get(m.start())
            if cur is None or m.end() < cur[0]:
                best[m.start()] = (m.end(), _clean(m.group(1)))
    return sorted((st, en, t) for st, (en, t) in best.items())

def qa(s):
    qs, ans = _hits(s, QPATS), _hits(s, APATS)
    # A page with questions and not one extractable answer is an unknown
    # answer-container class, not a page without answers. Returning the pairs
    # anyway lets a mirror check compare [] to [] and report success.
    if qs and not ans:
        raise ExtractorFailure(
            f"{len(qs)} question(s) and 0 extractable answers - unknown answer "
            f"container. First question: {qs[0][2][:80]!r}")
    pairs = []
    for i, (qa_s, qa_e, q) in enumerate(qs):
        nxt = qs[i + 1][0] if i + 1 < len(qs) else len(s)
        a = next((t for st, en, t in ans if st >= qa_e and st < nxt), None)
        pairs.append((q, a))
    return pairs

def qa_strict(s):
    """qa() but refuses to return a question whose answer could not be extracted.
    Writing a None answer into a header silently destroys real content."""
    pairs = qa(s)
    missing = [q for q, a in pairs if not a]
    assert not missing, f"{len(missing)} question(s) with no extractable answer: {missing[:3]}"
    return pairs

def questions(s):
    return [q for q, _ in qa(s)]
