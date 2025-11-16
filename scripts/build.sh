#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# 0) Run validators (fail fast)
python3 scripts/validate_news.py
python3 scripts/validate_seo.py

# 1) Generate sitemaps
python3 scripts/generate_sitemaps.py

# 2) Build deploy bundle
rm -rf deploy_bundle
mkdir -p deploy_bundle
rsync -a --exclude 'deploy_bundle' --exclude '.git' ./ deploy_bundle/site

cat <<'OUT'
Build finished.
Validators passed (news + SEO). Sitemaps regenerated.
Upload all files from deploy_bundle/site/ to GitHub repo root (overwrite).
Quick checks:
  curl -I https://shu-edu-tw.github.io/
  curl -s https://shu-edu-tw.github.io/sitemap.xml | head
  curl -s https://shu-edu-tw.github.io/news-sitemap.xml | head
  curl -s https://shu-edu-tw.github.io/robots.txt
OUT
