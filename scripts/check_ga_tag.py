#!/usr/bin/env python3
"""
Ensure GA4 gtag (G-QHYFHLDM6D) is present on index.html and
all pages/*.html & news/*.html.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / 'index.html',
    *(ROOT / 'pages').glob('*.html'),
    *(ROOT / 'news').glob('*.html'),
]

needle = 'https://www.googletagmanager.com/gtag/js?id=G-QHYFHLDM6D'

missing = []
for f in FILES:
    if not f.exists():
        continue
    t = f.read_text(encoding='utf-8', errors='ignore')
    if needle not in t:
        missing.append(f.relative_to(ROOT))

if missing:
    print('GA tag check failed, missing on:')
    for m in missing:
        print(' -', m)
    raise SystemExit(1)
else:
    print('GA tag check OK: all target pages include GA4 tag.')
