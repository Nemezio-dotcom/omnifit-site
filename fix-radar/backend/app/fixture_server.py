"""
Local fixture crawl target.

This environment's network egress policy blocks outbound access to
omnifittraining.com (verified: both raw HTTPS and the harness's own fetch
tool return an egress-blocked error). Phase 21 of the Fix Radar spec calls
for scanning the LIVE site; since that's not reachable from here, this
module serves the repository's own real page source -- the exact HTML
fragments and per-page <head> JSON-LD injection blocks committed under
../pages -- over a local HTTP server, so the crawler can run against
genuine OmniFit content instead of anything fabricated.

Caveats, surfaced to the user in the dashboard (see dashboard_service.py):
 - There is no homepage fragment committed in this repo (it's managed
   directly in the site builder), so "/" here is a SYNTHETIC index page
   that just links to every real page -- it is not the actual homepage
   and is excluded from content/AIO findings.
 - Each page's title, meta description, canonical URL, and JSON-LD are
   read from the real "-header.html" page-header-injection files, which
   is exactly what's pasted into the live CMS. Anything not present in
   these committed files (e.g. rendered nav/footer widgets the CMS adds
   at runtime) is not part of this fixture.
"""

from __future__ import annotations

import json
import re
import threading
from functools import lru_cache
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

FIXTURE_PORT = 8934
LOCAL_FIXTURE_URL = f"http://127.0.0.1:{FIXTURE_PORT}/"

REPO_ROOT = Path(__file__).resolve().parents[3]
PAGES_DIR = REPO_ROOT / "pages"
HEADERS_DIR = PAGES_DIR / "headers"

_LD_JSON_RE = re.compile(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', re.DOTALL)


def _slug_title(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").title()


def _load_head_metadata(slug: str) -> dict:
    header_path = HEADERS_DIR / f"{slug}-header.html"
    meta = {"title": _slug_title(slug), "description": None, "canonical": None, "json_ld_raw": None}
    if not header_path.exists():
        return meta
    raw = header_path.read_text(encoding="utf-8", errors="ignore")
    match = _LD_JSON_RE.search(raw)
    if not match:
        return meta
    meta["json_ld_raw"] = match.group(1).strip()
    try:
        data = json.loads(meta["json_ld_raw"])
    except json.JSONDecodeError:
        return meta
    graph = data.get("@graph", [data]) if isinstance(data, dict) else []
    for node in graph:
        if isinstance(node, dict) and node.get("@type") == "WebPage":
            meta["title"] = node.get("name") or meta["title"]
            meta["description"] = node.get("description")
            meta["canonical"] = node.get("url")
            break
    return meta


@lru_cache
def _discover_pages() -> dict[str, dict]:
    """slug -> {title, description, canonical, json_ld_raw, body_fragment}"""
    pages = {}
    if not PAGES_DIR.exists():
        return pages
    for path in sorted(PAGES_DIR.glob("*.html")):
        if path.name == "footer.html":
            continue
        slug = path.stem
        body = path.read_text(encoding="utf-8", errors="ignore")
        pages[slug] = {**_load_head_metadata(slug), "body_fragment": body}
    return pages


@lru_cache
def _footer_fragment() -> str:
    footer_path = PAGES_DIR / "footer.html"
    if footer_path.exists():
        return footer_path.read_text(encoding="utf-8", errors="ignore")
    return ""


def _render_page(slug: str, meta: dict) -> str:
    head_bits = [f"<title>{meta['title']}</title>"]
    if meta["description"]:
        head_bits.append(f'<meta name="description" content="{meta["description"]}">')
    if meta["canonical"]:
        head_bits.append(f'<link rel="canonical" href="{meta["canonical"]}">')
    if meta["json_ld_raw"]:
        head_bits.append(f'<script type="application/ld+json">{meta["json_ld_raw"]}</script>')
    return (
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        + "".join(head_bits)
        + "</head><body>"
        + meta["body_fragment"]
        + _footer_fragment()
        + "</body></html>"
    )


def _render_index(pages: dict[str, dict]) -> str:
    links = "".join(f'<li><a href="/{slug}">{p["title"]}</a></li>' for slug, p in pages.items())
    return (
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<title>OmniFit Fix Radar -- local fixture index</title>"
        "<meta name=\"description\" content=\"Synthetic index for local crawling. Not the real OmniFit homepage.\">"
        "</head><body><main>"
        "<h1>Local fixture index (not the real homepage)</h1>"
        f"<ul>{links}</ul>"
        "</main></body></html>"
    )


def _render_sitemap(pages: dict[str, dict]) -> str:
    urls = "".join(f"<url><loc>{LOCAL_FIXTURE_URL}{slug}</loc></url>" for slug in pages)
    return f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *args) -> None:  # silence default stderr logging
        pass

    def do_GET(self) -> None:
        pages = _discover_pages()
        path = self.path.split("?")[0].strip("/")

        if path in ("", "index"):
            body, content_type = _render_index(pages), "text/html; charset=utf-8"
        elif path == "robots.txt":
            body, content_type = f"User-agent: *\nAllow: /\nSitemap: {LOCAL_FIXTURE_URL}sitemap.xml\n", "text/plain"
        elif path == "sitemap.xml":
            body, content_type = _render_sitemap(pages), "application/xml"
        elif path in pages:
            body, content_type = _render_page(path, pages[path]), "text/html; charset=utf-8"
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not found")
            return

        encoded = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


_server_lock = threading.Lock()
_server_started = False


def ensure_fixture_server_running() -> None:
    global _server_started
    with _server_lock:
        if _server_started:
            return
        server = ThreadingHTTPServer(("127.0.0.1", FIXTURE_PORT), _Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        _server_started = True
