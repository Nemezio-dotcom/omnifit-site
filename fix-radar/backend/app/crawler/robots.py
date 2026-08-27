from __future__ import annotations

from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import httpx


class RobotsPolicy:
    """Thin wrapper so the crawler can ask "can I fetch this?" and also read
    sitemap URLs, without caring whether robots.txt was reachable."""

    def __init__(self, base_url: str, user_agent: str):
        self.base_url = base_url
        self.user_agent = user_agent
        self._parser = RobotFileParser()
        self._loaded = False
        # An unparsed RobotFileParser.can_fetch() defaults to DENY, not allow --
        # so "robots.txt not found/unreachable" must be tracked separately and
        # short-circuit to "everything allowed", rather than falling through to
        # the parser (which would silently block the entire crawl).
        self._rules_found = False
        self.sitemap_urls: list[str] = []

    def load(self, client: httpx.Client) -> None:
        robots_url = urljoin(self.base_url, "/robots.txt")
        try:
            resp = client.get(robots_url, timeout=10)
            if resp.status_code >= 400:
                # No robots.txt => everything allowed by convention.
                self._loaded = True
                return
            lines = resp.text.splitlines()
            self._parser.parse(lines)
            self._loaded = True
            self._rules_found = True
            self.sitemap_urls = [
                line.split(":", 1)[1].strip()
                for line in lines
                if line.lower().startswith("sitemap:")
            ]
        except httpx.HTTPError:
            # Fail open: treat as "no robots.txt found", not "block everything".
            self._loaded = True

    def can_fetch(self, url: str) -> bool:
        if not self._loaded or not self._rules_found:
            return True
        try:
            return self._parser.can_fetch(self.user_agent, url)
        except Exception:
            return True
