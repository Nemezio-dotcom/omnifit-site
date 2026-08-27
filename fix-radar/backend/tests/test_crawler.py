from app.crawler.crawler import Crawler


def test_crawl_fixture_site(fixture_server_url):
    crawler = Crawler(
        fixture_server_url,
        user_agent="FixRadarTest/1.0",
        max_pages=100,
        max_depth=4,
        allow_private_hosts=True,
        check_external_links=False,
    )
    result = crawler.crawl()

    assert len(result.pages) > 10
    assert result.robots_txt_found
    assert len(result.sitemap_urls) > 0

    ok_pages = [p for p in result.pages if p.status_code == 200]
    assert len(ok_pages) > 10

    services_page = next((p for p in ok_pages if p.url.endswith("/personal-training-services")), None)
    assert services_page is not None
    assert services_page.title
    assert services_page.word_count > 50
    assert any(services_page.json_ld)


def test_crawl_respects_max_pages(fixture_server_url):
    crawler = Crawler(
        fixture_server_url, user_agent="FixRadarTest/1.0", max_pages=3, max_depth=4,
        allow_private_hosts=True, check_external_links=False,
    )
    result = crawler.crawl()
    assert len(result.pages) <= 3


def test_orphan_detection(fixture_server_url):
    crawler = Crawler(
        fixture_server_url, user_agent="FixRadarTest/1.0", max_pages=100, max_depth=4,
        allow_private_hosts=True, check_external_links=False,
    )
    result = crawler.crawl()
    root = next(p for p in result.pages if p.normalized_url == crawler.root_url)
    assert root.is_orphan is False  # root is exempt from orphan status by definition
