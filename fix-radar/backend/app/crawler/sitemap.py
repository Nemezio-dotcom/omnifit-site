from __future__ import annotations

from urllib.parse import urljoin

from lxml import etree

from app.crawler.fetcher import HttpFetcher
from app.crawler.normalize import normalize_url


def discover_sitemap_urls(fetcher: HttpFetcher, base_url: str, robots_sitemaps: list[str]) -> list[str]:
    """Try robots.txt-declared sitemaps first, then the conventional /sitemap.xml."""
    candidates = list(robots_sitemaps) or [urljoin(base_url, "/sitemap.xml")]
    urls: list[str] = []
    seen_sitemaps: set[str] = set()

    def parse_sitemap(sm_url: str, depth: int = 0) -> None:
        if sm_url in seen_sitemaps or depth > 2:
            return
        seen_sitemaps.add(sm_url)
        result = fetcher.fetch(sm_url)
        if result.status_code != 200 or not result.body:
            return
        try:
            root = etree.fromstring(result.body.encode("utf-8"))
        except etree.XMLSyntaxError:
            return
        tag = etree.QName(root).localname
        if tag == "sitemapindex":
            for loc in root.iter():
                if etree.QName(loc).localname == "loc" and loc.text:
                    parse_sitemap(loc.text.strip(), depth + 1)
        elif tag == "urlset":
            for loc in root.iter():
                if etree.QName(loc).localname == "loc" and loc.text:
                    urls.append(normalize_url(loc.text.strip()))

    for c in candidates:
        parse_sitemap(c)
    return urls
