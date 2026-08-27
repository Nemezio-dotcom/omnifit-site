from app.crawler.extractor import extract

SAMPLE_HTML = """
<!DOCTYPE html><html lang="en"><head>
<title>Personal Training in San Diego | OmniFit</title>
<meta name="description" content="Premium personal training for professionals 30+.">
<link rel="canonical" href="https://example.com/services">
<meta property="og:title" content="OmniFit Services">
<script type="application/ld+json">{"@type": "WebPage", "name": "Services"}</script>
</head><body>
<h1>Personal Training Services</h1>
<h2>Corrective Exercise</h2>
<h2>Strength Training</h2>
<p>OmniFit Performance provides personal training in San Diego for professionals 30+.</p>
<a href="/about">About</a>
<a href="https://external-site.com/partner">Partner</a>
<a href="#skip">Skip link</a>
<a href="mailto:info@example.com">Email</a>
<img src="/img/hero.jpg" alt="Trainer coaching a client">
<img src="/img/logo.png">
</body></html>
"""


def test_extract_title_and_meta():
    result = extract(SAMPLE_HTML, "https://example.com/services", "https://example.com/")
    assert result.title == "Personal Training in San Diego | OmniFit"
    assert result.meta_description == "Premium personal training for professionals 30+."
    assert result.canonical == "https://example.com/services"


def test_extract_headings():
    result = extract(SAMPLE_HTML, "https://example.com/services", "https://example.com/")
    assert result.h1 == ["Personal Training Services"]
    assert result.h2 == ["Corrective Exercise", "Strength Training"]


def test_extract_links_split_internal_external():
    result = extract(SAMPLE_HTML, "https://example.com/services", "https://example.com/")
    assert "https://example.com/about" in result.internal_links
    assert "https://external-site.com/partner" in result.external_links
    assert not any("mailto" in link for link in result.internal_links + result.external_links)
    assert not any("#skip" in link for link in result.internal_links + result.external_links)


def test_extract_images_and_alt_flag():
    result = extract(SAMPLE_HTML, "https://example.com/services", "https://example.com/")
    alts = {img["src"]: img["has_alt"] for img in result.images}
    assert alts["https://example.com/img/hero.jpg"] is True
    assert alts["https://example.com/img/logo.png"] is False


def test_extract_json_ld_and_og():
    result = extract(SAMPLE_HTML, "https://example.com/services", "https://example.com/")
    assert result.json_ld == [{"@type": "WebPage", "name": "Services"}]
    assert result.open_graph["title"] == "OmniFit Services"


def test_extract_word_count_and_text():
    result = extract(SAMPLE_HTML, "https://example.com/services", "https://example.com/")
    assert result.word_count > 0
    assert "OmniFit" in result.text_content
