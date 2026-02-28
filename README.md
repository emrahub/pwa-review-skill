# PWA Review Skill for Claude Code

A comprehensive Progressive Web App audit skill that goes beyond standard Lighthouse testing. Analyzes PWAs across **11 categories** with a **192-point scoring system**, including real-time connection resilience, advanced features, and iOS-specific compatibility checks that typical audits miss.

## Features

- **192-point scoring system** across 11 categories
- **Beyond Lighthouse**: Checks advanced PWA features like `handle_links`, `launch_handler`, `file_handlers`, `protocol_handlers`
- **iOS Compatibility**: Safe area handling, splash screens, touch events, notch/Dynamic Island support
- **Core Web Vitals signals**: LCP, INP, and CLS optimization detection
- **Enhanced Security**: HSTS, CSP, Permissions-Policy, COOP/COEP checks
- **Install Experience**: beforeinstallprompt and custom install UI detection
- **Update UX**: Service worker update notification patterns
- **Actionable reports**: Each issue includes specific fix recommendations
- **No dependencies**: Runs natively in Claude Code using WebFetch

## Categories Evaluated

| Category | Points | What It Checks |
|----------|--------|----------------|
| Manifest Compliance | 20 | Required manifest fields (name, icons, display, colors) |
| Advanced Manifest | 15 | Screenshots, shortcuts, i18n, maskable icons, widgets, iOS splash screens |
| Service Worker & Caching | 33 | Registration, events, cache strategies, message handler, expiration config |
| Offline Capability | 24 | Fallback pages, app shell, sync triggers, IndexedDB, real-time resilience |
| Installability | 13 | HTTPS, manifest link, beforeinstallprompt, custom install UI |
| Security | 16 | CSP, SRI, HTTPS, COOP/COEP, HSTS, Permissions-Policy |
| Performance Signals | 17 | Render-blocking, lazy loading, resource hints, Network Info API, compression |
| UX & Accessibility | 29 | Viewport, safe areas, touch events, semantic HTML, ARIA, SPA state persistence |
| SEO & Discoverability | 7 | Meta tags, Open Graph, structured data |
| PWA Advanced | 17 | Cutting-edge PWA capabilities, Web Push |
| iOS Compatibility | 1 | Bonus for complete iOS meta tag set |

## Grading Scale

| Grade | Score Range | Percentage |
|-------|-------------|------------|
| A+ | 173+ points | 90%+ |
| A | 154-172 points | 80-89% |
| B | 135-153 points | 70-79% |
| C | 116-134 points | 60-69% |
| D | 77-115 points | 40-59% |
| F | <77 points | <40% |

## Installation

### Method 1: Add to Claude Code Skills (Recommended)

1. Copy the `SKILL.md` file to your Claude Code skills directory:
   ```bash
   # macOS/Linux
   cp SKILL.md ~/.claude/skills/pwa-review.md

   # Or create a custom skills folder
   mkdir -p ~/.claude/skills
   cp SKILL.md ~/.claude/skills/pwa-review.md
   ```

2. Restart Claude Code or reload skills

### Method 2: Project-Level Skill

Add `SKILL.md` to your project's `.claude/` directory:

```
your-project/
├── .claude/
│   └── skills/
│       └── pwa-review.md
└── ...
```

## Usage

Once installed, invoke the skill with:

```
/pwa-review https://your-pwa-url.com
```

### Example

```
/pwa-review https://looknex.com
```

Claude will:
1. Fetch the HTML from the URL
2. Discover manifest and service worker locations
3. Analyze both files against the 192-point checklist
4. Generate a detailed report with scores and recommendations

## Sample Output

```markdown
# PWA Audit Report

**URL:** https://example.com
**Date:** 2026-02-07
**Overall Score:** 165/178 (93%) — Grade: A+

## Score Breakdown

| Category | Score | Status |
|----------|-------|--------|
| Manifest Compliance | 20/20 | ✅ |
| Advanced Manifest | 15/15 | ✅ |
| Service Worker & Caching | 27/29 | ✅ |
| Offline Capability | 17/17 | ✅ |
| Installability | 13/13 | ✅ |
| Security | 14/16 | ⚠️ |
| Performance Signals | 16/16 | ✅ |
| UX & Accessibility | 25/27 | ✅ |
| SEO & Discoverability | 5/7 | ⚠️ |
| PWA Advanced | 12/17 | ⚠️ |
| iOS Compatibility | 1/1 | ✅ |

## Critical Issues
- None

## Warnings
- Missing Content Security Policy
- Missing canonical URL
- No file_handlers defined

## Recommendations
...
```

## What Makes This Different from Lighthouse

| Feature | Lighthouse | PWA Review Skill |
|---------|------------|------------------|
| `handle_links` check | ❌ | ✅ |
| `launch_handler` analysis | ❌ | ✅ |
| `file_handlers` validation | ❌ | ✅ |
| `protocol_handlers` check | ❌ | ✅ |
| `share_target` analysis | ❌ | ✅ |
| `edge_side_panel` support | ❌ | ✅ |
| `scope_extensions` check | ❌ | ✅ |
| `note_taking` (ChromeOS) | ❌ | ✅ |
| `widgets` (Windows 11) | ❌ | ✅ |
| `skipWaiting`/`clients.claim` | ❌ | ✅ |
| Navigation preload | ❌ | ✅ |
| Stale-while-revalidate | ❌ | ✅ |
| `beforeinstallprompt` | ❌ | ✅ |
| Push/notificationclick | ❌ | ✅ |
| **iOS Safe Area checks** | ❌ | ✅ |
| **iOS Splash Screens** | ❌ | ✅ |
| **Touch Event handling** | ❌ | ✅ |
| **Update UX patterns** | ❌ | ✅ |
| **Visibility change reconnection** | ❌ | ✅ |
| **Real-time reconnection strategy** | ❌ | ✅ |
| **Room re-subscribe on reconnect** | ❌ | ✅ |
| **SPA view state persistence** | ❌ | ✅ |
| Cache strategy analysis | Basic | Detailed |
| iOS-specific guidance | Limited | **Comprehensive** |

## v5.5.0 New Features (Real-Time Connection Resilience)

### Real-Time Connection Resilience (+5 points in Offline Capability)
- **Visibility change reconnection** (+2 pts) — Detects `visibilitychange` listener for WebSocket reconnection on tab return
- **Real-time reconnection strategy** (+2 pts) — Detects proper `reconnectionAttempts` (>5 or Infinity) with progressive backoff
- **Connection room re-subscribe** (+1 pt) — Detects persistent `connect` listener for room re-join after reconnection

### SPA State Persistence (+2 points in UX & Accessibility)
- **SPA view state persistence** (+2 pts) — Detects localStorage persistence for active view/conversation IDs with stale ID handling

These checks address real-world mobile PWA UX bugs where backgrounding kills WebSocket connections and SPA navigation destroys user state.

## v5.4.0 New Features (Sync Integration & Adaptive Performance)

### Service Worker & Caching Enhancements (+4 points)
- **Multiple caching strategies** (+2 pts) — Detects usage of different strategies (CacheFirst, NetworkFirst, StaleWhileRevalidate) for different resource types
- **Cache expiration config** (+1 pt) — Detects `maxEntries` or `maxAgeSeconds` for cache pruning
- **SW message handler** (+1 pt) — Detects `addEventListener('message', ...)` for client-SW communication

### Offline Capability Enhancements (+2 points)
- **Background sync client trigger** (+1 pt) — Detects `registration.sync.register()` call when coming back online
- **Periodic sync registration** (+1 pt) — Detects `registration.periodicSync.register()` on app initialization

### Performance Signals Enhancement (+1 point)
- **Network Information API** (+1 pt) — Detects `navigator.connection` for adaptive behavior on slow networks

These checks address real-world gaps discovered during LookNex PWA deep dive analysis.

## v5.3.0 New Features (Offline Storage & Performance)

### Offline Storage Enhancements (+3 points in Offline Capability)
- **Persistent storage request** (+1 pt) — Detects `navigator.storage.persist()` for iOS data persistence
- **IndexedDB offline storage** (+1 pt) — Detects `indexedDB.open()` or `idb` library for structured offline data
- **Storage quota monitoring** (+1 pt) — Detects `navigator.storage.estimate()` for storage health checks

### Performance Optimizations (+2 points in Performance Signals)
- **Compression headers** (+1 pt) — Note about `Content-Encoding: gzip/br` verification
- **Bundle chunking strategy** (+1 pt) — Detects `manualChunks`, vendor splitting patterns

These checks address production PWA requirements discovered during LookNex implementation.

## v5.2.0 New Features (Extended Theme Checks)

### Extended Theme Patterns (+5 points in UX)
- **Dark overlay theme pairs** (+1 pt) — Detects `bg-black/X` patterns without `dark:` prefix
- **Border visibility pairs** (+1 pt) — Detects `border-white/X` without light alternative
- **Hover state theme pairs** (+1 pt) — Detects hover backgrounds missing dual variants
- **Gradient theme support** (+1 pt) — Detects gradient stops without theme variants
- **Contextual text-white** (+1 pt) — Detects white text on non-colored backgrounds

These checks address common issues where alpha/opacity-based colors work in dark mode but fail in light mode.

## v5.1.0 Features (Mobile UX & State Management)

### Mobile Dropdown Positioning (+3 points in UX)
- `fixed sm:absolute` positioning pattern detection
- Viewport-relative vs container-relative positioning check
- `safe-area-inset-right/left` margin detection for dropdowns

### Update State Management (+2 points in Offline)
- localStorage flag detection for update state persistence (e.g., `pwa-just-updated`)
- Double-fire prevention for touch event handlers

### Theme Consistency (+2 points in UX)
- Light/dark theme variant detection for UI elements
- Hardcoded color warning (e.g., `bg-zinc-900` without `dark:` counterpart)

## v5.0.0 Features (iOS & Mobile Focus)

### iOS Safe Area Support (+4 points in UX)
- `viewport-fit=cover` check for notch/Dynamic Island support
- `env(safe-area-inset-*)` CSS usage detection
- Fixed header/footer safe area handling

### iOS Splash Screens (+2 points in Advanced Manifest)
- `<link rel="apple-touch-startup-image">` detection
- Multiple device size coverage check

### Touch Event Handling (+1 point in UX)
- `onTouchEnd` handler detection for iOS compatibility
- `touch-manipulation` CSS property check

### Update UX (+2 points in Offline)
- Service worker update notification patterns
- Graceful update flow detection

### Enhanced iOS/Safari Documentation
- Comprehensive safe area guidance
- Touch event best practices
- Splash screen requirements
- Z-index considerations for iOS

## Previous Versions

<details>
<summary>v4.0.0 Changes</summary>

### Service Worker & Caching (+6 points)
- `skipWaiting()` instant activation
- `clients.claim()` immediate control
- Navigation preload
- Stale-while-revalidate pattern
- Push event handler
- notificationclick handler

### Installability (+3 points)
- `beforeinstallprompt` handling
- Custom install UI detection

### Security (+4 points)
- HSTS header
- X-Content-Type-Options
- Referrer-Policy
- Permissions-Policy

### Performance Signals (+4 points)
- LCP optimization signals
- INP optimization signals
- CLS prevention
- Critical CSS inlined

### UX & Accessibility (+2 points)
- Focus indicators visible
- Skip to main content link

### Advanced Manifest (+2 points)
- `note_taking` (ChromeOS)
- `widgets` (Windows 11)

### PWA Advanced (+2 points)
- Web Push configured
- Notification permission UX

</details>

## Contributing

Contributions welcome! Please submit issues and PRs to improve the checklist or add new checks.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Resources

- [Web App Manifest | web.dev](https://web.dev/add-manifest/)
- [Service Workers | MDN](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [PWA Checklist | web.dev](https://web.dev/pwa-checklist/)
- [Workbox | Google](https://developer.chrome.com/docs/workbox/)
- [Safe Area Insets | WebKit](https://webkit.org/blog/7929/designing-websites-for-iphone-x/)

---

**Version:** 5.5.0
**Author:** [@emrahub](https://github.com/emrahub)
