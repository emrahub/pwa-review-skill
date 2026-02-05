# PWA Review Skill for Claude Code

A comprehensive Progressive Web App audit skill that goes beyond standard Lighthouse testing. Analyzes PWAs across **11 categories** with a **168-point scoring system**, including advanced features and iOS-specific compatibility checks that typical audits miss.

## Features

- **168-point scoring system** across 11 categories
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
| Service Worker & Caching | 29 | Registration, events, cache strategies, skipWaiting, clients.claim, push, navigation preload |
| Offline Capability | 14 | Fallback pages, app shell, offline indicators, update UX, state persistence |
| Installability | 13 | HTTPS, manifest link, beforeinstallprompt, custom install UI |
| Security | 16 | CSP, SRI, HTTPS, COOP/COEP, HSTS, Permissions-Policy |
| Performance Signals | 14 | Render-blocking, lazy loading, resource hints, Core Web Vitals signals |
| UX & Accessibility | 22 | Viewport, safe areas, touch events, semantic HTML, ARIA, mobile dropdowns, themes |
| SEO & Discoverability | 7 | Meta tags, Open Graph, structured data |
| PWA Advanced | 17 | Cutting-edge PWA capabilities, Web Push |
| iOS Compatibility | 1 | Bonus for complete iOS meta tag set |

## Grading Scale

| Grade | Score Range | Percentage |
|-------|-------------|------------|
| A+ | 152+ points | 90%+ |
| A | 135-151 points | 80-89% |
| B | 118-134 points | 70-79% |
| C | 101-117 points | 60-69% |
| D | 68-100 points | 40-59% |
| F | <68 points | <40% |

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
3. Analyze both files against the 168-point checklist
4. Generate a detailed report with scores and recommendations

## Sample Output

```markdown
# PWA Audit Report

**URL:** https://example.com
**Date:** 2026-02-04
**Overall Score:** 155/168 (92%) — Grade: A+

## Score Breakdown

| Category | Score | Status |
|----------|-------|--------|
| Manifest Compliance | 20/20 | ✅ |
| Advanced Manifest | 15/15 | ✅ |
| Service Worker & Caching | 27/29 | ✅ |
| Offline Capability | 14/14 | ✅ |
| Installability | 13/13 | ✅ |
| Security | 14/16 | ⚠️ |
| Performance Signals | 14/14 | ✅ |
| UX & Accessibility | 20/22 | ✅ |
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
| Cache strategy analysis | Basic | Detailed |
| iOS-specific guidance | Limited | **Comprehensive** |

## v5.1.0 New Features (Mobile UX & State Management)

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

**Version:** 5.1.0
**Author:** [@emrahub](https://github.com/emrahub)
