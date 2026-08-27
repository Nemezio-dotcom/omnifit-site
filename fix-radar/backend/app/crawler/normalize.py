from urllib.parse import urldefrag, urljoin, urlparse, urlunparse

_TRACKING_PREFIXES = ("utm_", "gclid", "fbclid", "mc_", "ref")


def normalize_url(url: str, base: str | None = None) -> str:
    """Canonicalize a URL for de-duplication and crawl-queue comparisons.

    - resolves relative URLs against `base`
    - lowercases scheme/host
    - drops fragments
    - drops known tracking query params
    - strips a single trailing slash (except for the bare root path)
    - drops default ports
    """
    if base:
        url = urljoin(base, url)
    url, _frag = urldefrag(url)
    parsed = urlparse(url)

    scheme = parsed.scheme.lower() or "https"
    netloc = parsed.netloc.lower()
    if netloc.endswith(":80") and scheme == "http":
        netloc = netloc[:-3]
    if netloc.endswith(":443") and scheme == "https":
        netloc = netloc[:-4]

    path = parsed.path or "/"
    if len(path) > 1 and path.endswith("/"):
        path = path[:-1]

    query_pairs = [
        kv for kv in parsed.query.split("&") if kv and not kv.split("=")[0].lower().startswith(_TRACKING_PREFIXES)
    ]
    query = "&".join(sorted(query_pairs))

    return urlunparse((scheme, netloc, path, "", query, ""))


def is_same_registrable_domain(url: str, root_url: str) -> bool:
    """Treat www/apex as the same site; anything else counts as external."""
    host_a = urlparse(url).netloc.lower().split(":")[0]
    host_b = urlparse(root_url).netloc.lower().split(":")[0]

    def strip_www(h: str) -> str:
        return h[4:] if h.startswith("www.") else h

    return strip_www(host_a) == strip_www(host_b)


def is_crawlable_scheme(url: str) -> bool:
    return urlparse(url).scheme in ("http", "https")
