---
name: pwa-review
description: Comprehensive PWA technical audit tool. Analyzes manifest.json, service worker, offline behavior, installability, security, performance, and UX. Use when user asks to review/audit a PWA, mentions "PWA review", "manifest check", "service worker analysis", "Lighthouse alternative", or provides a URL asking about PWA readiness.
invocable: true
---

# PWA Review Skill

Analyze Progressive Web Apps for technical compliance, performance, and UX quality.

## Workflow

1. **Fetch PWA resources** — Use the WebFetch tool to retrieve the target URL's HTML
2. **Discover manifest and service worker** — Run `scripts/discover_pwa.py` to extract manifest URL and SW registration from HTML
3. **Fetch manifest.json** — Use the WebFetch tool on discovered manifest URL
4. **Fetch service worker** — Use the WebFetch tool on discovered SW URL
5. **Run analysis** — Execute `scripts/analyze_pwa.py` with fetched content
6. **Generate report** — Execute `scripts/generate_report.py` to create final .md report
7. **Present report** — Display the generated report to the user

## Step Details

### Step 1-4: Fetching Resources

Fetch the target URL first. Save the HTML content to a temporary file, then run the discovery script to find manifest and service worker paths. If paths are relative, resolve them against the base URL before fetching.

```bash
python3 scripts/discover_pwa.py --html pwa_page.html --base-url "https://example.com"
```

Output: JSON with `manifest_url` and `sw_url` fields.

### Step 5: Analysis

Save fetched content to temp files in the current directory, then run:

```bash
python3 scripts/analyze_pwa.py \
  --html pwa_page.html \
  --manifest pwa_manifest.json \
  --sw pwa_sw.js \
  --url "https://example.com"
```

Output: JSON analysis results at `pwa_analysis.json`

### Step 6: Report Generation

```bash
python3 scripts/generate_report.py \
  --analysis pwa_analysis.json \
  --output pwa_review_report.md
```

### Step 7: Present

Read and display the generated `pwa_review_report.md` to the user.

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
