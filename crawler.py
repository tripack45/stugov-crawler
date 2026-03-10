#!/usr/bin/env python3
"""Crawl all pages under https://www.cmu.edu/stugov/gsa/ and list their links."""

import argparse
import json
import sys
import time
from collections import deque
from urllib.parse import urljoin, urldefrag

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.cmu.edu/stugov/gsa/"
DELAY = 0.5  # seconds between requests to be polite


def is_under_base(url: str) -> bool:
    return url.startswith(BASE_URL)


def normalize(url: str) -> str:
    """Remove fragment and trailing whitespace."""
    url, _ = urldefrag(url)
    return url.strip()


def crawl(max_depth: int | None = None):
    visited: set[str] = set()
    queue: deque[tuple[str, int]] = deque([(BASE_URL, 0)])
    results: dict[str, list[dict[str, str]]] = {}

    session = requests.Session()
    session.headers.update({"User-Agent": "CMU-GSA-Crawler/1.0 (student project)"})

    while queue:
        url, depth = queue.popleft()
        if url in visited:
            continue
        visited.add(url)

        print(f"Crawling (depth {depth}): {url}", file=sys.stderr)
        try:
            resp = session.get(url, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  Error: {e}", file=sys.stderr)
            results[url] = []
            continue

        content_type = resp.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        links: list[dict[str, str]] = []

        for tag in soup.find_all("a", href=True):
            href = normalize(urljoin(url, tag["href"]))
            if not href or href.startswith(("tel:", "javascript:")):
                continue
            link_entry: dict[str, str] = {"url": href}
            text = tag.get_text(strip=True)
            if text:
                link_entry["text"] = text
            links.append(link_entry)
            if is_under_base(href) and href not in visited:
                if max_depth is None or depth < max_depth:
                    queue.append((href, depth + 1))

        results[url] = links
        time.sleep(DELAY)

    return results


def main():
    parser = argparse.ArgumentParser(description="Crawl CMU GSA website pages.")
    parser.add_argument(
        "--max-depth", type=int, default=None,
        help="Maximum link depth to follow (default: unlimited)",
    )
    args = parser.parse_args()

    results = crawl(max_depth=args.max_depth)

    print(f"\n{'=' * 60}", file=sys.stderr)
    print(f"Crawled {len(results)} page(s).\n", file=sys.stderr)

    # Write structured JSON to stdout
    json.dump(results, sys.stdout, indent=2)
    print()  # trailing newline


if __name__ == "__main__":
    main()
