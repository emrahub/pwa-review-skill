---
name: pwa-review
description: Comprehensive 192-point PWA audit beyond Lighthouse - analyzes manifest, service worker, offline capabilities, real-time resilience, security, iOS compatibility, and advanced PWA features
user_invocable: true
args:
  - name: url
    description: The PWA URL to analyze (e.g., https://example.com)
    required: true
---

<pwa-review>

# PWA Review Skill

A comprehensive Progressive Web App audit that goes beyond standard Lighthouse testing. This skill analyzes PWAs across 11 categories with a 192-point scoring system, including real-time connection resilience, advanced features, and iOS-specific compatibility checks that typical audits miss.

## Scoring Overview

| Category | Points | Focus |
|----------|--------|-------|
| Manifest Compliance | 20 | Essential manifest fields |
| Advanced Manifest | 15 | Enhanced manifest features + iOS splash |
| Service Worker & Caching | 33 | SW implementation quality + caching strategies |
| Offline Capability | 24 | Offline functionality + storage + sync + real-time resilience |
| Installability | 13 | Install requirements |
| Security | 16 | Security measures |
| Performance Signals | 17 | Performance optimization + network detection |
| UX & Accessibility | 29 | User experience + iOS safe areas + mobile dropdowns + themes + state persistence |
| SEO & Discoverability | 7 | Search optimization |
| PWA Advanced | 17 | Cutting-edge PWA features |
| iOS Compatibility | 1 | iOS-specific meta tags (bonus) |

**Grading Scale:** A+ (173+, 90%+), A (154-172, 80-89%), B (135-153, 70-79%), C (116-134, 60-69%), D (77-115, 40-59%), F (<77, <40%)

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
- `<meta name="mobile-web-app-capable" content="...">`
- `<meta name="viewport" content="...">` (check for `viewport-fit=cover`)
- `<meta http-equiv="Content-Security-Policy" content="...">`
- `<link rel="apple-touch-icon" href="...">`
- `<link rel="apple-touch-startup-image" ...>` (iOS splash screens)

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

### Category 2: Advanced Manifest Features (15 points)

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
| `note_taking` object | 1 | manifest.note_taking exists (ChromeOS lock screen notes) |
| `widgets` array | 1 | manifest.widgets exists (Windows 11 Widgets Board) |
| iOS splash screens present | 2 | `<link rel="apple-touch-startup-image">` tags for multiple device sizes |

**iOS Splash Screen Note:** iOS requires separate `<link rel="apple-touch-startup-image">` tags for each device size. Without these, iOS shows a blank white screen during PWA launch. Check for multiple media queries covering different device dimensions.

### Category 3: Service Worker & Caching (33 points)

| Check | Points | How to Verify |
|-------|--------|---------------|
| SW registered in HTML | 2 | navigator.serviceWorker.register() found |
| `install` event handler present | 3 | SW contains addEventListener('install', ...) or self.oninstall |
| `activate` event handler present | 3 | SW contains addEventListener('activate', ...) or self.onactivate |
| `fetch` event handler present | 4 | SW contains addEventListener('fetch', ...) or self.onfetch |
| Cache API usage (caches.open/put/match) | 3 | SW contains caches.open or cache.put or cache.match |
| Cache versioning/naming strategy | 2 | SW has cache name variable (CACHE_NAME, CACHE_VERSION, etc.) |
| Old cache cleanup in activate | 2 | activate handler deletes old caches |
| Background Sync support | 2 | SW contains addEventListener('sync', ...) or addEventListener('periodicsync', ...) |
| Workbox usage (bonus, not required) | 1 | SW imports workbox or uses workbox.* methods |
| `skipWaiting()` usage | 1 | SW contains self.skipWaiting() for instant activation |
| `clients.claim()` usage | 1 | SW contains clients.claim() for immediate control |
| Navigation preload | 1 | SW uses navigationPreload.enable() |
| Stale-while-revalidate pattern | 1 | fetch handler serves cache then updates in background |
| Push event handler | 1 | SW contains addEventListener('push', ...) |
| notificationclick handler | 1 | SW contains addEventListener('notificationclick', ...) |
| Notification action buttons | 1 | Push notifications include `actions` array OR notificationclick checks `event.action` |
| Multiple caching strategies | 2 | SW uses different strategies for different routes (CacheFirst, NetworkFirst, StaleWhileRevalidate) |
| Cache expiration config | 1 | SW has maxEntries or maxAgeSeconds for cache pruning |
| SW message handler | 1 | SW contains addEventListener('message', ...) for client communication |

**Critical Blocker:** If no service worker, this category scores 0/33.

**Caching Strategies Note:** Production-grade PWAs should use different caching strategies based on resource type:
- **CacheFirst**: Static assets, fonts, images (rarely change)
- **NetworkFirst**: API responses, dynamic content (freshness matters)
- **StaleWhileRevalidate**: JS/CSS bundles (speed + freshness balance)
Look for patterns like `new CacheFirst()`, `new NetworkFirst()`, or explicit strategy patterns in fetch handlers.

**Cache Expiration Note:** Without expiration limits, caches grow unbounded and can exceed storage quotas. Look for `ExpirationPlugin` with `maxEntries` or `maxAgeSeconds`, or custom cleanup logic in the fetch handler.

### Category 4: Offline Capability (24 points)

| Check | Points | How to Verify |
|-------|--------|---------------|
| Offline fallback page defined | 3 | SW caches and serves an offline.html or similar |
| App shell resources precached | 3 | install event caches core HTML/CSS/JS files |
| Offline indicator in UI (code pattern) | 2 | Code checks navigator.onLine or listens to online/offline events |
| Network-first or cache-first strategy evident | 2 | fetch handler has clear strategy pattern |
| Update prompt shown to user | 1 | Code handles SW update with user notification (e.g., "New version available") |
| Graceful update flow | 1 | Update doesn't force reload without warning, user can choose when to update |
| Update state persistence | 1 | localStorage flag prevents update prompt re-appearing after update (e.g., `pwa-just-updated`) |
| Touch event double-fire prevention | 1 | Update/action handlers prevent duplicate execution from onClick + onTouchEnd |
| Persistent storage request | 1 | Code uses `navigator.storage.persist()` to prevent iOS data eviction |
| IndexedDB offline storage | 1 | Code uses `indexedDB.open()` or `idb` library for structured offline data |
| Storage quota monitoring | 1 | Code uses `navigator.storage.estimate()` for storage health checks |
| Background sync client trigger | 1 | Client triggers `registration.sync.register()` when coming back online |
| Periodic sync registration | 1 | Client registers `registration.periodicSync.register()` on app init |
| Visibility change reconnection | 2 | Code listens to `visibilitychange` event and triggers WebSocket/real-time reconnection when page becomes visible |
| Real-time reconnection strategy | 2 | WebSocket/Socket.io configured with sufficient reconnection attempts (>5 or Infinity) and progressive backoff |
| Connection room re-subscribe | 1 | After real-time reconnection, rooms/channels are re-joined automatically (not only on initial connect) |

**Update UX Note:** Good PWAs notify users when updates are available and let them choose when to apply the update. Look for patterns like `useRegisterSW`, `workbox-window`, or custom SW update handling with user-facing notifications.

**Background Sync Client Trigger Note:** Having a sync event handler in the service worker is not enough. The client must explicitly trigger background sync when coming back online by calling `navigator.serviceWorker.ready.then(reg => reg.sync.register('sync-pending-requests'))` in the `online` event listener. Without this, offline requests remain queued indefinitely.

**Periodic Sync Registration Note:** The service worker `periodicsync` event handler must be complemented by client-side registration during app initialization. Look for `registration.periodicSync.register('sync-content', { minInterval: ... })` wrapped in a permission check (`navigator.permissions.query({ name: 'periodic-background-sync' })`). This enables automatic background content updates even when the app is closed.

**Update State Note:** After a user clicks "Update", the PWA reloads. Without state management, the update prompt may immediately re-appear because the new service worker is still "waiting". Use localStorage flags (e.g., `pwa-just-updated` with timestamp) to suppress the prompt for a brief period (30 seconds) after update completion. Also implement double-fire prevention for touch handlers - on iOS, both `onClick` and `onTouchEnd` may fire, causing duplicate updates.

**Offline Storage Note:** For complex PWAs with user-generated content, localStorage alone is insufficient. Use IndexedDB for structured data storage (images, generation history, preferences). Request persistent storage with `navigator.storage.persist()` to prevent iOS from evicting data after 7 days of inactivity. Monitor storage quota with `navigator.storage.estimate()` to warn users before running out of space.

**Visibility Change Reconnection Note:** When a PWA is minimized, tab-switched, or the user navigates to another app on mobile, WebSocket/real-time connections silently die. The browser fires `visibilitychange` when the user returns, but most apps don't listen for it. Without a `visibilitychange` handler that checks connection state and triggers reconnection, users return to a permanently disconnected app. This is especially critical on iOS where PWAs are effectively frozen when backgrounded. Look for:
```javascript
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible' && !socket.connected) {
    socket.connect(); // or custom reconnect logic
  }
});
```

**Real-Time Reconnection Strategy Note:** Socket.io and similar libraries default to limited reconnection attempts (e.g., 5 attempts). In a PWA context where users may background the app for hours, 5 attempts are exhausted in ~15 seconds — long before the user returns. Production PWAs should configure `reconnectionAttempts: Infinity` with a reasonable `reconnectionDelayMax` (e.g., 30 seconds) for progressive backoff. Also provide a manual retry mechanism in the UI so users can trigger immediate reconnection. Look for:
- `reconnectionAttempts` configuration (should be high or Infinity)
- `reconnectionDelayMax` configuration (should be >5000ms)
- Manual reconnect button or tap-to-retry UI
- `reconnect_failed` event handling

**Connection Room Re-Subscribe Note:** After a WebSocket reconnection, the server-side room/channel memberships are lost. If the app only joins rooms on initial connection (e.g., in a `useEffect([workspaceId])` that doesn't re-trigger on reconnect), real-time events stop flowing after reconnection. The fix is to listen for the `connect` event persistently and re-join rooms on every reconnection — not just the first connection. Look for patterns where room-joining logic is called inside a persistent `connect` event listener rather than a self-removing one.

### Category 5: Installability Requirements (13 points)

| Check | Points | How to Verify |
|-------|--------|---------------|
| Served over HTTPS | 3 | URL starts with https:// |
| Valid manifest linked in HTML | 2 | <link rel="manifest"> exists with valid href |
| Service worker with fetch handler | 2 | Covered in SW category, cross-check |
| 192x192 icon present | 1 | Covered in manifest, cross-check |
| 512x512 icon present | 1 | Covered in manifest, cross-check |
| `apple-touch-icon` for iOS | 1 | <link rel="apple-touch-icon"> in HTML |
| `beforeinstallprompt` handled | 2 | HTML/JS contains beforeinstallprompt event listener |
| Custom install UI | 1 | Code shows/hides custom install button |

**Note:** `prefer_related_applications: true` in manifest BLOCKS browser install prompt - flag as CRITICAL if found.

### Category 6: Security Measures (16 points)

| Check | Points | How to Verify |
|-------|--------|---------------|
| HTTPS enforced | 2 | URL is https:// (duplicate check for emphasis) |
| Content Security Policy present | 3 | CSP meta tag or mention in SW/HTML |
| Subresource Integrity (SRI) on scripts | 2 | <script> tags have integrity="sha..." |
| No mixed content | 2 | No http:// resources loaded on https:// page |
| scope restricted appropriately | 1 | manifest.scope doesn't expose unnecessary paths |
| Cross-Origin Isolation (COOP/COEP) | 2 | Headers: Cross-Origin-Opener-Policy, Cross-Origin-Embedder-Policy |
| HSTS header | 1 | Strict-Transport-Security header (note: not detectable from HTML) |
| X-Content-Type-Options | 1 | nosniff header present (note: not detectable from HTML) |
| Referrer-Policy | 1 | Appropriate referrer policy set via meta or header |
| Permissions-Policy | 1 | Feature policy defined (note: not detectable from HTML) |

**Note:** Some security headers (HSTS, X-Content-Type-Options, Permissions-Policy) cannot be verified from HTML alone. Mark as "Unable to verify" unless response headers are available.

### Category 7: Performance Signals (17 points)

| Check | Points | How to Verify |
|-------|--------|---------------|
| No render-blocking scripts in head | 2 | Scripts have defer/async or are at body end |
| Images have lazy loading | 2 | <img loading="lazy"> or Intersection Observer usage |
| Resource hints present | 2 | <link rel="preload/prefetch/preconnect"> found |
| Code splitting indicators | 2 | Multiple JS chunks or dynamic import() usage |
| Font optimization | 2 | font-display: swap or preloaded fonts |
| LCP optimization signals | 1 | Hero image preloaded, above-fold content prioritized |
| INP optimization signals | 1 | No long tasks, event handlers optimized (qualitative) |
| CLS prevention | 1 | Images have width/height, no layout shifts expected |
| Critical CSS inlined | 1 | Critical styles in <head> or preloaded |
| Compression headers | 1 | Server returns `Content-Encoding: gzip` or `br` (note: verify via DevTools) |
| Bundle chunking strategy | 1 | Build uses `manualChunks`, vendor splitting, or separate runtime chunks |
| Network Information API usage | 1 | Code uses `navigator.connection` for adaptive behavior on slow networks |

**Compression Note:** Gzip/Brotli compression can reduce bundle sizes by 60-80%. This cannot be verified from HTML alone - check Network tab in DevTools for `Content-Encoding` response header. Build tools like `vite-plugin-compression` can generate pre-compressed `.gz` and `.br` files.

**Bundle Chunking Note:** Good build configurations split vendor dependencies (React, UI libraries, i18n) into separate chunks. Look for patterns like `manualChunks` in Vite/Rollup config or webpack's `splitChunks`. This enables better caching (vendor chunks change less frequently) and parallel loading.

**Network Information API Note:** The Network Information API (`navigator.connection`) enables adaptive behavior based on connection quality. Look for patterns that check `connection.effectiveType` (4g/3g/2g/slow-2g), `connection.saveData`, or `connection.downlink`. PWAs can reduce image quality, disable prefetching, or extend API timeouts on slow connections. Example:
```javascript
const conn = navigator.connection;
if (conn?.effectiveType === '2g' || conn?.saveData) {
  // Load low-quality images, disable autoplay, extend timeouts
}
```

### Category 8: UX & Accessibility (29 points)

| Check | Points | How to Verify |
|-------|--------|---------------|
| Responsive viewport meta | 2 | <meta name="viewport" content="width=device-width, initial-scale=1"> |
| `viewport-fit=cover` for safe areas | 2 | Viewport meta includes `viewport-fit=cover` (required for iOS notch/Dynamic Island) |
| Safe area CSS usage | 2 | Code uses `env(safe-area-inset-*)` for fixed/sticky elements |
| Semantic HTML structure | 2 | <main>, <nav>, <header>, <footer> tags present |
| ARIA landmarks or roles | 2 | role="..." or aria-* attributes found |
| Language declared | 2 | <html lang="..."> attribute present |
| Touch-friendly targets | 2 | No evidence of tiny click targets (qualitative) |
| Touch event handling for iOS | 1 | Critical buttons have `onTouchEnd` handlers or `touch-manipulation` CSS |
| Focus indicators visible | 1 | :focus styles not removed, visible outlines (qualitative) |
| Skip to main content link | 1 | Skip link present for keyboard navigation |
| Mobile dropdown positioning | 2 | Dropdowns use `fixed` on mobile, `absolute` on desktop with proper margins |
| Dropdown safe area handling | 1 | Dropdowns apply `safe-area-inset-right/left` for notch devices |
| Theme consistency (light/dark) | 2 | All UI elements have both light and `dark:` variants in Tailwind/CSS |
| Dark overlay theme pairs | 1 | `bg-black/X` patterns have `dark:` prefix (e.g., `bg-white/60 dark:bg-black/60`) |
| Border visibility pairs | 1 | `border-white/X` has light alternative (e.g., `border-zinc-200 dark:border-white/10`) |
| Hover state theme pairs | 1 | Hover backgrounds have both variants (e.g., `hover:bg-zinc-100 dark:hover:bg-white/10`) |
| Gradient theme support | 1 | Gradient stops have variants (e.g., `from-white/80 dark:from-black/80`) |
| Contextual text-white | 1 | White text only on colored backgrounds, not transparent overlays |
| SPA view state persistence | 2 | Active view/tab/conversation ID persisted to localStorage so navigation back restores user's position |

**iOS Safe Area Note:** iPhone notch and Dynamic Island require special handling. Without `viewport-fit=cover` and `env(safe-area-inset-*)` CSS, content may be obscured or buttons may be unreachable in PWA standalone mode. Fixed headers should use `padding-top: env(safe-area-inset-top)` and bottom navigation should account for `safe-area-inset-bottom`.

**Touch Event Note:** On iOS, `onClick` handlers may not fire reliably in PWA mode. Critical action buttons (update, install, submit) should include `onTouchEnd` handlers as backup. The CSS property `touch-manipulation` prevents double-tap zoom delays.

**Mobile Dropdown Positioning Note:** Dropdowns positioned with `absolute` relative to a small parent element (like a button) often extend beyond the viewport on mobile. Solution: Use `fixed` positioning on mobile to break out of the parent's positioning context, then use `left-4 right-4` (or similar) for consistent margins instead of transform centering (`left-1/2 -translate-x-1/2`). On desktop (`sm:` breakpoint), revert to `absolute` with `right-0` for proper alignment. Always apply `safe-area-inset-right` via inline style for notch devices.

**Theme Consistency Note:** In Tailwind CSS projects, all UI elements should have both light and dark variants. Look for patterns like `bg-zinc-100 dark:bg-zinc-900`. Hardcoded colors without a `dark:` counterpart (e.g., `bg-zinc-900` alone) will appear incorrectly in light mode. Common problem areas: tooltips, buttons, borders, and dropdown backgrounds.

**Extended Theme Checks Note:** Alpha/opacity-based colors (`bg-black/60`, `border-white/10`, `from-black/80`) are commonly used for dark mode but invisible or wrong in light mode. Each pattern needs a light mode counterpart:
- `bg-black/60` → `bg-white/60 dark:bg-black/60`
- `border-white/10` → `border-zinc-200 dark:border-white/10`
- `hover:bg-black/10` → `hover:bg-zinc-100 dark:hover:bg-white/10`
- `from-black/80` → `from-white/80 dark:from-black/80`
- `text-white` on overlays → `text-zinc-900 dark:text-white`
These patterns are frequently missed because they work in dark mode (the default design) but break in light mode.

**SPA View State Persistence Note:** In SPA-based PWAs, navigating away from a view (back button, tab switch, or mobile gesture) unmounts React/Vue components, destroying all in-memory state. When the user returns, they lose their position — active chat conversation, selected tab, scroll position, form data, etc. This is especially painful on mobile PWAs where accidental back gestures are common. The fix is lightweight: persist critical view identifiers (active conversation ID, selected tab, last viewed item) to localStorage keyed by context (e.g., `chat-active-${workspaceId}`). On mount, restore from localStorage and load data from the API. Don't cache full data in localStorage — just the identifier needed to restore the view. Also handle stale IDs gracefully (e.g., if a persisted conversation ID returns 404, clear it and show the default view instead of an error).

### Category 9: SEO & Discoverability (7 points)

| Check | Points | How to Verify |
|-------|--------|---------------|
| `<title>` tag present | 1 | HTML has <title> with content |
| Meta description | 2 | <meta name="description" content="..."> |
| Open Graph tags | 2 | og:title, og:description, og:image present |
| Canonical URL | 1 | <link rel="canonical" href="..."> |
| Structured data (JSON-LD) | 1 | <script type="application/ld+json"> found |

### Category 10: PWA Advanced Capabilities (17 points)

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
| Web Push configured | 1 | VAPID or gcm_sender_id in manifest |
| Notification permission UX | 1 | Permission requested after user action, not on load |

### Category 11: iOS Compatibility Bonus (1 point)

| Check | Points | How to Verify |
|-------|--------|---------------|
| Complete iOS meta tag set | 1 | Has `apple-mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style`, AND `mobile-web-app-capable` |

**Note:** This is a bonus point for PWAs that have complete iOS compatibility meta tags. The individual checks are scored in their respective categories, but having the complete set demonstrates attention to cross-platform compatibility.

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
- No skipWaiting/clients.claim
- No beforeinstallprompt handling
- Missing `viewport-fit=cover` (iOS safe areas won't work)
- No `env(safe-area-inset-*)` usage for fixed elements
- Missing iOS splash screens
- No update notification UX for users
- No update state persistence (prompt may re-appear after update)
- Dropdowns use absolute positioning without mobile viewport handling
- Hardcoded colors without light/dark theme variants
- `bg-black/X` patterns without `dark:` prefix (invisible in light mode)
- `border-white/X` patterns without light alternative (invisible in light mode)
- `hover:bg-black/X` or `hover:bg-white/X` without theme pair
- Gradient stops without theme variants
- `text-white` on transparent/overlay backgrounds (unreadable in light mode)
- No `visibilitychange` handler for real-time reconnection (connection lost when returning to app)
- WebSocket reconnection attempts too low (≤5 exhausted before user returns)
- No room/channel re-subscribe after real-time reconnection (events stop flowing)
- No SPA view state persistence (user loses position on navigation)

### Informational (Nice to Have)
- Missing advanced manifest features
- No PWA advanced capabilities
- No structured data
- Missing shortcuts
- No navigation preload
- No stale-while-revalidate
- No persistent storage request (iOS data may be evicted)
- No IndexedDB usage (limited to localStorage)
- No storage quota monitoring
- No compression headers detected
- No bundle chunking strategy evident
- No background sync client trigger (offline requests never sync)
- No periodic sync registration (no background updates)
- No Network Information API usage (no adaptive behavior on slow networks)
- Single caching strategy for all resources (not optimized)
- No cache expiration config (unbounded cache growth)

---

## Report Template

Generate the report in this exact format:

```markdown
# PWA Audit Report

**URL:** [analyzed URL]
**Date:** [current date]
**Overall Score:** [X]/192 ([percentage]%) — Grade: [letter grade]

---

## Score Breakdown

| Category | Score | Status |
|----------|-------|--------|
| Manifest Compliance | X/20 | [status emoji] |
| Advanced Manifest | X/15 | [status emoji] |
| Service Worker & Caching | X/33 | [status emoji] |
| Offline Capability | X/24 | [status emoji] |
| Installability | X/13 | [status emoji] |
| Security | X/16 | [status emoji] |
| Performance Signals | X/17 | [status emoji] |
| UX & Accessibility | X/29 | [status emoji] |
| SEO & Discoverability | X/7 | [status emoji] |
| PWA Advanced | X/17 | [status emoji] |
| iOS Compatibility | X/1 | [status emoji] |

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

*Generated by PWA Review Skill v5.5.0*
```

---

## Error Handling

### Manifest Not Found
- Score Category 1 (Manifest Compliance) as 0/20
- Score Category 2 (Advanced Manifest) as 0/13
- Add CRITICAL issue: "No manifest.json found"
- Continue with remaining categories

### Service Worker Not Found
- Score Category 3 (Service Worker & Caching) as 0/33
- Score Category 4 (Offline Capability) as 0/24
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

### Installation & Capabilities
- iOS Safari: `beforeinstallprompt` event not supported (users must manually "Add to Home Screen")
- iOS Safari: Push notifications require iOS 16.4+ and explicit user permission
- iOS Safari: Storage limited to ~50MB (may be evicted under storage pressure)
- iOS Safari: No persistent storage API
- Safari: Service worker scope limitations more strict

### Real-Time Connections
- iOS PWAs are frozen when backgrounded — WebSocket connections die silently (close code 1005)
- When user returns to the app, socket.io's limited reconnection attempts may already be exhausted
- `visibilitychange` event is the reliable signal for detecting return from background on both iOS and Android
- After reconnection, server-side room memberships are lost — must re-join rooms on every `connect` event
- SPA component state is destroyed on navigation — persist critical IDs (active conversation, selected tab) to localStorage

### Safe Area & Display (Critical for PWA Mode)
- **Notch/Dynamic Island**: Without `viewport-fit=cover` in viewport meta, `env(safe-area-inset-*)` won't work
- **Fixed Headers**: Must use `padding-top: env(safe-area-inset-top)` to avoid content being hidden behind notch
- **Fixed Bottom Elements**: Must use `padding-bottom: env(safe-area-inset-bottom)` for home indicator area
- **Status Bar**: `apple-mobile-web-app-status-bar-style` can be `default`, `black`, or `black-translucent`
- PWA mode on iOS shows no browser chrome - safe area handling is essential

### Touch Events & Interactions
- `onClick` handlers may not fire reliably on some iOS versions in PWA mode
- Add `onTouchEnd` as backup for critical buttons (install, update, submit actions)
- Use `touch-manipulation` CSS to eliminate 300ms tap delay and prevent double-tap zoom
- Use `cursor: pointer` CSS on interactive elements - iOS Safari requires this to recognize elements as clickable
- Use `-webkit-tap-highlight-color: transparent` for clean visual feedback
- Use `-webkit-user-select: none` on interactive elements to prevent text selection

### Splash Screens
- iOS requires `<link rel="apple-touch-startup-image">` with media queries for each device size
- Without splash screens, iOS shows blank white screen during PWA launch
- Each iPhone/iPad dimension needs its own splash image (portrait and landscape)

### Z-Index & Stacking Context (Critical)
- **backdrop-filter creates new stacking context**: Headers with `backdrop-blur` or `backdrop-filter` create isolated stacking contexts in iOS Safari. Elements with higher z-index values may still appear BEHIND these elements.
- **Fix**: Add `transform: translate3d(0,0,0)` to elements that need to appear above backdrop-filter elements. This forces GPU layer rendering and fixes stacking order.
- Toast/notification components must have high z-index (e.g., `z-[9999]`) AND `transform: translate3d(0,0,0)` to appear above blurred headers
- iOS Safari has stricter stacking context behavior than Chrome/Firefox

**Example fix for notifications above blurred headers:**
```css
.notification {
  position: fixed;
  z-index: 9999;
  transform: translate3d(0,0,0); /* Forces GPU layer, fixes iOS stacking */
}
```

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
