from __future__ import annotations

import json
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from app.crawler.normalize import is_crawlable_scheme, is_same_registrable_domain, normalize_url


@dataclass
class ExtractedPage:
    title: str | None = None
    meta_description: str | None = None
    canonical: str | None = None
    h1: list[str] = field(default_factory=list)
    h2: list[str] = field(default_factory=list)
    h3: list[str] = field(default_factory=list)
    word_count: int = 0
    text_content: str = ""
    internal_links: list[str] = field(default_factory=list)
    external_links: list[str] = field(default_factory=list)
    images: list[dict] = field(default_factory=list)
    json_ld: list[dict] = field(default_factory=list)
    open_graph: dict = field(default_factory=dict)
    robots_meta: str | None = None
    lang: str | None = None


_NOISE_TAGS = ("script", "style", "noscript", "template", "svg")


def extract(html: str, page_url: str, root_url: str) -> ExtractedPage:
    soup = BeautifulSoup(html, "lxml")
    out = ExtractedPage()

    title_tag = soup.find("title")
    out.title = title_tag.get_text(strip=True) if title_tag else None

    meta_desc = soup.find("meta", attrs={"name": "description"})
    out.meta_description = meta_desc.get("content", "").strip() if meta_desc else None

    canonical_tag = soup.find("link", attrs={"rel": "canonical"})
    if canonical_tag and canonical_tag.get("href"):
        out.canonical = normalize_url(canonical_tag["href"], base=page_url)

    robots_tag = soup.find("meta", attrs={"name": "robots"})
    out.robots_meta = robots_tag.get("content", "").strip().lower() if robots_tag else None

    html_tag = soup.find("html")
    out.lang = html_tag.get("lang") if html_tag else None

    out.h1 = [h.get_text(strip=True) for h in soup.find_all("h1")]
    out.h2 = [h.get_text(strip=True) for h in soup.find_all("h2")]
    out.h3 = [h.get_text(strip=True) for h in soup.find_all("h3")]

    for meta in soup.find_all("meta"):
        prop = meta.get("property", "")
        if prop.startswith("og:"):
            out.open_graph[prop[3:]] = meta.get("content", "")

    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(script.string or "{}")
            if isinstance(data, list):
                out.json_ld.extend([d for d in data if isinstance(d, dict)])
            elif isinstance(data, dict):
                out.json_ld.append(data)
        except (json.JSONDecodeError, TypeError):
            continue

    body = soup.find("body") or soup
    for tag in body.find_all(_NOISE_TAGS):
        tag.decompose()
    text = " ".join(body.get_text(" ").split())
    out.text_content = text
    out.word_count = len(text.split())

    seen_links: set[str] = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        absolute = urljoin(page_url, href)
        if not is_crawlable_scheme(absolute):
            continue
        normalized = normalize_url(absolute)
        if normalized in seen_links:
            continue
        seen_links.add(normalized)
        if is_same_registrable_domain(normalized, root_url):
            out.internal_links.append(normalized)
        else:
            out.external_links.append(normalized)

    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if not src:
            continue
        out.images.append(
            {
                "src": urljoin(page_url, src),
                "alt": img.get("alt"),
                "has_alt": img.get("alt") is not None and img.get("alt").strip() != "",
            }
        )

    return out
