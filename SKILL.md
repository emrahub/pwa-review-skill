---
name: pwa-review
description: Comprehensive 127-point PWA audit beyond Lighthouse - analyzes manifest, service worker, offline capabilities, security, and advanced PWA features
user_invocable: true
args:
  - name: url
    description: The PWA URL to analyze (e.g., https://example.com)
    required: true
---

<pwa-review>

# PWA Review Skill

A comprehensive Progressive Web App audit that goes beyond standard Lighthouse testing. This skill analyzes PWAs across 10 categories with a 127-point scoring system, including advanced features that typical audits miss.

## Scoring Overview

| Category | Points | Focus |
|----------|--------|-------|
| Manifest Compliance | 20 | Essential manifest fields |
| Advanced Manifest | 11 | Enhanced manifest features |
| Service Worker & Caching | 22 | SW implementation quality |
| Offline Capability | 10 | Offline functionality |
| Installability | 10 | Install requirements |
| Security | 12 | Security measures |
| Performance Signals | 10 | Performance optimization |
| UX & Accessibility | 10 | User experience |
| SEO & Discoverability | 7 | Search optimization |
| PWA Advanced | 15 | Cutting-edge PWA features |

**Grading Scale:** A+ (90%+), A (80-89%), B (70-79%), C (60-69%), D (40-59%), F (<40%)

---

## Execution Workflow

When the user invokes `/pwa-review <url>`, follow these steps precisely:

### Step 1: Fetch Target HTML

Use WebFetch to retrieve the target URL's HTML content.

```
WebFetch: {url}
Prompt: "Return the complete HTML source code. I need to analyze the head section for PWA-related tags including manifest link, meta tags, and inline scripts."
```

### Step 2: Extract PWA Resources

From the HTML, identify:

**Manifest URL:**
- Look for `<link rel="manifest" href="...">`
- Convert relative URLs to absolute using the base URL
- If not found, note as CRITICAL issue

**Service Worker Registration:**
- Search for `navigator.serviceWorker.register('...')` or `navigator.serviceWorker.register("...")`
- Extract the SW file path
- If not found, note as CRITICAL issue

**Meta Tags to Extract:**
- `<meta name="theme-color" content="...">`
- `<meta name="apple-mobile-web-app-capable" content="...">`
- `<meta name="apple-mobile-web-app-status-bar-style" content="...">`
- `<meta name="viewport" content="...">`
- `<meta http-equiv="Content-Security-Policy" content="...">`
- `<link rel="apple-touch-icon" href="...">`

### Step 3: Fetch Manifest

If manifest URL was found, use WebFetch to retrieve it:

```
WebFetch: {manifest_url}
Prompt: "Return the complete manifest.json content as raw JSON."
```

If manifest fetch fails (CORS, 404, etc.), score manifest categories as 0 and continue.

### Step 4: Fetch Service Worker

If service worker URL was found, use WebFetch to retrieve it:

```
WebFetch: {sw_url}
Prompt: "Return the complete service worker JavaScript code."
```

If SW fetch fails, score SW-related categories as 0 and continue.

### Step 5: Analyze & Score

Evaluate each category using the detailed checklist below. Track:
- **Passed items** (full points)
- **Failed items** (0 points) - record as issues
- **Partial items** (partial points where applicable)

### Step 6: Generate Report

Output a markdown report following the template at the end of this document.

---

## Detailed Scoring Checklist

### Category 1: Manifest Compliance (20 points)

| Check | Points | How to Verify |
|-------|--------|---------------|
| `name` field present and non-empty | 2 | manifest.name exists and length > 0 |
| `short_name` present (≤12 chars recommended) | 2 | manifest.short_name exists |
| `icons` array with 192x192 PNG | 4 | icons array has item with sizes="192x192" |
| `icons` array with 512x512 PNG | 4 | icons array has item with sizes="512x512" |
| `start_url` defined | 2 | manifest.start_url exists |
| `display` mode set (standalone/fullscreen/minimal-ui) | 2 | manifest.display is one of allowed values |
| `background_color` specified | 2 | manifest.background_color exists (hex/rgb/named) |
| `theme_color` specified | 2 | manifest.theme_color exists |

**Critical Blocker:** If manifest is missing entirely, this category scores 0/20.

### Category 2: Advanced Manifest Features (11 points)

| Check | Points | How to Verify |
|-------|--------|---------------|
| `description` field present | 1 | manifest.description exists |
| `screenshots` array for install UI | 2 | manifest.screenshots array with ≥1 item |
| `shortcuts` array for quick actions | 2 | manifest.shortcuts array with ≥1 item |
| `categories` array defined | 1 | manifest.categories exists |
| `orientation` preference set | 1 | manifest.orientation exists |
| `dir` and `lang` for i18n | 1 | manifest.dir OR manifest.lang exists |
| `id` field for app identity | 1 | manifest.id exists |
| `scope` properly defined | 1 | manifest.scope exists |
| Maskable icon present | 1 | icons array has item with purpose="maskable" or "any maskable" |

### Category 3: Service Worker & Caching (22 points)

| Check | Points | How to Verify |
|-------|--------|---------------|
| SW registered in HTML | 2 | navigator.serviceWorker.register() found |
| `install` event handler present | 3 | SW contains addEventListener('install', ...) or self.oninstall |
| `activate` event handler present | 3 | SW contains addEventListener('activate', ...) or self.onactivate |
| `fetch` event handler present | 4 | SW contains addEventListener('fetch', ...) or self.onfetch |
| Cache API usage (caches.open/put/match) | 3 | SW contains caches.open or cache.put or cache.match |
| Cache versioning/naming strategy | 2 | SW has cache name variable (CACHE_NAME, CACHE_VERSION, etc.) |
| Old cache cleanup in activate | 2 | activate handler deletes old caches |
| Background Sync support | 2 | SW contains addEventListener('sync', ...) or addEventListener('periodicsync', ...) for offline queue processing |
| Workbox usage (bonus, not required) | 1 | SW imports workbox or uses workbox.* methods |

**Critical Blocker:** If no service worker, this category scores 0/22.

### Category 4: Offline Capability (10 points)

| Check | Points | How to Verify |
|-------|--------|---------------|
| Offline fallback page defined | 3 | SW caches and serves an offline.html or similar |
| App shell resources precached | 3 | install event caches core HTML/CSS/JS files |
| Offline indicator in UI (code pattern) | 2 | Code checks navigator.onLine or listens to online/offline events |
| Network-first or cache-first strategy evident | 2 | fetch handler has clear strategy pattern |

### Category 5: Installability Requirements (10 points)

| Check | Points | How to Verify |
|-------|--------|---------------|
| Served over HTTPS | 3 | URL starts with https:// |
| Valid manifest linked in HTML | 2 | <link rel="manifest"> exists with valid href |
| Service worker with fetch handler | 2 | Covered in SW category, cross-check |
| 192x192 icon present | 1 | Covered in manifest, cross-check |
| 512x512 icon present | 1 | Covered in manifest, cross-check |
| `apple-touch-icon` for iOS | 1 | <link rel="apple-touch-icon"> in HTML |

**Note:** `prefer_related_applications: true` in manifest BLOCKS browser install prompt - flag as CRITICAL if found.

### Category 6: Security Measures (12 points)

| Check | Points | How to Verify |
|-------|--------|---------------|
| HTTPS enforced | 2 | URL is https:// (duplicate check for emphasis) |
| Content Security Policy present | 3 | CSP meta tag or mention in SW/HTML |
| Subresource Integrity (SRI) on scripts | 2 | <script> tags have integrity="sha..." |
| No mixed content | 2 | No http:// resources loaded on https:// page |
| scope restricted appropriately | 1 | manifest.scope doesn't expose unnecessary paths |
| Cross-Origin Isolation (COOP/COEP) | 2 | Headers: Cross-Origin-Opener-Policy, Cross-Origin-Embedder-Policy (required for SharedArrayBuffer) |

### Category 7: Performance Signals (10 points)

| Check | Points | How to Verify |
|-------|--------|---------------|
| No render-blocking scripts in head | 2 | Scripts have defer/async or are at body end |
| Images have lazy loading | 2 | <img loading="lazy"> or Intersection Observer usage |
| Resource hints present | 2 | <link rel="preload/prefetch/preconnect"> found |
| Code splitting indicators | 2 | Multiple JS chunks or dynamic import() usage |
| Font optimization | 2 | font-display: swap or preloaded fonts |

### Category 8: UX & Accessibility (10 points)

| Check | Points | How to Verify |
|-------|--------|---------------|
| Responsive viewport meta | 2 | <meta name="viewport" content="width=device-width, initial-scale=1"> |
| Semantic HTML structure | 2 | <main>, <nav>, <header>, <footer> tags present |
| ARIA landmarks or roles | 2 | role="..." or aria-* attributes found |
| Language declared | 2 | <html lang="..."> attribute present |
| Touch-friendly targets | 2 | No evidence of tiny click targets (qualitative) |

### Category 9: SEO & Discoverability (7 points)

| Check | Points | How to Verify |
|-------|--------|---------------|
| `<title>` tag present | 1 | HTML has <title> with content |
| Meta description | 2 | <meta name="description" content="..."> |
| Open Graph tags | 2 | og:title, og:description, og:image present |
| Canonical URL | 1 | <link rel="canonical" href="..."> |
| Structured data (JSON-LD) | 1 | <script type="application/ld+json"> found |

### Category 10: PWA Advanced Capabilities (15 points)

| Check | Points | How to Verify |
|-------|--------|---------------|
| `handle_links` preference | 2 | manifest.handle_links exists (preferred/auto/not-preferred) |
| `launch_handler` defined | 2 | manifest.launch_handler object exists |
| `file_handlers` array | 2 | manifest.file_handlers with accept types |
| `protocol_handlers` array | 2 | manifest.protocol_handlers for custom protocols |
| `share_target` defined | 2 | manifest.share_target object exists |
| `display_override` array | 1 | manifest.display_override for fallback displays |
| `edge_side_panel` for Edge | 1 | manifest.edge_side_panel object exists |
| `scope_extensions` | 1 | manifest.scope_extensions array exists |
| `related_applications` (informational) | 1 | manifest.related_applications exists |
| `prefer_related_applications` is false/absent | 1 | Value is false or field is missing (true = CRITICAL issue) |

---

## Issue Classification

### Critical Issues (Must Fix)
- Missing manifest file
- Missing service worker
- No fetch event handler in SW
- `prefer_related_applications: true` (blocks install)
- Not served over HTTPS
- Missing required icons (192x192, 512x512)

### Warnings (Should Fix)
- Missing theme_color/background_color
- No offline fallback page
- No CSP header/meta
- Missing apple-touch-icon
- No cache versioning strategy
- Missing meta description

### Informational (Nice to Have)
- Missing advanced manifest features
- No PWA advanced capabilities
- No structured data
- Missing shortcuts

---

## Report Template

Generate the report in this exact format:

```markdown
# PWA Audit Report

**URL:** [analyzed URL]
**Date:** [current date]
**Overall Score:** [X]/127 ([percentage]%) — Grade: [letter grade]

---

## Score Breakdown

| Category | Score | Status |
|----------|-------|--------|
| Manifest Compliance | X/20 | [status emoji] |
| Advanced Manifest | X/11 | [status emoji] |
| Service Worker & Caching | X/22 | [status emoji] |
| Offline Capability | X/10 | [status emoji] |
| Installability | X/10 | [status emoji] |
| Security | X/12 | [status emoji] |
| Performance Signals | X/10 | [status emoji] |
| UX & Accessibility | X/10 | [status emoji] |
| SEO & Discoverability | X/7 | [status emoji] |
| PWA Advanced | X/15 | [status emoji] |

Status: Pass (80%+), Warn (50-79%), Fail (<50%)

---

## Critical Issues

[List any critical blockers that prevent PWA functionality]

---

## Warnings

[List important issues that should be addressed]

---

## Passed Checks

[Summarize what the PWA does well]

---

## Recommendations

### High Priority
1. [Most impactful fix]
2. [Second priority]

### Medium Priority
1. [Improvement]
2. [Enhancement]

### Quick Wins
- [Easy fix 1]
- [Easy fix 2]

---

## Resources

- [Web App Manifest | web.dev](https://web.dev/add-manifest/)
- [Service Workers | MDN](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [PWA Checklist | web.dev](https://web.dev/pwa-checklist/)
- [Workbox | Google](https://developer.chrome.com/docs/workbox/)

---

*Generated by PWA Review Skill v3.1.1*
```

---

## Error Handling

### Manifest Not Found
- Score Category 1 (Manifest Compliance) as 0/20
- Score Category 2 (Advanced Manifest) as 0/11
- Add CRITICAL issue: "No manifest.json found"
- Continue with remaining categories

### Service Worker Not Found
- Score Category 3 (Service Worker & Caching) as 0/22
- Score Category 4 (Offline Capability) as 0/10
- Reduce Category 5 (Installability) by 2 points
- Add CRITICAL issue: "No service worker registered"
- Continue with remaining categories

### CORS/Fetch Failures
- Note which resource couldn't be fetched
- Score affected categories as 0
- Add WARNING: "Could not fetch [resource] - CORS or access issue"
- Analyze whatever resources were successfully retrieved

### Invalid JSON (Manifest)
- Score manifest categories as 0
- Add CRITICAL issue: "manifest.json contains invalid JSON"
- Continue with HTML and SW analysis

---

## iOS/Safari Limitations to Note

When generating the report, include these platform-specific notes if relevant:

- iOS Safari: Push notifications not fully supported (use apple-mobile-web-app-* meta tags)
- iOS Safari: Storage limited to ~50MB
- iOS Safari: No persistent storage API
- iOS Safari: beforeinstallprompt event not supported
- Safari: Service worker scope limitations more strict

---

## Example Usage

User: `/pwa-review https://looknex.com`

Claude will:
1. Fetch https://looknex.com HTML
2. Find manifest at /manifest.json
3. Find SW at /sw.js
4. Fetch and analyze both files
5. Score across all 10 categories
6. Generate detailed report with findings

</pwa-review>
