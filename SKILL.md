---
name: pwa-review
description: >
  Comprehensive PWA (Progressive Web App) technical audit and review tool.
  Analyzes manifest.json, service worker strategies, offline behavior, installability,
  performance, and UX quality. Use when the user asks to review, audit, analyze, or
  evaluate a PWA, or when they mention "PWA review", "PWA audit", "service worker analysis",
  "manifest check", "offline capability test", "installability check", "Lighthouse alternative",
  or any request to assess a web app's progressive web app compliance and quality.
  Also triggers when user provides a URL and asks about PWA readiness, app-like experience,
  or mobile web app quality. Generates a professional report with scores, findings,
  and actionable recommendations.
---

# PWA Review Skill

Analyze Progressive Web Apps for technical compliance, performance, and UX quality.

## Workflow

1. **Fetch PWA resources** — Use `web_fetch` to retrieve the target URL's HTML
2. **Discover manifest and service worker** — Run `scripts/discover_pwa.py` to extract manifest URL and SW registration from HTML
3. **Fetch manifest.json** — Use `web_fetch` on discovered manifest URL
4. **Fetch service worker** — Use `web_fetch` on discovered SW URL
5. **Run analysis** — Execute `scripts/analyze_pwa.py` with fetched content
6. **Generate report** — Execute `scripts/generate_report.py` to create final .md report
7. **Present report** — Share the generated report with the user

## Step Details

### Step 1-4: Fetching Resources

Fetch the target URL first. Then run the discovery script to find manifest and service worker paths.
If paths are relative, resolve them against the base URL before fetching.

```bash
python3 scripts/discover_pwa.py --html /tmp/pwa_page.html --base-url "https://example.com"
```

Output: JSON with `manifest_url` and `sw_url` fields.

### Step 5: Analysis

Save fetched content to temp files, then run:

```bash
python3 scripts/analyze_pwa.py \
  --html /tmp/pwa_page.html \
  --manifest /tmp/pwa_manifest.json \
  --sw /tmp/pwa_sw.js \
  --url "https://example.com"
```

Output: JSON analysis results at `/tmp/pwa_analysis.json`

### Step 6: Report Generation

```bash
python3 scripts/generate_report.py \
  --analysis /tmp/pwa_analysis.json \
  --output /home/claude/pwa_review_report.md
```

### Step 7: Present

Copy report to `/mnt/user-data/outputs/` and present to user.

## Handling Missing Resources

- **No manifest found**: Score manifest category as 0, note as critical finding
- **No service worker**: Score SW/offline categories as 0, note as critical finding
- **Fetch errors**: Note the error, analyze available resources, mention limitations in report

## PWA Scoring Categories (100 pts total)

See `references/pwa-checklist.md` for detailed scoring criteria across these categories:
- Manifest Compliance (20 pts)
- Advanced Manifest (10 pts) — screenshots, shortcuts, share_target, display_override
- Service Worker & Caching (20 pts)
- Offline Capability (10 pts)
- Installability (10 pts)
- Security (10 pts) — CSP, SRI, mixed content, scope restriction
- Performance Signals (10 pts)
- UX & Accessibility (10 pts)

## Report Output Format

Reports use a professional markdown format with:
- Overall score (0-100) with letter grade
- Category breakdown with individual scores
- Critical findings (blockers)
- Warnings (improvements needed)
- Passed checks (what's working well)
- Actionable recommendations prioritized by impact
