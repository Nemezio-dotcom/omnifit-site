import httpx

from app.crawler.robots import RobotsPolicy


class _RaisingTransport(httpx.BaseTransport):
    def handle_request(self, request):
        raise httpx.ConnectError("simulated egress block", request=request)


class _NotFoundTransport(httpx.BaseTransport):
    def handle_request(self, request):
        return httpx.Response(404, request=request)


class _RulesTransport(httpx.BaseTransport):
    def handle_request(self, request):
        body = b"User-agent: *\nDisallow: /private\nSitemap: https://example.com/sitemap.xml\n"
        return httpx.Response(200, content=body, request=request)


def test_can_fetch_defaults_to_allow_when_robots_txt_unreachable():
    """Regression test: an unparsed RobotFileParser denies by default, so a
    network failure fetching robots.txt must not silently block the whole crawl."""
    client = httpx.Client(transport=_RaisingTransport())
    policy = RobotsPolicy("https://example.com/", "TestAgent")
    policy.load(client)
    assert policy.can_fetch("https://example.com/") is True
    assert policy.can_fetch("https://example.com/anything") is True


def test_can_fetch_defaults_to_allow_on_404():
    client = httpx.Client(transport=_NotFoundTransport())
    policy = RobotsPolicy("https://example.com/", "TestAgent")
    policy.load(client)
    assert policy.can_fetch("https://example.com/") is True


def test_can_fetch_respects_real_disallow_rules():
    client = httpx.Client(transport=_RulesTransport())
    policy = RobotsPolicy("https://example.com/", "TestAgent")
    policy.load(client)
    assert policy.can_fetch("https://example.com/private/page") is False
    assert policy.can_fetch("https://example.com/public") is True
    assert policy.sitemap_urls == ["https://example.com/sitemap.xml"]
