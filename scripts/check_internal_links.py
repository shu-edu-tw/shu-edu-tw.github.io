#!/usr/bin/env python3
"""
Check internal anchor href/src references across HTML files:
- <a href> for same-site links (/, ./, ../, /pages, /news, absolute base)
- <img src> references
Reports missing targets. Exits non-zero if any are found.
"""
from __future__ import annotations
from pathlib import Path
import re
 

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://shu-edu-tw.github.io'

HTML_FILES = [
    ROOT / 'index.html',
    *(ROOT / 'pages').glob('*.html'),
    *(ROOT / 'news').glob('*.html'),
]

HREF_RE = re.compile(r'<a\s+[^>]*href=["\']([^"\'#]+)["\']', re.I)
SRC_RE = re.compile(r'<img\s+[^>]*src=["\']([^"\']+)["\']', re.I)

missing: list[str] = []


def to_local_path(url: str, base_file: Path) -> Path | None:
    if url.startswith('mailto:') or url.startswith('tel:'):
        return None
    if url.startswith('#'):
        return None
    if url.startswith('http://') or url.startswith('https://'):
        # only handle same-origin
        if url.startswith(BASE + '/'):
            path = url[len(BASE):]
        else:
            return None
    else:
        path = url
    # map root or directory-ending to index.html
    if path == '' or path.endswith('/'):
        path = path + 'index.html'
    # absolute-rooted path
    if path.startswith('/'):
        return ROOT / path.lstrip('/')
    # relative path: resolve against current file's directory
    return (base_file.parent / path).resolve()


for html in HTML_FILES:
    if not html.exists():
        continue
    text = html.read_text(encoding='utf-8', errors='ignore')
    for m in HREF_RE.finditer(text):
        href = m.group(1)
        p = to_local_path(href, html)
        if p is None:
            continue
        if not p.exists():
            missing.append(
                f"[A HREF] {html.relative_to(ROOT)} -> {href} -> missing "
                f"{p.relative_to(ROOT)}"
            )
    for m in SRC_RE.finditer(text):
        src = m.group(1)
        p = to_local_path(src, html)
        if p is None:
            # external absolute images allowed if same origin not required
            if src.startswith('http://') or src.startswith('https://'):
                if src.startswith(BASE + '/'):
                    # same-origin external; compute path and check
                    up = to_local_path(src, html)
                    if up and not up.exists():
                        msg = (
                            f"[IMG SRC] {html.relative_to(ROOT)} -> {src} -> "
                            f"missing {up.relative_to(ROOT)}"
                        )
                        missing.append(msg)
            continue
        if not p.exists():
            msg = (
                f"[IMG SRC] {html.relative_to(ROOT)} -> {src} -> "
                f"missing {p.relative_to(ROOT)}"
            )
            missing.append(msg)

if missing:
    print('Internal link check found issues:')
    for i in missing:
        print(' -', i)
    raise SystemExit(1)
else:
    print('Internal link check OK: no missing internal anchors or images.')
