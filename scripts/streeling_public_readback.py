"""Read back deployed Streeling pages anonymously against one Demerzel commit.

Example:
    python scripts/streeling_public_readback.py \
        --sha 0f7a5fd110acfc4835776d38ab1a115533467d34 \
        --module network-science/net-001-scale-free-tool-networks

This checks the live index source link, each page's source link, and the first
rendered heading against the pinned source. It does not establish review,
pedagogical quality, or that a learner completed the course.
"""

import argparse
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


SOURCE_ROOT = "state/streeling/courses"
REPO_URL = "https://github.com/GuitarAlchemist/Demerzel"
DEFAULT_SITE_ROOT = "https://spareilleux.github.io/learn/"
MODULE_PATTERN = re.compile(r"^[a-z0-9-]+/[a-z0-9-]+$")
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = set()
        self.headings = []
        self._in_h1 = False
        self._heading = ""

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.add(href)
        elif tag == "h1":
            self._in_h1 = True
            self._heading = ""

    def handle_data(self, data):
        if self._in_h1:
            self._heading += data

    def handle_endtag(self, tag):
        if tag == "h1" and self._in_h1:
            self.headings.append(self._heading.strip())
            self._in_h1 = False


def fetch(url):
    request = Request(url, headers={"User-Agent": "StreelingPublicReadback/1.0"})
    try:
        with urlopen(request, timeout=15) as response:
            body = response.read().decode("utf-8")
            page = PageParser()
            page.feed(body)
            return {"status": response.status, "links": page.links, "h1": page.headings[:1]}
    except HTTPError as exc:
        return {"status": exc.code, "error": str(exc)}
    except (URLError, TimeoutError, UnicodeDecodeError) as exc:
        return {"status": None, "error": str(exc)}


def source_heading(sha, source_path):
    result = subprocess.run(
        ["git", "show", f"{sha}:{source_path}"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    for line in result.stdout.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError(f"No level-one heading in {source_path} at {sha}")


def check_index(site_root, sha):
    url = urljoin(site_root, "streeling/")
    page = fetch(url)
    expected_link = f"{REPO_URL}/tree/{sha}/{SOURCE_ROOT}"
    return {
        "url": url,
        "status": page["status"],
        "source_link_matches": expected_link in page.get("links", set()),
        "ok": page["status"] == 200 and expected_link in page.get("links", set()),
        **({"error": page["error"]} if "error" in page else {}),
    }


def check_module(site_root, sha, module, lang):
    department, stem = module.split("/", 1)
    locale_prefix = "" if lang == "en" else f"{lang}/"
    url = urljoin(site_root, f"{locale_prefix}streeling/{department}/{stem}/")
    source_file = f"{stem}.md" if lang == "en" else f"{stem}.{lang}.md"
    source_path = f"{SOURCE_ROOT}/{department}/{lang}/{source_file}"
    expected_link = f"{REPO_URL}/blob/{sha}/{source_path}"
    expected_heading = source_heading(sha, source_path)
    page = fetch(url)
    rendered_heading = page.get("h1", [None])[0] if page.get("h1") else None
    link_matches = expected_link in page.get("links", set())
    return {
        "module": module,
        "language": lang,
        "url": url,
        "status": page["status"],
        "source_link_matches": link_matches,
        "heading_matches": expected_heading == rendered_heading,
        "expected_heading": expected_heading,
        "rendered_heading": rendered_heading,
        "ok": page["status"] == 200 and link_matches and expected_heading == rendered_heading,
        **({"error": page["error"]} if "error" in page else {}),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sha", required=True, help="Full Demerzel source commit SHA")
    parser.add_argument("--module", action="append", required=True, help="department/module-stem; repeat for a batch")
    parser.add_argument("--locale", nargs="+", choices=("en", "fr", "es"), default=["en"])
    parser.add_argument("--site-root", default=DEFAULT_SITE_ROOT)
    parser.add_argument("--workers", type=int, default=4, help="Concurrent page requests, from 1 to 8")
    args = parser.parse_args()
    if not SHA_PATTERN.fullmatch(args.sha):
        parser.error("--sha must be a full lowercase 40-character Git commit SHA")
    if any(not MODULE_PATTERN.fullmatch(module) for module in args.module):
        parser.error("each --module must be department/module-stem with lowercase letters, digits, or hyphens")
    if not 1 <= args.workers <= 8:
        parser.error("--workers must be between 1 and 8")
    site_root = args.site_root.rstrip("/") + "/"
    try:
        index = check_index(site_root, args.sha)
        targets = [(module, lang) for module in args.module for lang in args.locale]
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            modules = list(executor.map(lambda target: check_module(site_root, args.sha, *target), targets))
    except (subprocess.CalledProcessError, ValueError) as exc:
        parser.error(f"Could not load pinned source: {exc}")
    receipt = {
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "site_root": site_root,
        "source_revision": args.sha,
        "index": index,
        "modules": modules,
        "ok": index["ok"] and all(item["ok"] for item in modules),
        "scope": "Anonymous HTTP provenance and rendered-title readback only; not review or learner evidence",
    }
    print(json.dumps(receipt, indent=2, ensure_ascii=True))
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
