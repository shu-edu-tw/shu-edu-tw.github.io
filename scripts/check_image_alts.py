#!/usr/bin/env python3
"""
Check all images across HTML files for alt attributes:
- Find all <img> tags
- Report missing or empty alt attributes
- Flag decorative images that should have alt=""
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IMG_PATTERN = re.compile(r'<img\s+([^>]+)>', re.I)
ALT_PATTERN = re.compile(r'alt=["\']([^"\']*)["\']', re.I)

issues = []
total_images = 0
missing_alt = 0
empty_alt = 0

for base, _, files in os.walk(ROOT):
    relbase = os.path.relpath(base, ROOT)
    if relbase.startswith(('deploy_bundle', '.git', 'scripts')):
        continue
    
    for fn in files:
        if not fn.endswith('.html'):
            continue
        
        path = os.path.join(base, fn)
        rel = os.path.relpath(path, ROOT)
        
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
        
        for img_match in IMG_PATTERN.finditer(html):
            total_images += 1
            img_tag = img_match.group(0)
            alt_match = ALT_PATTERN.search(img_tag)
            
            # Extract src for context
            src_match = re.search(r'src=["\']([^"\']+)["\']', img_tag, re.I)
            src = src_match.group(1) if src_match else 'unknown'
            
            if not alt_match:
                missing_alt += 1
                issues.append(f"{rel}: missing alt -> {src}")
            elif not alt_match.group(1).strip():
                empty_alt += 1
                # Empty alt is OK for decorative images, just note it
                issues.append(f"{rel}: empty alt (decorative?) -> {src}")

print(f"Total images scanned: {total_images}")
print(f"Missing alt: {missing_alt}")
print(f"Empty alt: {empty_alt}")

if issues:
    print("\nImage alt issues:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("\n✓ All images have alt attributes")
