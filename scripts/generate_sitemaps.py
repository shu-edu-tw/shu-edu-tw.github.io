#!/usr/bin/env python3
"""Generate standard and Google News sitemaps from repo content."""
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path
from typing import Iterable, List, Tuple

BASE_URL = "https://shu-edu-tw.github.io"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT_MAIN = ROOT / "sitemap.xml"
OUTPUT_NEWS = ROOT / "news-sitemap.xml"
NEWS_MANIFEST = ROOT / "js" / "news-manifest.json"

STATIC_PAGES: List[Tuple[str, str, float]] = [
    ("index.html", "weekly", 1.0),
    ("pages/about.html", "monthly", 0.8),
    ("pages/academics.html", "monthly", 0.9),
    ("pages/faculty.html", "monthly", 0.7),
    ("pages/courses.html", "monthly", 0.7),
    ("pages/admissions.html", "weekly", 0.9),
    ("pages/campus-life.html", "monthly", 0.8),
    ("pages/alumni.html", "monthly", 0.7),
    ("pages/news.html", "weekly", 0.9),
    ("pages/contact.html", "yearly", 0.6),
]

PUBLISHER_NAME = "世新大學"
LANGUAGE = "zh-tw"


def _file_lastmod(path: Path) -> str:
    timestamp = path.stat().st_mtime
    dt_utc = _dt.datetime.fromtimestamp(timestamp, _dt.timezone.utc)
    return dt_utc.strftime("%Y-%m-%d")


def build_standard_entries() -> List[str]:
    entries: List[str] = []
    for rel_path, changefreq, priority in STATIC_PAGES:
        file_path = ROOT / rel_path
        if not file_path.exists():
            continue
        lastmod = _file_lastmod(file_path)
        if rel_path == "index.html":
            url = f"{BASE_URL}/index.html"
        else:
            url = f"{BASE_URL}/{rel_path}"
        entries.append(
            f"  <url>\n"
            f"    <loc>{url}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>{changefreq}</changefreq>\n"
            f"    <priority>{priority:.1f}</priority>\n"
            f"  </url>"
        )

    # Include news articles as well
    for news in load_news_entries():
        lastmod = news["date"]
        entries.append(
            f"  <url>\n"
            f"    <loc>{news['url']}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>monthly</changefreq>\n"
            f"    <priority>0.7</priority>\n"
            f"  </url>"
        )
    return entries


def load_news_entries() -> List[dict]:
    if not NEWS_MANIFEST.exists():
        return []
    data = json.loads(NEWS_MANIFEST.read_text(encoding="utf-8"))
    formatted = []
    for entry in data:
        url = entry.get("url", "").replace("../", "/")
        formatted.append(
            {
                "title": entry.get("title", ""),
                "date": entry.get("date", ""),
                "url": f"{BASE_URL}{url}",
            }
        )
    # sort by date desc
    formatted.sort(key=lambda item: item["date"], reverse=True)
    return formatted


def write_standard_sitemap(entries: Iterable[str]) -> None:
    body = "\n".join(entries)
    contents = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n\n"
        f"{body}\n\n"
        "</urlset>\n"
    )
    OUTPUT_MAIN.write_text(contents, encoding="utf-8")


def write_news_sitemap(news_entries: List[dict]) -> None:
    news_entries = news_entries[:100]  # per Google News guidelines
    blocks: List[str] = []
    for entry in news_entries:
        publication_date = entry["date"]
        blocks.append(
            "  <url>\n"
            f"    <loc>{entry['url']}</loc>\n"
            f"    <news:news>\n"
            f"      <news:publication>\n"
            f"        <news:name>{PUBLISHER_NAME}</news:name>\n"
            f"        <news:language>{LANGUAGE}</news:language>\n"
            f"      </news:publication>\n"
            f"      <news:publication_date>"
            f"{publication_date}"
            f"</news:publication_date>\n"
            f"      <news:title>{entry['title']}</news:title>\n"
            f"    </news:news>\n"
            "  </url>"
        )
    body = "\n".join(blocks)
    contents = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\" \n"
        "        xmlns:news=\"http://www.google.com/schemas/"
        "sitemap-news/0.9\">\n\n"
        f"{body}\n\n"
        "</urlset>\n"
    )
    OUTPUT_NEWS.write_text(contents, encoding="utf-8")


def main() -> None:
    news_entries = load_news_entries()
    write_standard_sitemap(build_standard_entries())
    write_news_sitemap(news_entries)
    main_path = OUTPUT_MAIN.relative_to(ROOT)
    news_path = OUTPUT_NEWS.relative_to(ROOT)
    print(f"Wrote {main_path} and {news_path}")


if __name__ == "__main__":
    main()
