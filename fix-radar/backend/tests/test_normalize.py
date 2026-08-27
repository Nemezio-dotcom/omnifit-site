from app.crawler.normalize import is_crawlable_scheme, is_same_registrable_domain, normalize_url


def test_normalize_strips_fragment_and_trailing_slash():
    assert normalize_url("https://example.com/page/#section") == "https://example.com/page"


def test_normalize_lowercases_host():
    assert normalize_url("https://EXAMPLE.com/Page") == "https://example.com/Page"


def test_normalize_resolves_relative_against_base():
    assert normalize_url("/about", base="https://example.com/blog/post") == "https://example.com/about"


def test_normalize_strips_tracking_params():
    assert normalize_url("https://example.com/?utm_source=x&keep=1") == "https://example.com/?keep=1"


def test_normalize_root_path_keeps_single_slash():
    assert normalize_url("https://example.com") == "https://example.com/"


def test_same_registrable_domain_ignores_www():
    assert is_same_registrable_domain("https://www.example.com/a", "https://example.com/")
    assert not is_same_registrable_domain("https://other.com/a", "https://example.com/")


def test_crawlable_scheme():
    assert is_crawlable_scheme("https://example.com")
    assert is_crawlable_scheme("http://example.com")
    assert not is_crawlable_scheme("mailto:a@example.com")
    assert not is_crawlable_scheme("javascript:void(0)")
    assert not is_crawlable_scheme("ftp://example.com/file")
