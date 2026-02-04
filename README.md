# 🔍 PWA Review Skill for Claude

A comprehensive Progressive Web App (PWA) audit tool that works as a **Claude Skill**. It analyzes any PWA for technical compliance, performance, offline capability, and UX quality — generating a professional scored report.

Think of it as a **Lighthouse alternative** that runs inside Claude, with actionable insights and a 100-point scoring system.

![Score: A+](https://img.shields.io/badge/Max%20Score-100%20pts-brightgreen)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- **Manifest Validation** — Checks all required and recommended fields
- **Advanced Manifest** — screenshots, shortcuts, display_override, share_target, launch_handler
- **Service Worker Analysis** — Detects cache strategies, Workbox, skipWaiting, push/sync handlers
- **Offline Capability** — Evaluates fallback pages, app shell caching, offline indicators
- **Installability Check** — HTTPS, icons, manifest link, iOS support, prefer_related_applications blocker
- **Security Audit** — CSP, SRI, mixed content, sensitive data in cache, SW scope
- **Performance Signals** — Render-blocking resources, lazy loading, preload hints, font optimization
- **UX & Accessibility** — Semantic HTML, ARIA landmarks, viewport, language attributes
- **Actionable Reports** — Every finding includes a "How to Fix" code snippet and reference links

## 📊 Scoring System

| Category | Max Points | Key Checks |
|----------|-----------|------------|
| 📋 Manifest Compliance | 20 | name, display, icons, theme_color, scope |
| 🧩 Advanced Manifest | 10 | screenshots, shortcuts, categories, display_override, share_target |
| ⚙️ Service Worker & Caching | 20 | Events, cache strategy, versioning, Workbox detection |
| 📡 Offline Capability | 10 | Fallback page, app shell, offline UI indicator |
| 📲 Installability | 10 | HTTPS, manifest link, icon sizes, apple-touch-icon |
| 🔒 Security | 10 | CSP, SRI, mixed content, SW scope, error handling |
| ⚡ Performance Signals | 10 | Blocking resources, lazy loading, preload, fonts |
| 🎨 UX & Accessibility | 10 | Semantic HTML, ARIA, viewport, lang, theme-color meta |

**Grading Scale:**

| Score | Grade | Label |
|-------|-------|-------|
| 90–100 | A+ | Excellent PWA |
| 80–89 | A | Strong PWA |
| 70–79 | B | Good — Room for improvement |
| 60–69 | C | Functional — Needs work |
| 40–59 | D | Major gaps |
| 0–39 | F | Not a functional PWA |

## 🚀 Usage

### As a Claude Skill

1. Download or clone this repo
2. Upload the `pwa-review.skill` file to Claude (or add the folder as a skill)
3. Ask Claude to review any PWA:

```
Review the PWA at https://example.com
```

Claude will automatically fetch the page, discover the manifest and service worker, run the analysis, and generate a scored report.

### Standalone (CLI)

You can also run the scripts independently:

```bash
# Step 1: Save your PWA's HTML to a file
curl -o /tmp/page.html https://your-pwa.com

# Step 2: Discover manifest & service worker URLs
python3 scripts/discover_pwa.py \
  --html /tmp/page.html \
  --base-url "https://your-pwa.com"

# Step 3: Save manifest and service worker files
curl -o /tmp/manifest.json https://your-pwa.com/manifest.json
curl -o /tmp/sw.js https://your-pwa.com/sw.js

# Step 4: Run analysis
python3 scripts/analyze_pwa.py \
  --html /tmp/page.html \
  --manifest /tmp/manifest.json \
  --sw /tmp/sw.js \
  --url "https://your-pwa.com"

# Step 5: Generate report
python3 scripts/generate_report.py \
  --analysis /tmp/pwa_analysis.json \
  --output report.md
```

## 📁 Project Structure

```
pwa-review/
├── SKILL.md                    # Claude skill definition & workflow
├── scripts/
│   ├── discover_pwa.py         # Extracts manifest & SW URLs from HTML
│   ├── analyze_pwa.py          # Core analysis engine (8 categories, 100 pts)
│   └── generate_report.py      # Markdown report generator
├── references/
│   └── pwa-checklist.md        # Detailed scoring criteria & best practices
├── examples/
│   └── sample_report.md        # Example output report
├── LICENSE
└── README.md
```

## 📋 Sample Report Output

```
# PWA Review Report

**URL:** https://example.com
**Overall Score:** 83/100 — Grade: 🥇 A (Strong PWA)

| Category                        | Score         |
|---------------------------------|---------------|
| 📋 Manifest Compliance          | 18/20 (90%)   |
| 🧩 Advanced Manifest            | 2/10  (20%)   |
| ⚙️ Service Worker & Caching     | 18/20 (90%)   |
| 📡 Offline Capability           | 10/10 (100%)  |
| 📲 Installability               | 9/10  (90%)   |
| 🔒 Security                     | 6/10  (60%)   |
| ⚡ Performance Signals           | 10/10 (100%)  |
| 🎨 UX & Accessibility           | 10/10 (100%)  |

## 🚨 Critical Findings
(none)

## ⚠️ Warnings
- No screenshots — Chrome shows basic install dialog without them
- No Content Security Policy meta tag detected

## ✅ Passed Checks (35 items)
...

## 📌 Prioritized Recommendations
1. Add screenshots with form_factor (wide + narrow) to manifest
2. Add Content-Security-Policy meta tag or HTTP header
...
```

See [examples/sample_report.md](examples/sample_report.md) for a full report.

## 🤝 Contributing

Contributions are welcome! Some ideas:

- **HTTP header analysis**: CSP via headers, HSTS, compression (gzip/brotli)
- **Lighthouse API integration**: Automated performance scoring via PageSpeed Insights API
- **Multi-page crawl**: Analyze multiple routes and aggregate findings
- **Web Push check**: Detect push notification subscription and handling
- **Background Sync**: Detect Background Sync API usage in service worker
- **JSON/HTML output**: Alternative report formats
- **CI integration**: Run as a GitHub Action for automated PWA audits

### How to contribute

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/web-push-check`)
3. Make your changes and test with real PWAs
4. Submit a pull request

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

## 🙏 Credits

Built by [Emrah](https://github.com/emrahub) as a Claude Skill for the community.

Inspired by [Lighthouse](https://developer.chrome.com/docs/lighthouse), [PWA Builder](https://www.pwabuilder.com/), and the [Web App Manifest spec](https://www.w3.org/TR/appmanifest/).
