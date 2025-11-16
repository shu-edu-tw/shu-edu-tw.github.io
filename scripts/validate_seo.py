#!/usr/bin/env python3
import os
import re
import sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ORIGIN = "https://shu-edu-tw.github.io"

HTML_GLOB_DIRS = [ROOT]
RE_TITLE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
RE_META_DESC = re.compile(
    r"<meta[^>]*name=[\"']description[\"'][^>]*content=[\"']([^\"']+)[\"'][^>]*>",
    re.I,
)
RE_CANONICAL = re.compile(
    r"<link[^>]*rel=[\"']canonical[\"'][^>]*href=[\"']([^\"']+)[\"'][^>]*>",
    re.I,
)
RE_OG_URL = re.compile(
    r"<meta[^>]*property=[\"']og:url[\"'][^>]*content=[\"']([^\"']+)[\"'][^>]*>",
    re.I,
)
RE_OG_IMAGE = re.compile(
    r"<meta[^>]*property=[\"']og:image[\"'][^>]*content=[\"']([^\"']+)[\"'][^>]*>",
    re.I,
)
RE_OG_SITE = re.compile(
    r"<meta[^>]*property=[\"']og:site_name[\"'][^>]*content=[\"']([^\"']+)[\"'][^>]*>",
    re.I,
)
RE_OG_LOCALE = re.compile(
    r"<meta[^>]*property=[\"']og:locale[\"'][^>]*content=[\"']([^\"']+)[\"'][^>]*>",
    re.I,
)
RE_TW_CARD = re.compile(
    r"<meta[^>]*name=[\"']twitter:card[\"'][^>]*content=[\"']([^\"']+)[\"'][^>]*>",
    re.I,
)

issues = []
checked = 0

for base, _, files in os.walk(ROOT):
    for fn in files:
        if not fn.endswith('.html'):
            continue
        path = os.path.join(base, fn)
        rel = os.path.relpath(path, ROOT)
        # Skip non-public or special-purpose files
        if rel in {
            'offline.html',
            '404.html',
            'google-site-verification-template.html',
        }:
            continue
        if fn.startswith('google') and fn.endswith('.html'):
            # actual Google verification files
            continue
        if rel.startswith(('deploy_bundle/', '.git/', 'scripts/')):
            continue
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
        checked += 1
        title = RE_TITLE.search(html)
        desc = RE_META_DESC.search(html)
        cano = RE_CANONICAL.search(html)
        ogu = RE_OG_URL.search(html)
        ogi = RE_OG_IMAGE.search(html)
        ogs = RE_OG_SITE.search(html)
        ogl = RE_OG_LOCALE.search(html)
        twc = RE_TW_CARD.search(html)

        def add(msg): issues.append(f"{rel}: {msg}")

        if not title:
            add('missing <title>')
        if not desc:
            add('missing meta description')
        if not cano:
            add('missing canonical link')
        if not ogu:
            add('missing og:url')
        if not ogi:
            add('missing og:image')
        if not ogs:
            add('missing og:site_name')
        if not ogl:
            add('missing og:locale')
        if not twc:
            add('missing twitter:card')

        # canonical and og:url should be absolute and same-origin
        for tag, m in [('canonical', cano), ('og:url', ogu)]:
            if m:
                href = m.group(1)
                if not href.startswith('http'):
                    add(f'{tag} not absolute: {href}')
                else:
                    u = urlparse(href)
                    origin = f"{u.scheme}://{u.netloc}"
                    if origin != SITE_ORIGIN:
                        add(f'{tag} wrong origin: {href}')

print(f"Checked HTML files: {checked}")
if issues:
    print("SEO issues found:")
    for i in issues:
        print(" -", i)
    sys.exit(1)
else:
    print("All SEO checks passed.")
