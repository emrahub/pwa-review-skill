# PWA Best Practices Checklist & Scoring — v2.2

Total: 108 points across 9 categories.

## 1. Manifest Compliance (20 pts)

| Check | Pts | Criteria |
|-------|-----|----------|
| name | 2 | Present, non-empty |
| short_name | 2 | Present, ≤12 chars recommended |
| start_url | 2 | Present, valid path |
| display | 3 | "standalone"/"fullscreen" = 3, "minimal-ui" = 2, "browser" = 0 |
| icons | 4 | 192x192 (2) + 512x512 (2) + maskable bonus (1, max 4) |
| theme_color | 2 | Valid hex/named color |
| background_color | 2 | Valid, used for splash screen |
| scope | 1 | Present, consistent with start_url |

## 2. Advanced Manifest (11 pts)

| Check | Pts | Criteria |
|-------|-----|----------|
| id | 1 | App identity field |
| description | 1 | Needed for richer install dialog |
| screenshots | 2 | Present with form_factor (wide + narrow) |
| shortcuts | 2 | Valid quick actions (name + url) |
| orientation | 1 | Explicit orientation preference |
| categories | 1 | App store categorization hints |
| display_override | 1 | Fallback display mode chain |
| lang | 1 | BCP-47 language code for i18n |
| dir | — | Text direction (ltr/rtl/auto) — info only |
| Bonus info | 0 | share_target, protocol_handlers, file_handlers, related_applications |

## 3. Service Worker & Caching (20 pts)

| Check | Pts | Criteria |
|-------|-----|----------|
| SW registered | 4 | Registration found in HTML/JS |
| Install event | 3 | Precaches critical assets |
| Activate event | 2 | Cleans old caches |
| Fetch handler | 4 | Intercepts fetch requests |
| Cache strategy | 3 | Recognized strategy detected |
| Cache versioning | 2 | Version identifier in cache names |
| Workbox | — | Detection as bonus info |
| Navigation Preload | — | Performance optimization (info only) |
| Periodic Sync | — | Background updates (info only) |

### Cache Strategy Types
- **Cache-First**: `caches.match()` → fallback `fetch()`
- **Network-First**: `fetch()` → fallback `caches.match()`
- **Stale-While-Revalidate**: Return cache, update in background
- **Workbox**: Google's SW library detection

## 4. Offline Capability (10 pts)

| Check | Pts | Criteria |
|-------|-----|----------|
| Offline fallback | 3 | Custom offline page cached |
| App shell cached | 3 | HTML + CSS + JS precached |
| Static assets | 2 | Images, fonts cached |
| Offline indicator | 2 | navigator.onLine or online/offline events |

## 5. Installability (10 pts)

| Check | Pts | Criteria |
|-------|-----|----------|
| Manifest linked | 2 | `<link rel="manifest">` in HTML |
| HTTPS | 2 | Secure origin (or localhost) |
| SW fetch handler | 2 | Required for install prompt |
| 192px icon | 1 | Minimum install requirement |
| 512px icon | 1 | Splash screen support |
| apple-touch-icon | 1 | iOS home screen |
| beforeinstallprompt | — | Custom install UX (info only) |

## 6. Security (10 pts)

| Check | Pts | Criteria |
|-------|-----|----------|
| HTTPS | 2 | Secure origin enforced |
| CSP | 3 | Content-Security-Policy meta tag with default-src + script-src |
| SRI | 2 | Subresource Integrity on external scripts/styles |
| Mixed content | 1 | No http:// references on https page |
| SW scope | 1 | Explicitly restricted scope |
| Error handling | 1 | try/catch or .catch() in SW |

### CSP Scoring Detail
- Strong (default-src + script-src, no unsafe-eval): 3 pts
- Present but weak (missing directives or unsafe-*): 1-2 pts
- Not detected in HTML (may be in headers): 0 pts + note

## 7. Performance Signals (10 pts)

| Check | Pts | Criteria |
|-------|-----|----------|
| Render-blocking | 2 | No undeferred JS in `<head>` |
| Image optimization | 2 | Lazy loading + modern formats (webp/avif) |
| Code splitting | 2 | async/defer/module scripts ratio |
| Resource hints | 2 | preload/prefetch/preconnect/dns-prefetch |
| Font optimization | 1 | font-display: swap |
| Viewport meta | 1 | Present with proper content |

## 8. UX & Accessibility (10 pts)

| Check | Pts | Criteria |
|-------|-----|----------|
| Responsive viewport | 2 | width=device-width |
| Splash screen | 1 | name + background_color + icons |
| Semantic HTML | 2 | header, nav, main, footer, article, section, aside |
| ARIA | 2 | role attributes, aria-* attributes |
| Lang attribute | 1 | `<html lang="...">` |
| iOS status bar | 1 | apple-mobile-web-app-status-bar-style |
| Theme color meta | 1 | `<meta name="theme-color">` in HTML |

## 9. SEO & Discoverability (7 pts) — NEW

| Check | Pts | Criteria |
|-------|-----|----------|
| title | 2 | Present, 10-70 chars recommended |
| meta description | 2 | Present, 50-160 chars recommended |
| Open Graph | 2 | og:title, og:description, og:image (3+ tags = 2pts) |
| canonical URL | 1 | `<link rel="canonical">` defined |

## Grading Scale

Grades are based on **percentage** of total score (108 pts max):

| Percentage | Grade | Label |
|------------|-------|-------|
| 90%+ | A+ | Excellent PWA |
| 80-89% | A | Strong PWA |
| 70-79% | B | Good — room for improvement |
| 60-69% | C | Functional — needs significant work |
| 40-59% | D | Major PWA gaps |
| <40% | F | Not a functional PWA |
