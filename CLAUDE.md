# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A single-file Python crawler that discovers all pages under `https://www.cmu.edu/stugov/gsa/` and records every link found on each page. It performs a BFS traversal, outputs JSON to stdout, and logs progress to stderr.

## Setup & Running

```bash
# Install dependencies (Python 3.10+ required)
pip install -r requirements.txt

# Run the crawler (output goes to stdout, progress to stderr)
python crawler.py > results.json
python crawler.py --max-depth 2 > results.json
```

## Architecture

The entire codebase is `crawler.py` — a single script with no tests or build system. Key components:

- `crawl(max_depth)` — BFS loop using `collections.deque`; visits only URLs under `BASE_URL`; respects a 0.5s rate limit between requests
- `normalize(url)` — strips fragments and whitespace
- `is_under_base(url)` — scope check against `BASE_URL`
- Output is a JSON dict mapping each crawled page URL to a list of link objects (`{"url": "...", "text": "..."}`) where `text` is included only when the link has visible text

Dependencies: `requests`, `beautifulsoup4` (html.parser backend).
