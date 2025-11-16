#!/usr/bin/env python3
"""
Check heading hierarchy across all HTML files:
- Verify h1-h6 logical nesting
- Report pages with multiple h1 tags
- Flag heading level skips (e.g., h1 -> h3)
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
        
        # Extract all headings with their levels
        headings = []
        for level in range(1, 7):
            pattern = re.compile(f'<h{level}[^>]*>(.*?)</h{level}>', re.I | re.S)
            for match in pattern.finditer(html):
                text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
                headings.append((level, text[:60]))
        
        if not headings:
            continue
        
        # Check for multiple h1
        h1_count = sum(1 for level, _ in headings if level == 1)
        if h1_count > 1:
            issues.append(f"{rel}: Multiple H1 tags ({h1_count})")
        elif h1_count == 0:
            issues.append(f"{rel}: No H1 tag found")
        
        # Check for level skips
        prev_level = 0
        for level, text in headings:
            if prev_level > 0 and level > prev_level + 1:
                issues.append(f"{rel}: Heading skip from h{prev_level} to h{level}")
                break
            prev_level = level

if issues:
    print("Heading hierarchy issues:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("✓ All pages have proper heading hierarchy")
