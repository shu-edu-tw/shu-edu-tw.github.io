#!/usr/bin/env python3
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ORIGIN = "https://shu-edu-tw.github.io"

RE_LINK = re.compile(r"<a[^>]+href=\"([^\"]+)\"", re.I)
RE_IMG = re.compile(r"<img[^>]+src=\"([^\"]+)\"", re.I)

problems = []
scanned = 0

# Helpers

def is_external(url: str) -> bool:
    return (
        url.startswith('http://') or url.startswith('https://') or
        url.startswith('mailto:') or url.startswith('tel:')
    )


def to_local_path(relpath: str, file_dir: str) -> str:
    # Map absolute site URLs to local
    if relpath.startswith(SITE_ORIGIN):
        rel = relpath[len(SITE_ORIGIN):]
        if not rel.startswith('/'):
            rel = '/' + rel
        return os.path.join(ROOT, rel.lstrip('/'))
    # Protocol-relative // or absolute path
    if relpath.startswith('//'):
        return ''  # treat as external
    if relpath.startswith('/'):
        return os.path.join(ROOT, relpath.lstrip('/'))
    # Relative to current file
    return os.path.normpath(os.path.join(file_dir, relpath))


for base, _, files in os.walk(ROOT):
    relbase = os.path.relpath(base, ROOT)
    if relbase.startswith(('deploy_bundle', '.git', 'scripts')):
        continue
    for fn in files:
        if not fn.endswith('.html'):
            continue
        path = os.path.join(base, fn)
        file_dir = os.path.dirname(path)
        rel = os.path.relpath(path, ROOT)
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
        scanned += 1

        links = RE_LINK.findall(html)
        imgs = RE_IMG.findall(html)

        for href in links:
            if is_external(href) or href.startswith('#'):
                continue
            if '#' in href:
                href = href.split('#', 1)[0]
            local = to_local_path(href, file_dir)
            if not local:
                continue
            if not os.path.exists(local):
                problems.append(f"{rel}: broken link -> {href}")

        for src in imgs:
            if is_external(src):
                continue
            local = to_local_path(src, file_dir)
            if not local:
                continue
            if not os.path.exists(local):
                problems.append(f"{rel}: missing image -> {src}")

print(f"Scanned HTML files: {scanned}")
if problems:
    print("Broken internals:")
    for p in problems:
        print(" -", p)
    sys.exit(1)
else:
    print("All internal links and images OK.")
