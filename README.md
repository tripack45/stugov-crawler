# CMU GSA Website Crawler

A Python crawler that discovers all pages under
[https://www.cmu.edu/stugov/gsa/](https://www.cmu.edu/stugov/gsa/) and
records every link found on each page.

## How it works

The crawler performs a breadth-first traversal starting from the GSA homepage.
For every HTML page it visits, it extracts all `<a href="...">` links along with
their visible text. Links that fall under the GSA URL prefix are added to the
crawl queue; all discovered links (internal and external) are recorded in the
output.

Key behaviors:

- **Scoped crawling** — only follows links under `https://www.cmu.edu/stugov/gsa/`.
- **Polite rate-limiting** — waits 0.5 seconds between requests.
- **Fragment & duplicate handling** — strips URL fragments and avoids revisiting pages.
- **Structured output** — writes JSON to stdout mapping each page to its list of links.

## Setup

Requires Python 3.10+.

```bash
pip install -r requirements.txt
```

## Usage

```bash
python crawler.py [OPTIONS] > results.json
```

### Options

| Option | Description |
|---|---|
| `--max-depth N` | Maximum link depth to follow from the start page. Depth 0 is the start page itself, depth 1 is pages linked from it, etc. Default: unlimited. |

### Examples

Crawl the entire GSA site:

```bash
python crawler.py > results.json
```

Crawl only up to 2 levels deep:

```bash
python crawler.py --max-depth 2 > results.json
```

## Output format

The crawler writes JSON to stdout. Progress and errors are logged to stderr.

```json
{
  "https://www.cmu.edu/stugov/gsa/": [
    {"url": "https://www.cmu.edu/stugov/gsa/about/", "text": "About Us"},
    {"url": "https://www.cmu.edu/stugov/gsa/events/", "text": "Events"},
    {"url": "https://www.cmu.edu/index.html"},
    {"url": "mailto:gsa@cmu.edu", "text": "Contact Us"}
  ],
  "https://www.cmu.edu/stugov/gsa/about/": [
    {"url": "https://www.cmu.edu/stugov/gsa/", "text": "Home"},
    {"url": "https://example.com/external-link", "text": "External Resource"}
  ]
}
```

Each key is a crawled page URL. Its value is a list of link objects found on that
page (both internal, external, and `mailto:` links). Each link object has a
`"url"` field and an optional `"text"` field containing the visible link text
(omitted when the link has no text content).
