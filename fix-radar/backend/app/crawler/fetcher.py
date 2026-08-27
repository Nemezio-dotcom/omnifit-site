from __future__ import annotations

import ipaddress
import socket
import time
from dataclasses import dataclass
from urllib.parse import urlparse

import httpx


class SSRFBlockedError(Exception):
    pass


@dataclass
class FetchResult:
    url: str
    final_url: str
    status_code: int
    content_type: str
    body: str
    elapsed_ms: float
    redirect_chain: list[str]
    error: str | None = None


def _is_public_ip(host: str) -> bool:
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return False
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            return False
    return True


def assert_safe_to_fetch(url: str, *, allow_private: bool = False) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise SSRFBlockedError(f"Blocked non-HTTP(S) scheme: {parsed.scheme}")
    if not parsed.hostname:
        raise SSRFBlockedError("Blocked URL with no hostname")
    if allow_private:
        return
    if not _is_public_ip(parsed.hostname):
        raise SSRFBlockedError(f"Blocked request to non-public host: {parsed.hostname}")


class HttpFetcher:
    """httpx-based fetcher used for the vast majority of pages. Captures the
    full redirect chain and never follows a redirect off http/https."""

    def __init__(self, user_agent: str, timeout_ms: int, allow_private: bool = False):
        self.timeout = timeout_ms / 1000
        self.allow_private = allow_private
        self.client = httpx.Client(
            headers={"User-Agent": user_agent},
            follow_redirects=False,
            timeout=self.timeout,
            verify=True,
        )

    def close(self) -> None:
        self.client.close()

    def fetch(self, url: str, max_redirects: int = 5) -> FetchResult:
        chain: list[str] = []
        current = url
        start = time.perf_counter()
        for _ in range(max_redirects + 1):
            assert_safe_to_fetch(current, allow_private=self.allow_private)
            try:
                resp = self.client.get(current)
            except httpx.HTTPError as exc:
                elapsed = (time.perf_counter() - start) * 1000
                return FetchResult(url, current, 0, "", "", elapsed, chain, error=str(exc))

            if resp.status_code in (301, 302, 303, 307, 308) and "location" in resp.headers:
                chain.append(current)
                current = httpx.URL(current).join(resp.headers["location"]).human_repr()
                continue

            elapsed = (time.perf_counter() - start) * 1000
            content_type = resp.headers.get("content-type", "")
            binary_prefixes = ("image/", "video/", "audio/", "font/", "application/octet-stream", "application/pdf", "application/zip")
            body = ""
            if not any(content_type.startswith(p) for p in binary_prefixes):
                try:
                    body = resp.text
                except UnicodeDecodeError:
                    body = ""
            return FetchResult(
                url=url,
                final_url=current,
                status_code=resp.status_code,
                content_type=content_type,
                body=body,
                elapsed_ms=elapsed,
                redirect_chain=chain,
            )
        elapsed = (time.perf_counter() - start) * 1000
        return FetchResult(url, current, 0, "", "", elapsed, chain, error="Too many redirects")
