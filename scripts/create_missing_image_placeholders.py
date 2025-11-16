#!/usr/bin/env python3
"""
Create placeholder images for missing <img src> references by copying
images/shu-logo.webp.
Only affects same-repo images under the images/ folder.
"""
from __future__ import annotations
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://shu-edu-tw.github.io'
PLACEHOLDER = ROOT / 'images' / 'shu-logo.webp'

HTML_FILES = [
    ROOT / 'index.html',
    *(ROOT / 'pages').glob('*.html'),
    *(ROOT / 'news').glob('*.html'),
]

SRC_RE = re.compile(r'<img\s+[^>]*src=["\']([^"\']+)["\']', re.I)


def to_local_path(url: str, base_file: Path) -> Path | None:
    if url.startswith('http://') or url.startswith('https://'):
        if url.startswith(BASE + '/'):
            path = url[len(BASE):]
        else:
            return None
    else:
        path = url
    if path == '' or path.endswith('/'):
        path = path + 'index.html'
    if path.startswith('/'):
        return ROOT / path.lstrip('/')
    return (base_file.parent / path).resolve()

 
created: list[Path] = []
for html in HTML_FILES:
    if not html.exists():
        continue
    text = html.read_text(encoding='utf-8', errors='ignore')
    for m in SRC_RE.finditer(text):
        src = m.group(1)
        p = to_local_path(src, html)
        if p is None:
            continue
        # only act on files under images/
        try:
            rel = p.relative_to(ROOT)
        except ValueError:
            continue
        if not str(rel).startswith('images/'):
            continue
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(PLACEHOLDER, p)
            created.append(rel)

if created:
    print('Created placeholder images:')
    for c in created:
        print(' -', c)
else:
    print('No placeholders needed.')
