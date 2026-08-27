from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from app.crawler.extractor import extract
from app.crawler.fetcher import HttpFetcher, SSRFBlockedError
from app.crawler.normalize import is_crawlable_scheme, is_same_registrable_domain, normalize_url
from app.crawler.robots import RobotsPolicy
from app.crawler.sitemap import discover_sitemap_urls


@dataclass
class CrawledPage:
    url: str
    normalized_url: str
    status_code: int
    response_time_ms: float
    content_type: str
    final_url: str
    redirect_chain: list[str]
    depth: int
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
    is_indexable: bool = True
    in_sitemap: bool = False
    inbound_internal_link_count: int = 0
    is_orphan: bool = False
    fetch_error: str | None = None


@dataclass
class CrawlResult:
    pages: list[CrawledPage]
    broken_internal_links: list[dict]  # {from_url, to_url, status_code}
    external_link_checks: list[dict]  # {from_url, to_url, status_code, ok}
    sitemap_urls: list[str]
    robots_txt_found: bool
    root_url: str
    truncated: bool  # hit max_pages before the frontier was empty


class Crawler:
    def __init__(
        self,
        root_url: str,
        *,
        user_agent: str,
        max_pages: int = 200,
        max_depth: int = 6,
        timeout_ms: int = 15000,
        allow_private_hosts: bool = False,
        check_external_links: bool = True,
        max_external_link_checks: int = 40,
    ):
        self.root_url = normalize_url(root_url)
        self.user_agent = user_agent
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.timeout_ms = timeout_ms
        self.allow_private_hosts = allow_private_hosts
        self.check_external_links = check_external_links
        self.max_external_link_checks = max_external_link_checks

    def crawl(self) -> CrawlResult:
        fetcher = HttpFetcher(self.user_agent, self.timeout_ms, allow_private=self.allow_private_hosts)
        robots = RobotsPolicy(self.root_url, self.user_agent)
        try:
            robots.load(fetcher.client)
        except Exception:
            pass

        sitemap_urls = []
        try:
            sitemap_urls = discover_sitemap_urls(fetcher, self.root_url, robots.sitemap_urls)
        except Exception:
            pass
        sitemap_set = set(sitemap_urls)

        visited: set[str] = set()
        queue: deque[tuple[str, int]] = deque([(self.root_url, 0)])
        pages: list[CrawledPage] = []
        inbound_counts: dict[str, int] = {}
        broken_internal: list[dict] = []
        truncated = False

        while queue:
            if len(visited) >= self.max_pages:
                truncated = bool(queue)
                break
            url, depth = queue.popleft()
            if url in visited:
                continue
            if depth > self.max_depth:
                continue
            if not is_crawlable_scheme(url):
                continue
            if not robots.can_fetch(url):
                continue

            visited.add(url)
            try:
                result = fetcher.fetch(url)
            except SSRFBlockedError as exc:
                pages.append(
                    CrawledPage(
                        url=url, normalized_url=url, status_code=0, response_time_ms=0,
                        content_type="", final_url=url, redirect_chain=[], depth=depth,
                        fetch_error=str(exc),
                    )
                )
                continue

            page = CrawledPage(
                url=url,
                normalized_url=url,
                status_code=result.status_code,
                response_time_ms=result.elapsed_ms,
                content_type=result.content_type,
                final_url=result.final_url,
                redirect_chain=result.redirect_chain,
                depth=depth,
                in_sitemap=url in sitemap_set,
                fetch_error=result.error,
            )

            if result.error or result.status_code >= 400 or result.status_code == 0:
                pages.append(page)
                continue

            if "html" not in result.content_type:
                pages.append(page)
                continue

            extracted = extract(result.body, result.final_url, self.root_url)
            page.title = extracted.title
            page.meta_description = extracted.meta_description
            page.canonical = extracted.canonical
            page.h1 = extracted.h1
            page.h2 = extracted.h2
            page.h3 = extracted.h3
            page.word_count = extracted.word_count
            page.text_content = extracted.text_content
            page.internal_links = extracted.internal_links
            page.external_links = extracted.external_links
            page.images = extracted.images
            page.json_ld = extracted.json_ld
            page.open_graph = extracted.open_graph
            page.robots_meta = extracted.robots_meta
            page.is_indexable = "noindex" not in (extracted.robots_meta or "")
            pages.append(page)

            for link in extracted.internal_links:
                inbound_counts[link] = inbound_counts.get(link, 0) + 1
                if link not in visited:
                    queue.append((link, depth + 1))

        for page in pages:
            page.inbound_internal_link_count = inbound_counts.get(page.normalized_url, 0)
            page.is_orphan = (
                page.inbound_internal_link_count == 0
                and page.normalized_url != self.root_url
                and page.status_code and page.status_code < 400
            )

        # broken internal links: a page links to a URL that we crawled and got 4xx/5xx
        status_by_url = {p.normalized_url: p.status_code for p in pages}
        for page in pages:
            for link in page.internal_links:
                status = status_by_url.get(link)
                if status is not None and status >= 400:
                    broken_internal.append({"from_url": page.normalized_url, "to_url": link, "status_code": status})

        external_checks: list[dict] = []
        if self.check_external_links:
            all_external = []
            seen_ext = set()
            for page in pages:
                for link in page.external_links:
                    if link not in seen_ext:
                        seen_ext.add(link)
                        all_external.append((page.normalized_url, link))
            for from_url, link in all_external[: self.max_external_link_checks]:
                try:
                    r = fetcher.fetch(link)
                    ok = bool(r.status_code) and r.status_code < 400
                    external_checks.append(
                        {"from_url": from_url, "to_url": link, "status_code": r.status_code, "ok": ok, "error": r.error}
                    )
                except SSRFBlockedError as exc:
                    external_checks.append(
                        {"from_url": from_url, "to_url": link, "status_code": 0, "ok": False, "error": str(exc)}
                    )

        fetcher.close()
        return CrawlResult(
            pages=pages,
            broken_internal_links=broken_internal,
            external_link_checks=external_checks,
            sitemap_urls=sitemap_urls,
            robots_txt_found=robots._loaded,
            root_url=self.root_url,
            truncated=truncated,
        )
