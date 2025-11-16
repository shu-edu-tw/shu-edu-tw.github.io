#!/usr/bin/env python3
"""
Accessibility checks:
- <img> must have non-empty alt,
  unless role="presentation" or aria-hidden="true".
Prints issues and exits non-zero if any are found.
"""
from __future__ import annotations
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = [
    ROOT / 'index.html',
    *(ROOT / 'pages').glob('*.html'),
    *(ROOT / 'news').glob('*.html'),
]
IMG_RE = re.compile(r'<img\s+([^>]+)>', re.I)
ALT_RE = re.compile(r'alt=["\']([^"\']*)["\']', re.I)
ROLE_PRESENT = re.compile(r'role=["\']presentation["\']', re.I)
ARIA_HIDDEN = re.compile(r'aria-hidden=["\']true["\']', re.I)

issues: list[str] = []

for html in HTML_FILES:
    if not html.exists():
        continue
    text = html.read_text(encoding='utf-8', errors='ignore')
    for m in IMG_RE.finditer(text):
        attrs = m.group(1)
        if ROLE_PRESENT.search(attrs) or ARIA_HIDDEN.search(attrs):
            continue
        altm = ALT_RE.search(attrs)
        if not altm or altm.group(1).strip() == '':
            msg = (
                f"[IMG ALT] {html.relative_to(ROOT)} -> missing or empty alt"
            )
            issues.append(msg)

if issues:
    print('Accessibility validation found issues:')
    for i in issues:
        print(' -', i)
    raise SystemExit(1)
else:
    print('Accessibility validation OK: all <img> have alt or are decorative.')
