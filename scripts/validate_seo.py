#!/usr/bin/env python3
"""
Light SEO checks:
- Each HTML has canonical tag and correct domain/path
- No stray 'https://shu-edu-tw.github.io/home' references
- OG url matches canonical (if present)
Prints issues and exits non-zero if any are found.
"""
from __future__ import annotations
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://shu-edu-tw.github.io'
HTML_GLOBS = [
    ROOT / 'index.html',
    *(ROOT / 'pages').glob('*.html'),
    *(ROOT / 'news').glob('*.html'),
]

issues: list[str] = []

HOME_BAD_RE = re.compile(r'https://shu-edu-tw\.github\.io/home', re.I)
CANON_RE = re.compile(
    r'<link[^>]+rel=["\']canonical["\']'
    r'[^>]*href=["\']([^"\']+)["\']',
    re.I,
)
OG_URL_RE = re.compile(
    r'<meta[^>]+property=["\']og:url["\']'
    r'[^>]*content=["\']([^"\']+)["\']',
    re.I,
)

for html in HTML_GLOBS:
    if not html.exists():
        continue
    text = html.read_text(encoding='utf-8', errors='ignore')

    # 1) stray /home
    if HOME_BAD_RE.search(text):
        issues.append(f"[STRAY /home] {html}")

    # 2) canonical presence & correctness
    m = CANON_RE.search(text)
    if not m:
        issues.append(f"[MISSING CANONICAL] {html}")
    else:
        canon = m.group(1)
        if not canon.startswith(BASE):
            issues.append(f"[CANONICAL DOMAIN] {html} -> {canon}")
        # basic path heuristic: index at root; others under /pages/ or /news/
        if html.name == 'index.html' and not canon.endswith('/'):
            issues.append(
                f"[CANONICAL INDEX TRAILING SLASH] {html} -> {canon}"
            )
        if html.parent.name == 'pages' and f"{BASE}/pages/" not in canon:
            issues.append(f"[CANONICAL PATH] {html} -> {canon}")
        if html.parent.name == 'news' and f"{BASE}/news/" not in canon:
            issues.append(f"[CANONICAL PATH] {html} -> {canon}")

    # 3) og:url matches canonical (if both exist)
    ogm = OG_URL_RE.search(text)
    if m and ogm:
        og = ogm.group(1)
        canon = m.group(1)
        if og != canon:
            issues.append(
                f"[OG URL != CANONICAL] {html} -> og:{og} vs canon:{canon}"
            )

if issues:
    print('SEO validation found issues:')
    for i in issues:
        print(' -', i)
    raise SystemExit(1)
else:
    print(
        'SEO validation OK: canonical/OG paths consistent and no stray '
        '/home references.'
    )
