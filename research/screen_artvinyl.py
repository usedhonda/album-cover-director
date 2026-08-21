#!/usr/bin/env python3
"""Build a temporary visual-screening sheet from Best Art Vinyl archive pages.

The archive supplies cover-specific award evidence and design credits. This
helper writes metadata and thumbnails only to an explicit output directory;
never point it at the repository. Third-party images remain research inputs
and must not be committed or redistributed.
"""

from __future__ import annotations

import argparse
import io
import json
import textwrap
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path


USER_AGENT = "album-cover-director-research/0.1 (+https://github.com/usedhonda/album-cover-director)"
ROOT = Path(__file__).resolve().parents[1]
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class ArchiveParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.item_depth: int | None = None
        self.item: dict[str, str] | None = None
        self.capture_tag: str | None = None
        self.capture: list[str] = []
        self.heading: str | None = None
        self.items: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        classes = set((attr.get("class") or "").split())
        if tag == "div" and "bestitem" in classes and self.item is None:
            self.item_depth = len(self.stack) + 1
            self.item = {}
        if tag not in VOID_TAGS:
            self.stack.append(tag)
        if self.item is None:
            return
        if tag == "img" and attr.get("src"):
            self.item["image_url"] = str(attr["src"])
        if tag in {"h5", "p"}:
            self.capture_tag = tag
            self.capture = []

    def handle_data(self, data: str) -> None:
        if self.capture_tag:
            value = " ".join(data.split())
            if value:
                self.capture.append(value)

    def handle_endtag(self, tag: str) -> None:
        if self.capture_tag == tag and self.item is not None:
            value = " ".join(self.capture).strip()
            if tag == "h5":
                self.heading = value.lower()
            elif self.heading and value:
                self.item[self.heading] = value
            self.capture_tag = None
            self.capture = []
        if self.item is not None and tag == "div" and len(self.stack) == self.item_depth:
            if self.item.get("artist") and self.item.get("title"):
                self.items.append(self.item)
            self.item = None
            self.item_depth = None
            self.heading = None
        if tag not in VOID_TAGS and self.stack:
            self.stack.pop()


def fetch(url: str) -> bytes:
    for attempt in range(4):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            if exc.code not in {429, 502, 503, 504} or attempt == 3:
                raise
            retry_after = exc.headers.get("Retry-After")
            delay = float(retry_after) if retry_after and retry_after.isdigit() else 5.0 * (2 ** attempt)
            time.sleep(delay)
    raise RuntimeError(f"unreachable retry state for {url}")


def fetch_year(year: int) -> list[dict[str, object]]:
    source_url = f"https://artvinyl.com/award-year/{year}/"
    parser = ArchiveParser()
    parser.feed(fetch(source_url).decode("utf-8", errors="replace"))
    seen: set[tuple[str, str]] = set()
    records: list[dict[str, object]] = []
    for index, item in enumerate(parser.items, start=1):
        key = (item["artist"], item["title"])
        if key in seen:
            continue
        seen.add(key)
        records.append({
            "year": year,
            "rank": index if index <= 3 else None,
            "artist": item["artist"],
            "title": item["title"],
            "label": item.get("label", ""),
            "design_credit": item.get("design", ""),
            "source_url": source_url,
            "image_url": item.get("image_url", ""),
        })
    return records


def require_external_output(path: Path) -> Path:
    """Keep downloaded third-party metadata and images outside the repository."""
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError:
        return resolved
    raise SystemExit("--out-dir must be outside the repository; research images are not redistributable")


def make_sheet(records: list[dict[str, object]], output: Path) -> None:
    try:
        from PIL import Image, ImageDraw, ImageOps
    except ImportError as exc:
        raise SystemExit("Pillow is required for --sheet") from exc

    cell_w, cell_h, image_size, columns = 240, 290, 210, 5
    rows = (len(records) + columns - 1) // columns
    sheet = Image.new("RGB", (cell_w * columns, cell_h * rows), "#f4f2ed")

    def load_image(record: dict[str, object]):
        raw = fetch(str(record["image_url"]))
        return Image.open(io.BytesIO(raw)).convert("RGB")

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(load_image, record) for record in records]
        for index, (record, future) in enumerate(zip(records, futures)):
            col, row = index % columns, index // columns
            x, y = col * cell_w, row * cell_h
            try:
                cover = ImageOps.fit(future.result(), (image_size, image_size))
                sheet.paste(cover, (x + 15, y + 10))
            except Exception:
                ImageDraw.Draw(sheet).rectangle((x + 15, y + 10, x + 225, y + 220), outline="#a00", width=3)
            label = f"{index + 1:02d} {record['artist']}\n{record['title']}"
            label = "\n".join(textwrap.wrap(label, width=34))
            ImageDraw.Draw(sheet).multiline_text((x + 15, y + 225), label, fill="#111", spacing=2)
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("years", nargs="+", type=int)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--sheet", action="store_true", help="download temporary thumbnails and create one sheet per year")
    parser.add_argument("--year-delay", type=float, default=2.0, help="seconds between archive-year requests")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.out_dir = require_external_output(args.out_dir)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for index, year in enumerate(args.years):
        if index:
            time.sleep(args.year_delay)
        records = fetch_year(year)
        if not records:
            raise SystemExit(f"no archive records parsed for {year}")
        metadata = args.out_dir / f"artvinyl-{year}.json"
        metadata.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n")
        if args.sheet:
            make_sheet(records, args.out_dir / f"artvinyl-{year}.jpg")
        print(f"{year}: {len(records)} records -> {metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
