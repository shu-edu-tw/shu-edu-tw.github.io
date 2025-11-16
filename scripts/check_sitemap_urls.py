#!/usr/bin/env python3
"""
Validate sitemap.xml and news-sitemap.xml URLs:
- Parse XML sitemaps
- Check that each <loc> URL returns HTTP 200
- Report any broken/404 URLs
"""
import os
import sys
import xml.etree.ElementTree as ET
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP = os.path.join(ROOT, 'sitemap.xml')
NEWS_SITEMAP = os.path.join(ROOT, 'news-sitemap.xml')


def check_url(url: str) -> tuple[int, str]:
    """Returns (status_code, message)"""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=10) as resp:
            return resp.status, 'OK'
    except HTTPError as e:
        return e.code, str(e)
    except URLError as e:
        return 0, str(e)
    except Exception as e:
        return -1, str(e)


def parse_sitemap(path: str) -> list[str]:
    """Extract all <loc> URLs from sitemap XML"""
    tree = ET.parse(path)
    root = tree.getroot()
    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    return [loc.text for loc in root.findall('.//ns:loc', ns) if loc.text]


issues = []
checked = 0

for sitemap_path in [SITEMAP, NEWS_SITEMAP]:
    if not os.path.exists(sitemap_path):
        print(f"Warning: {sitemap_path} not found, skipping")
        continue
    
    urls = parse_sitemap(sitemap_path)
    sitemap_name = os.path.basename(sitemap_path)
    
    for url in urls:
        checked += 1
        status, msg = check_url(url)
        if status != 200:
            issues.append(f"{sitemap_name}: {url} -> HTTP {status} ({msg})")

print(f"Checked URLs: {checked}")
if issues:
    print("Sitemap issues found:")
    for i in issues:
        print(" -", i)
    sys.exit(1)
else:
    print("All sitemap URLs return HTTP 200.")
