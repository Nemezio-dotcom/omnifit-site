"""Ordered (question, answer) extraction across every FAQ markup pattern in the repo."""
import re, html

QPATS = [
    # `<summary ...>` with attributes as well as bare. hsa-fsa-personal-training
    # writes `<summary class="hsa-faq-q">`; the bare-tag-only version yielded
    # ZERO questions for that page, which reads downstream as "the page has no
    # FAQ" rather than "the extractor does not know this markup" — the same
    # silent-miss shape as the answer-pattern incident in tools/README.md.
    r'<summary[^>]*>(.*?)</summary>',
    r'<div class="[a-z-]*faq-q">(.*?)</div>',
    r'<button class="fq"[^>]*>(.*?)<span',
    r'<div class="faq-question">(.*?)</div>',
    r'<button class="op-faq-q"[^>]*>(.*?)<svg',
]
APATS = [
    r'<div class="[a-z-]*faq-a"[^>]*>(.*?)</div>',
    r'<div class="[a-z-]*faq-body"[^>]*>(.*?)</div>\s*</details>',
    r'<div class="fa"><p>(.*?)</p></div>',
    r'<div class="faq-answer">(.*?)</div>\s*</div>',
    r'<div class="op-faq-a-inner">(.*?)</div>',
]

def _clean(x):
    x = re.sub(r'<[^>]+>', ' ', x)
    return re.sub(r'\s+', ' ', html.unescape(x)).strip()

def _hits(s, pats):
    out = []
    for p in pats:
        for m in re.finditer(p, s, re.S):
            out.append((m.start(), m.end(), _clean(m.group(1))))
    return sorted(out)

def qa(s):
    qs, ans = _hits(s, QPATS), _hits(s, APATS)
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
