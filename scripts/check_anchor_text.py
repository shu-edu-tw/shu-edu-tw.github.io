#!/usr/bin/env python3
"""
Find generic anchor text that should be improved:
- "點擊這裡", "click here", "more", "read more", etc.
- Report with context for replacement
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GENERIC_PATTERNS = [
    r'點擊這裡',
    r'點此',
    r'按這裡',
    r'click\s+here',
    r'\bmore\b',
    r'read\s+more',
    r'詳情',
    r'更多',
]

LINK_PATTERN = re.compile(r'<a\s+[^>]*>(.*?)</a>', re.I | re.S)

issues = []

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
        
        for link_match in LINK_PATTERN.finditer(html):
            link_text = re.sub(r'<[^>]+>', '', link_match.group(1)).strip()
            
            for pattern in GENERIC_PATTERNS:
                if re.search(pattern, link_text, re.I):
                    # Extract href for context
                    full_tag = link_match.group(0)
                    href_match = re.search(r'href=["\']([^"\']+)["\']', full_tag, re.I)
                    href = href_match.group(1) if href_match else 'unknown'
                    
                    issues.append(f"{rel}: Generic anchor '{link_text}' -> {href}")
                    break

if issues:
    print(f"Generic anchor text found ({len(issues)} instances):")
    for issue in issues:
        print(f"  - {issue}")
    print("\nSuggestion: Replace with descriptive text that indicates destination")
else:
    print("✓ No generic anchor text found")
