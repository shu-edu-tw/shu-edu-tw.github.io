# shu-edu-tw.github.io

靜態網站（GitHub Pages）。本文件說明手動部署與日常維運流程，避免遺漏步驟。

## 檔案結構（重點）
- `index.html`、`pages/`、`news/`、`css/`、`js/`、`images/`
- `robots.txt`：列出 `sitemap.xml` 與 `news-sitemap.xml`
- `sitemap.xml`：一般頁面 + 已發布新聞頁
- `news-sitemap.xml`：Google News 專用（最近 100 則）
- `scripts/`：維運腳本（見下）

## 一次性設定
- Search Console 資源：`https://shu-edu-tw.github.io/`
- GA4：確認使用 gtag 代碼 `G-QHYFHLDM6D`，啟用 Enhanced Measurement 的 Page views + History events。

## 日常發佈（手動部署）
1. 新增/修改內容（頁面或新聞）。
2. 產生部署包（含驗證與站圖生成）：
   ```bash
   bash scripts/build.sh
   ```
3. 將 `deploy_bundle/site/` 內檔案整包上傳至 GitHub repo 根目錄（覆蓋）。
4. 驗證：
   ```bash
   curl -I https://shu-edu-tw.github.io/
   curl -s https://shu-edu-tw.github.io/sitemap.xml | head
   curl -s https://shu-edu-tw.github.io/news-sitemap.xml | head
   curl -s https://shu-edu-tw.github.io/robots.txt
   ```
5. Search Console：在 Sitemaps 重新提交 `sitemap.xml` 與 `news-sitemap.xml`，並對兩者做「URL 檢查 → 測試即時網址」。

## 新聞維運
- 列表資料：`js/news-manifest.json`
- 頁面檔：`news/YYYY-MM-DD-slug.html`
- 自動站圖：`scripts/generate_sitemaps.py` 只收錄「實際存在的頁面」，避免 404 進索引。
- 發佈前檢查（build.sh 會自動執行）：
   ```bash
   python3 scripts/validate_news.py
   python3 scripts/validate_seo.py
   ```

## GA/SEO 注意事項
- 已移除手動 `page_view` 事件，避免與 GA4 自動 page_view 重複計數。
- canonical/OG 全站改為 `https://shu-edu-tw.github.io/`；如新增新頁，請套用既有頁面模版的 `<head>` 欄位。
- 建議新增/維護 `NewsArticle` 結構化資料於每篇新聞頁。

## 疑難排解
- GitHub Pages 沒更新：稍等 1–3 分鐘；清除瀏覽器快取或在 DevTools Application > Service Workers 移除舊快取（目前 `shu-website-v3`）。
- Search Console 顯示無法擷取 Sitemap：確認資源是 `https://shu-edu-tw.github.io/`，且線上 `sitemap.xml` 能 `200 OK`。
