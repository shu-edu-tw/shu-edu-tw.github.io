#!/usr/bin/env python3
"""
Analyze index.html structure for SEO:
- Count and list all <meta> tags
- Check <h1> uniqueness
- Report heading hierarchy (h1-h6)
- Validate semantic structure
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'index.html')

with open(INDEX, 'r', encoding='utf-8') as f:
    html = f.read()

# Extract meta tags
meta_pattern = re.compile(r'<meta\s+([^>]+)>', re.I)
metas = meta_pattern.findall(html)

print(f"=== index.html SEO Structure Analysis ===\n")
print(f"Total <meta> tags: {len(metas)}\n")

# Categorize meta tags
meta_types = {}
for meta in metas:
    if 'name=' in meta:
        match = re.search(r'name=["\']([^"\']+)["\']', meta)
        if match:
            key = f"name={match.group(1)}"
            meta_types[key] = meta_types.get(key, 0) + 1
    elif 'property=' in meta:
        match = re.search(r'property=["\']([^"\']+)["\']', meta)
        if match:
            key = f"property={match.group(1)}"
            meta_types[key] = meta_types.get(key, 0) + 1
    elif 'charset=' in meta:
        meta_types['charset'] = meta_types.get('charset', 0) + 1

print("Meta tag breakdown:")
for key, count in sorted(meta_types.items()):
    print(f"  {key}: {count}")

# Check H1 tags
h1_pattern = re.compile(r'<h1[^>]*>(.*?)</h1>', re.I | re.S)
h1_tags = h1_pattern.findall(html)
h1_texts = [re.sub(r'<[^>]+>', '', h1).strip() for h1 in h1_tags]

print(f"\n<h1> count: {len(h1_texts)}")
if len(h1_texts) == 1:
    print("✓ Single H1 (good)")
elif len(h1_texts) > 1:
    print("⚠ Multiple H1 tags found:")
    for i, text in enumerate(h1_texts, 1):
        preview = text[:60] + '...' if len(text) > 60 else text
        print(f"  {i}. {preview}")

# Check heading hierarchy
for level in range(1, 7):
    pattern = re.compile(f'<h{level}[^>]*>', re.I)
    count = len(pattern.findall(html))
    if count > 0:
        print(f"<h{level}>: {count}")

# Check title
title_match = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
if title_match:
    title = title_match.group(1).strip()
    print(f"\n<title>: {title}")
    print(f"Title length: {len(title)} chars")
    if len(title) < 30:
        print("⚠ Title might be too short (< 30 chars)")
    elif len(title) > 60:
        print("⚠ Title might be too long (> 60 chars)")

# Check meta description
desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', html, re.I)
if desc_match:
    desc = desc_match.group(1)
    print(f"\nMeta description length: {len(desc)} chars")
    if len(desc) < 120:
        print("⚠ Description might be too short (< 120 chars)")
    elif len(desc) > 160:
        print("⚠ Description might be too long (> 160 chars)")

print("\n=== Analysis complete ===")
