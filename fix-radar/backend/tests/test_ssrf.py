import pytest

from app.crawler.fetcher import SSRFBlockedError, assert_safe_to_fetch


def test_blocks_non_http_scheme():
    with pytest.raises(SSRFBlockedError):
        assert_safe_to_fetch("file:///etc/passwd")


def test_blocks_ftp_scheme():
    with pytest.raises(SSRFBlockedError):
        assert_safe_to_fetch("ftp://example.com/file")


def test_blocks_loopback_by_default():
    with pytest.raises(SSRFBlockedError):
        assert_safe_to_fetch("http://127.0.0.1:8080/")


def test_blocks_private_network_by_default():
    with pytest.raises(SSRFBlockedError):
        assert_safe_to_fetch("http://10.0.0.5/")
    with pytest.raises(SSRFBlockedError):
        assert_safe_to_fetch("http://192.168.1.1/")


def test_allows_loopback_when_explicitly_permitted():
    assert_safe_to_fetch("http://127.0.0.1:8080/", allow_private=True)
