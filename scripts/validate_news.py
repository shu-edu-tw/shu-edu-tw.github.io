#!/usr/bin/env python3
"""
Validate news-manifest.json against actual files and images.
Exits with non-zero code if problems found.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'js' / 'news-manifest.json'
IMG_ROOT = ROOT / 'images'
NEWS_ROOT = ROOT / 'news'
BASE_URL = 'https://shu-edu-tw.github.io'

problems: List[str] = []

if not MANIFEST.exists():
    print('No news-manifest.json found. Skipping.')
    raise SystemExit(0)

data = json.loads(MANIFEST.read_text(encoding='utf-8'))

for i, item in enumerate(data, start=1):
    title = item.get('title', '(no title)')
    url = item.get('url', '')
    image = item.get('image', '')

    # Normalize relative paths (../images/... -> images/...)
    page_rel = url.replace('../', '')
    img_rel = image.replace('../', '')

    page_path = ROOT / page_rel
    img_path = ROOT / img_rel

    if not page_path.exists():
        problems.append(f"[MISSING PAGE] {title} -> {BASE_URL}/{page_rel}")

    if not img_path.exists():
        problems.append(f"[MISSING IMAGE] {title} -> {BASE_URL}/{img_rel}")

if problems:
    print('News validation found issues:')
    for p in problems:
        print(' -', p)
    raise SystemExit(1)
else:
    print('News validation OK: all listed pages and images exist.')
