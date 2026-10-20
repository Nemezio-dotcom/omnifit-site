"""The OmniFit Journal (/blog): post parsing and rendering for build.py.

Sources
  pages/blog/<slug>.html   one post: a POST metadata comment, then the
                           article body (plain semantic HTML, no wrapper,
                           no <style>; the look lives in site/blog.css)
  site/blog.css            journal styles, scoped under .omni-blog; appended
                           to public/assets/site.css only once a post exists

Post format (every key required except `updated`, `image` and `image_alt`):

    <!-- POST
    title:       SEO title (no trailing brand; keep it under ~60 characters)
    description: meta description (~150 characters)
    h1:          the visible headline
    published:   YYYY-MM-DD
    updated:     YYYY-MM-DD   (optional; defaults to published)
    method:      e.g. Correct · Regulation (physical stage · behavioral stage)
    minutes:     reading time, whole minutes
    image:       optional lead photo, a .jpg in site/img (e.g. name-1600.jpg);
                 a same-name .webp and smaller -NNNN.jpg/.webp siblings are
                 picked up for srcset
    image_alt:   alt text for the photo (required when image is set)
    -->
    <p class="post-lede">...</p>
    <h2>...</h2> <p>...</p> ...
    <aside class="post-quotable"><p>...</p></aside>
    <section class="post-faq">
      <h2>...</h2>
      <div class="post-q"><h3>Question?</h3><p>Answer.</p></div>
    </section>

Generated per post: the page chrome (breadcrumb, method tag, H1, byline,
lead photo, author box, consultation CTA), Open Graph / Twitter card tags
when the post has an image, and one JSON-LD @graph (BlogPosting,
BreadcrumbList, and a FAQPage built from the visible .post-q blocks, so the
schema always mirrors the page). /blog lists every post, newest first.

While pages/blog/ holds no post, nothing here changes the build: no /blog
page, the /blog 302 stays, no CSS, no footer link, no llms.txt lines.
Standard library only.
"""
import datetime
import html
import json
import re
import struct
from pathlib import Path

REQUIRED = ("title", "description", "h1", "published", "method", "minutes")
META_RE = re.compile(r"\A\s*<!--\s*POST\s*\n(.*?)-->\s*", re.S)
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TAG_RE = re.compile(r"<[^>]+>")
Q_RE = re.compile(r'<div class="post-q">\s*<h3>(.*?)</h3>(.*?)</div>', re.S)
WIDTH_RE = re.compile(r"^(.*)-(\d+)$")

AUTHOR_NAME = "Nemezio LopezPerez"
CALENDLY = "https://calendly.com/nemezio-omnifittraining/45min"


class PostError(SystemExit):
    pass


def _jpeg_size(path):
    """(width, height) from a JPEG's SOF marker."""
    d = path.read_bytes()
    i = 2
    while i + 9 < len(d):
        if d[i] != 0xFF:
            break
        marker = d[i + 1]
        seg_len = struct.unpack(">H", d[i + 2:i + 4])[0]
        if marker in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", d[i + 5:i + 9])
            return w, h
        i += 2 + seg_len
    raise PostError(f"{path}: could not read the JPEG size")


def _image(p, name, alt, img_dir):
    """Resolve a post's lead photo into src, srcset (jpg and webp), size and alt."""
    if not alt:
        raise PostError(f"{p}: image is set, so image_alt is required")
    src = Path(img_dir) / name
    if src.suffix.lower() not in (".jpg", ".jpeg") or not src.is_file():
        raise PostError(f"{p}: image {name!r} must be a .jpg in site/img")
    w, h = _jpeg_size(src)
    m = WIDTH_RE.match(src.stem)
    if m:
        widths = sorted(int(f.stem.rsplit("-", 1)[1]) for f in src.parent.glob(f"{m.group(1)}-*{src.suffix}")
                        if WIDTH_RE.match(f.stem) and WIDTH_RE.match(f.stem).group(1) == m.group(1))
        stems = [(f"{m.group(1)}-{n}", n) for n in widths if n <= int(m.group(2))]
    else:
        stems = [(src.stem, w)]
    jpg = ", ".join(f"/assets/img/{s}{src.suffix} {n}w" for s, n in stems)
    webp = ", ".join(f"/assets/img/{s}.webp {n}w" for s, n in stems)
    has_webp = all((src.parent / f"{s}.webp").is_file() for s, _ in stems)
    return {"src": f"/assets/img/{name}", "srcset": jpg, "webp": webp if has_webp else "",
            "width": w, "height": h, "alt": alt}


def load_posts(blog_dir, img_dir=None):
    """pages/blog/*.html -> list of post dicts, newest first."""
    blog_dir = Path(blog_dir)
    posts = []
    if not blog_dir.is_dir():
        return posts
    for p in sorted(blog_dir.glob("*.html")):
        text = p.read_text(encoding="utf-8")
        m = META_RE.match(text)
        if not m:
            raise PostError(f"{p}: missing the <!-- POST ... --> metadata comment at the top")
        meta = {}
        for line in m.group(1).splitlines():
            line = line.strip()
            if not line:
                continue
            if ":" not in line:
                raise PostError(f"{p}: bad metadata line {line!r}")
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip()
        missing = [k for k in REQUIRED if not meta.get(k)]
        if missing:
            raise PostError(f"{p}: metadata missing {missing}")
        meta.setdefault("updated", meta["published"])
        if not meta["updated"]:
            meta["updated"] = meta["published"]
        for k in ("published", "updated"):
            if not DATE_RE.match(meta[k]):
                raise PostError(f"{p}: {k} must be YYYY-MM-DD")
        if not meta["minutes"].isdigit():
            raise PostError(f"{p}: minutes must be a whole number")
        if not SLUG_RE.match(p.stem):
            raise PostError(f"{p}: file name must be a lower-case hyphenated slug")
        if meta.get("image"):
            meta["image"] = _image(p, meta["image"], meta.get("image_alt", ""), img_dir)
        else:
            meta["image"] = None
        body = text[m.end():].strip()
        if "<style" in body or "<h1" in body:
            raise PostError(f"{p}: the body carries no <style> and no <h1> (the template adds the H1)")
        posts.append({"slug": p.stem, "path": p, "body": body, **meta})
    posts.sort(key=lambda r: (r["published"], r["slug"]), reverse=True)
    return posts


def _date_label(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d:%B} {d.day}, {d.year}"


def _plain(fragment):
    return re.sub(r"\s+", " ", html.unescape(TAG_RE.sub("", fragment))).strip()


def faq_pairs(body):
    return [(_plain(q), _plain(a)) for q, a in Q_RE.findall(body)]


def post_header(post, base):
    url = f"{base}/blog/{post['slug']}"
    graph = [
        {
            "@type": "BlogPosting",
            "@id": f"{url}#article",
            "url": url,
            "mainEntityOfPage": url,
            "headline": post["h1"],
            "description": post["description"],
            "datePublished": post["published"],
            "dateModified": post["updated"],
            "author": {"@id": f"{base}/#founder"},
            "publisher": {"@id": f"{base}/#organization"},
            "isPartOf": {"@id": f"{base}/blog#blog"},
            "about": {"@id": f"{base}/#localbusiness-of"},
            "breadcrumb": {"@id": f"{url}#breadcrumb"},
            "inLanguage": "en-US",
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{url}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{base}/"},
                {"@type": "ListItem", "position": 2, "name": "Journal", "item": f"{base}/blog"},
                {"@type": "ListItem", "position": 3, "name": post["h1"], "item": url},
            ],
        },
    ]
    img = post["image"]
    if img:
        graph[0]["image"] = {"@type": "ImageObject", "url": base + img["src"],
                             "width": img["width"], "height": img["height"]}
    pairs = faq_pairs(post["body"])
    if pairs:
        graph.append({
            "@type": "FAQPage",
            "@id": f"{url}#faq",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in pairs
            ],
        })
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)
    return ("<!-- Generated by site/blog.py from pages/blog/" + post["slug"] + ".html. "
            "Edit the post, not this block. -->\n" + _social_tags(post, url, base) +
            '<script type="application/ld+json">\n' + data + "\n</script>")


def _social_tags(post, url, base):
    """Open Graph and Twitter card tags, so a shared link shows the lead photo."""
    img = post["image"]
    if not img:
        return ""
    e = lambda v: html.escape(str(v), quote=True)
    tags = [
        ("property", "og:type", "article"),
        ("property", "og:site_name", "OmniFit Performance"),
        ("property", "og:title", post["h1"]),
        ("property", "og:description", post["description"]),
        ("property", "og:url", url),
        ("property", "og:image", base + img["src"]),
        ("property", "og:image:width", img["width"]),
        ("property", "og:image:height", img["height"]),
        ("property", "og:image:alt", img["alt"]),
        ("property", "article:published_time", post["published"]),
        ("property", "article:modified_time", post["updated"]),
        ("name", "twitter:card", "summary_large_image"),
        ("name", "twitter:image", base + img["src"]),
    ]
    return "".join(f'<meta {a}="{k}" content="{e(v)}">\n' for a, k, v in tags)


def _figure(img):
    if not img:
        return ""
    webp = (f'<source type="image/webp" srcset="{img["webp"]}" sizes="(max-width:760px) 100vw, 720px">'
            if img["webp"] else "")
    return f"""<figure class="ob-figure">
    <picture>{webp}<img src="{img['src']}" srcset="{img['srcset']}" sizes="(max-width:760px) 100vw, 720px" width="{img['width']}" height="{img['height']}" alt="{html.escape(img['alt'], quote=True)}" fetchpriority="high" decoding="async"></picture>
  </figure>
  """


CTA = f"""<aside class="ob-cta" aria-label="Work with OmniFit">
    <p class="ob-cta-title">Want this applied to you, not just read about?</p>
    <p>Every OmniFit program starts with a Performance Assessment: a movement screen and baseline measurements, then a plan built from what we find.</p>
    <div class="ob-cta-row">
      <a class="ob-btn ob-btn--gold" href="{CALENDLY}">Book Your Consultation</a>
      <a class="ob-btn" href="/fit-check">Take the Fit Check</a>
    </div>
    <p class="ob-cta-note">45-minute video or phone consultation. $30 refundable deposit, refunded the same day you attend.</p>
  </aside>"""

AUTHOR = f"""<aside class="ob-author" aria-label="About the author">
    <p class="ob-author-name"><a href="/about">{AUTHOR_NAME}</a></p>
    <p>Founder of OmniFit Performance. NASM Elite Trainer and Precision Nutrition Level 2 Master Health Coach, with thirteen certifications across corrective exercise, performance and nutrition coaching. He coaches busy professionals 30+ in 4S Ranch, in their homes across North County, and online. OmniFit is a personal training practice, not a medical provider.</p>
  </aside>"""


def post_body(post):
    return f"""<div class="omni-blog">
<article class="ob-post">
  <header class="ob-hero">
    <div class="ob-hero-inner">
    <nav class="ob-crumb" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <a href="/blog">Journal</a></nav>
    <span class="ob-tag">{html.escape(post['method'])}</span>
    <h1>{html.escape(post['h1'])}</h1>
    <p class="ob-byline">By <a href="/about">{AUTHOR_NAME}</a> · <time datetime="{post['published']}">{_date_label(post['published'])}</time> · {post['minutes']} min read</p>
    </div>
  </header>
  <div class="ob-main">
  {_figure(post['image'])}<div class="ob-body">
{post['body']}
  </div>
  {AUTHOR}
  {CTA}
  <p class="ob-back"><a href="/blog">More from the Journal</a></p>
  </div>
</article>
</div>"""


INDEX_TITLE = "The OmniFit Journal | Training, Nutrition and Behavior Change"
INDEX_DESC = ("Long-form articles from OmniFit Performance on strength, corrective work, nutrition "
              "and the habits that make them stick, written for busy professionals 30+.")


def index_body(posts):
    cards = []
    for p in posts:
        cards.append(f"""  <article class="ob-card">
    <span class="ob-tag">{html.escape(p['method'])}</span>
    <h2><a href="/blog/{p['slug']}">{html.escape(p['h1'])}</a></h2>
    <p>{html.escape(p['description'])}</p>
    <p class="ob-card-meta"><time datetime="{p['published']}">{_date_label(p['published'])}</time> · {p['minutes']} min read</p>
  </article>""")
    return f"""<div class="omni-blog">
<header class="ob-hero ob-hero--index">
  <div class="ob-hero-inner">
  <span class="ob-tag">The OmniFit Journal</span>
  <h1>Training, Nutrition and the Habits That Hold Them Together</h1>
  <p class="ob-intro">Every article pairs a physical stage of the OmniFit Method (Assess, Correct, Build, Sustain) with a behavioral one (Awareness, Regulation, Adaptation, Integration), because a program only works if the person can keep running it. Written by {AUTHOR_NAME} for busy professionals 30+.</p>
  </div>
</header>
<div class="ob-main">
<div class="ob-list">
{chr(10).join(cards)}
</div>
{CTA}
</div>
</div>"""


def index_header(posts, base):
    graph = [
        {
            "@type": "Blog",
            "@id": f"{base}/blog#blog",
            "url": f"{base}/blog",
            "name": "The OmniFit Journal",
            "description": INDEX_DESC,
            "publisher": {"@id": f"{base}/#organization"},
            "author": {"@id": f"{base}/#founder"},
            "isPartOf": {"@id": f"{base}/#website"},
            "inLanguage": "en-US",
            "blogPost": [{"@id": f"{base}/blog/{p['slug']}#article"} for p in posts],
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{base}/blog#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{base}/"},
                {"@type": "ListItem", "position": 2, "name": "Journal", "item": f"{base}/blog"},
            ],
        },
    ]
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)
    return ('<!-- Generated by site/blog.py. -->\n<script type="application/ld+json">\n' + data + "\n</script>")


def llms_lines(posts, base):
    lines = ["", "## The OmniFit Journal", f"- [Journal index]({base}/blog) - Long-form articles pairing training, nutrition and behavior change."]
    for p in posts:
        lines.append(f"- [{p['h1']}]({base}/blog/{p['slug']}) - {p['description']}")
    return "\n".join(lines) + "\n"


FOOTER_LINK = '\n          <li><a href="/blog"><span>Journal</span></a></li>'
