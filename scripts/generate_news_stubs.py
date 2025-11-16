#!/usr/bin/env python3
"""
Generate missing news/*.html stubs from js/news-manifest.json.
- Uses title/date/excerpt/image/url from manifest
- Writes minimal SEO page with canonical, OG/Twitter,
  and JSON-LD NewsArticle
- Skips files that already exist
"""
from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://shu-edu-tw.github.io'

manifest_path = ROOT / 'js' / 'news-manifest.json'
news_dir = ROOT / 'news'
news_dir.mkdir(parents=True, exist_ok=True)

manifest = json.loads(manifest_path.read_text(encoding='utf-8'))

TZ8 = timezone(timedelta(hours=8))


def to_abs(url: str) -> str:
    # manifest url like ../news/2024-...html
    if url.startswith('../'):
        url = url[2:]
    return f"{BASE}/{url.lstrip('/')}"


def to_rel_path(url: str) -> Path:
    # ../news/2024-...html -> ROOT/news/2024-...html
    u = url
    if u.startswith('../'):
        u = u[3:]
    return ROOT / u
 

TEMPLATE = """<!DOCTYPE html>
<html lang=\"zh-TW\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>{title} | 世新大學新聞</title>
  <meta name=\"description\" content=\"{desc}\">

  <link rel=\"canonical\" href=\"{canonical}\">
  <meta name=\"robots\"
        content=\"index, follow, max-image-preview:large,
                 max-snippet:-1, max-video-preview:-1\">

  <meta property=\"og:title\" content=\"{title}\">
  <meta property=\"og:description\" content=\"{desc}\">
  <meta property=\"og:image\" content=\"{image_abs}\">
  <meta property=\"og:url\" content=\"{canonical}\">
  <meta property=\"og:type\" content=\"article\">

  <meta name=\"twitter:card\" content=\"summary_large_image\">
  <meta name=\"twitter:title\" content=\"{title}\">
  <meta name=\"twitter:description\" content=\"{desc}\">
  <meta name=\"twitter:image\" content=\"{image_abs}\">

  <link rel=\"icon\" type=\"image/x-icon\" href=\"../images/favicon.ico\">
  <link rel=\"stylesheet\" href=\"../css/style.css\">
  <link
    href=\"https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&display=swap\"
    rel=\"stylesheet\">
  <link rel=\"preload\" as=\"image\" href=\"{image_rel}\">

  <!-- Google tag (gtag.js) -->
  <script async
    src=\"https://www.googletagmanager.com/gtag/js?id=G-QHYFHLDM6D\"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}} gtag('js', new Date());
    gtag('config', 'G-QHYFHLDM6D');
  </script>

  <script type=\"application/ld+json\">{{
    \"@context\": \"https://schema.org\",
    \"@type\": \"NewsArticle\",
    \"headline\": {json_title},
    \"image\": {json_image},
    \"datePublished\": {json_date},
    \"dateModified\": {json_date},
    \"author\": {{
      \"@type\": \"Organization\",
      \"name\": \"世新大學\",
      \"url\": \"{base}\"
    }},
    \"publisher\": {{
      \"@type\": \"Organization\",
      \"name\": \"世新大學\",
      \"logo\": {{
        \"@type\": \"ImageObject\",
        \"url\": \"{base}/images/shu-logo.webp\"
      }}
    }},
    \"description\": {json_desc},
    \"mainEntityOfPage\": {{\"@type\": \"WebPage\", \"@id\": {json_canonical}}}
  }}</script>
</head>
<body>
  <header class=\"header\"></header>
  <main id=\"main-content\">
    <section class=\"hero\"
      style=\"min-height: 320px; background: #f5f5f5 url('{image_rel}')
             center/cover no-repeat;\"></section>
    <section class=\"news\" style=\"padding: 3rem 0;\">
      <div class=\"container\">
        <article class=\"feature-card\"
          style=\"max-width: 800px; margin: 0 auto; text-align: left;
                 padding: 2rem;\">
          <h1 class=\"college-title\"
              style=\"margin-bottom: .5rem;\">{title}</h1>
          <p style=\"color: #666; margin-top: 0;\">{date_ch}</p>
          <p class=\"news-excerpt\" style=\"font-size: 1.1rem;\">{desc}</p>
          <p>本頁為新聞頁面骨架。待正式內文完成後，請替換此段落為完整報導內容與圖片。</p>
          <a href=\"../pages/news.html\" class=\"btn btn-outline\"
             style=\"margin-top: 1.5rem;\">返回新聞列表</a>
        </article>
      </div>
    </section>
  </main>
  <footer class=\"footer\"></footer>
  <button id=\"backToTop\" class=\"back-to-top\">
    <i class=\"fas fa-arrow-up\"></i>
  </button>
  <script src=\"../js/main.js\"></script>
</body>
</html>
"""

for item in manifest:
    url = item.get('url', '')
    if not url:
        continue
    out_path = to_rel_path(url)
    if out_path.exists():
        continue

    title = item.get('title', '世新大學新聞')
    desc = item.get('excerpt', '世新大學新聞稿。')
    date = item.get('date', '2025-01-01')
    dt = datetime.fromisoformat(date).replace(
      tzinfo=TZ8, hour=10, minute=0, second=0
    )

    image_rel = item.get('image', '../images/shu-logo.webp')
    # normalize relative like ../images/...
    if image_rel.startswith('./'):
        image_rel = image_rel[2:]
    canonical = to_abs(url)
    image_abs = image_rel
    if image_rel.startswith('../'):
        image_abs = f"{BASE}/{image_rel[3:]}"
    elif image_rel.startswith('/'):
        image_abs = f"{BASE}{image_rel}"
    else:
        image_abs = f"{BASE}/news/{image_rel}"

    html = TEMPLATE.format(
        title=title,
        desc=desc,
        canonical=canonical,
        image_rel=image_rel,
        image_abs=image_abs,
        date_ch=date,
        base=BASE,
        json_title=json.dumps(title, ensure_ascii=False),
        json_image=json.dumps(image_abs, ensure_ascii=False),
        json_date=json.dumps(dt.isoformat()),
        json_desc=json.dumps(desc, ensure_ascii=False),
        json_canonical=json.dumps(canonical, ensure_ascii=False),
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding='utf-8')
    print(f"Created stub: {out_path.relative_to(ROOT)}")

print('News stubs generation completed.')
