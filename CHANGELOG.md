# Changelog

## [5.2.0] - 2026-02-06

### Added

#### Extended Theme Pattern Checks (+5 points in UX & Accessibility)
- **Dark overlay theme pairs** (+1 pt) — Detects `bg-black/X` patterns that need `dark:` prefix (e.g., `bg-white/60 dark:bg-black/60`)
- **Border visibility pairs** (+1 pt) — Detects `border-white/X` that needs light alternative (e.g., `border-zinc-200 dark:border-white/10`)
- **Hover state theme pairs** (+1 pt) — Detects hover backgrounds missing dual variants (e.g., `hover:bg-zinc-100 dark:hover:bg-white/10`)
- **Gradient theme support** (+1 pt) — Detects gradient stops without theme variants (e.g., `from-white/80 dark:from-black/80`)
- **Contextual text-white** (+1 pt) — Detects white text on non-colored/transparent backgrounds

### Changed
- **Total scoring increased from 168 to 173 points**
- UX & Accessibility: 22 → 27 points
- Updated grading scale thresholds:
  - A+: 156+ points (90%+)
  - A: 139-155 points (80-89%)
  - B: 122-138 points (70-79%)
  - C: 104-121 points (60-69%)
  - D: 70-103 points (40-59%)
  - F: <70 points (<40%)

### Notes
These additions are based on real-world theme issues discovered during LookNex PWA production testing:
- `bg-black/60` overlays invisible/wrong in light mode
- `border-white/10` borders invisible in light mode
- `hover:bg-black/10` hover states not visible in light mode
- `from-black/80` gradients incorrect in light mode
- `text-white` on transparent overlays unreadable in light mode

Alpha/opacity colors are commonly used for dark mode but require explicit light mode counterparts.

---

## [5.1.0] - 2026-02-05

### Added

#### Mobile Dropdown Positioning (+3 points in UX & Accessibility)
- **Mobile dropdown positioning** (+2 pts) — Detects `fixed sm:absolute` pattern for dropdowns that break out of positioning context on mobile
- **Dropdown safe area handling** (+1 pt) — Detects `safe-area-inset-right/left` application for notch devices

#### Update State Management (+2 points in Offline Capability)
- **Update state persistence** (+1 pt) — Detects localStorage flags (e.g., `pwa-just-updated`) to prevent update prompt re-appearing immediately after update
- **Touch event double-fire prevention** (+1 pt) — Detects guards against duplicate execution from onClick + onTouchEnd

#### Theme Consistency (+2 points in UX & Accessibility)
- **Light/dark theme consistency** (+2 pts) — Verifies UI elements have both light and `dark:` variants in Tailwind CSS

### Changed
- **Total scoring increased from 161 to 168 points**
- Offline Capability: 12 → 14 points
- UX & Accessibility: 17 → 22 points

### Notes
These additions are based on real-world iOS PWA issues discovered during production app testing:
- Dropdown positioning with `absolute` relative to narrow containers causes viewport overflow on mobile
- Update prompts re-appearing after user clicks "Update" due to missing state persistence
- Hardcoded dark colors appearing incorrectly in light theme

---

## [5.0.2] - 2026-02-05

### Added
- **Notification action buttons** (+1 pt) — Detects push notifications with actionable buttons (`actions` array) or `event.action` handling in notificationclick. Enables richer user interactions directly from notifications.

### Changed
- **Total scoring increased from 160 to 161 points**
- Service Worker & Caching: 28 → 29 points

---

## [5.0.1] - 2026-02-05

### Added
- **cursor: pointer best practice** — Added to Touch Events & Interactions section. iOS Safari requires `cursor: pointer` CSS on interactive elements to recognize them as clickable. Without this, click/touch events may not fire reliably in PWA mode.

---

## [5.0.0] - 2026-02-04

### Added

#### iOS Safe Area Support (+4 points in UX & Accessibility)
- **viewport-fit=cover check** (+2 pts) — Required for iPhone notch/Dynamic Island safe area access
- **Safe area CSS usage** (+2 pts) — Detects `env(safe-area-inset-*)` usage for fixed elements

#### iOS Splash Screens (+2 points in Advanced Manifest)
- **apple-touch-startup-image detection** (+2 pts) — iOS requires separate splash images for each device size

#### Touch Event Handling (+1 point in UX & Accessibility)
- **Touch event handlers** (+1 pt) — Detects `onTouchEnd` handlers and `touch-manipulation` CSS for iOS compatibility

#### Update UX (+2 points in Offline Capability)
- **Update prompt shown to user** (+1 pt) — Detects SW update notification patterns
- **Graceful update flow** (+1 pt) — Detects user-controlled update implementation

#### iOS Compatibility Bonus (+1 point, new category)
- **Complete iOS meta tag set** (+1 pt) — Bonus for having all iOS-specific meta tags

#### Enhanced iOS/Safari Documentation
- Comprehensive safe area handling guidance
- Touch event best practices for iOS PWA mode
- Splash screen requirements and media query patterns
- **backdrop-filter stacking context warning** — iOS Safari creates isolated stacking contexts for elements with backdrop-blur, causing z-index issues. Solution: use `transform: translate3d(0,0,0)` to force GPU layer

### Changed
- **BREAKING**: Total scoring increased from 150 to **160 points**
- UX & Accessibility: 12 → 17 points
- Advanced Manifest: 13 → 15 points
- Offline Capability: 10 → 12 points
- Added new Category 11: iOS Compatibility (1 point bonus)
- Updated grading scale thresholds:
  - A+: 144+ points (90%+)
  - A: 128-143 points (80-89%)
  - B: 112-127 points (70-79%)
  - C: 96-111 points (60-69%)
  - D: 64-95 points (40-59%)
  - F: <64 points (<40%)
- Expanded iOS/Safari limitations section with practical implementation guidance
- Added warnings for missing safe area handling and iOS splash screens

### Why This Version

This release focuses on iOS and mobile compatibility, addressing real-world issues discovered during PWA development:

1. **iPhone Notch/Dynamic Island**: Without proper safe area handling, content is obscured in PWA mode
2. **Touch Events**: `onClick` handlers don't always fire on iOS PWAs — `onTouchEnd` is essential
3. **Splash Screens**: iOS shows blank white screen without proper startup images
4. **Update UX**: Users should be notified of updates and control when they're applied

These checks ensure PWAs work correctly on iPhones, which represent a significant portion of mobile users.

---

## [4.0.0] - 2026-02-04

### Added

#### Service Worker & Caching (+6 points, now 28 total)
- **skipWaiting() usage** (+1 pt) — Detects `self.skipWaiting()` for instant SW activation
- **clients.claim() usage** (+1 pt) — Detects `clients.claim()` for immediate control
- **Navigation preload** (+1 pt) — Detects `navigationPreload.enable()` usage
- **Stale-while-revalidate pattern** (+1 pt) — Detects SWR caching strategy
- **Push event handler** (+1 pt) — Detects `addEventListener('push', ...)`
- **notificationclick handler** (+1 pt) — Detects `addEventListener('notificationclick', ...)`

#### Installability (+3 points, now 13 total)
- **beforeinstallprompt handled** (+2 pts) — Detects install prompt event listener
- **Custom install UI** (+1 pt) — Detects custom install button implementation

#### Security (+4 points, now 16 total)
- **HSTS header** (+1 pt) — Strict-Transport-Security check (note only, not detectable from HTML)
- **X-Content-Type-Options** (+1 pt) — nosniff header check
- **Referrer-Policy** (+1 pt) — Appropriate referrer policy
- **Permissions-Policy** (+1 pt) — Feature policy definition

#### Performance Signals (+4 points, now 14 total)
- **LCP optimization signals** (+1 pt) — Hero image preload, above-fold prioritization
- **INP optimization signals** (+1 pt) — Event handler optimization indicators
- **CLS prevention** (+1 pt) — Image dimensions, layout shift prevention
- **Critical CSS inlined** (+1 pt) — Critical styles in head or preloaded

#### UX & Accessibility (+2 points, now 12 total)
- **Focus indicators visible** (+1 pt) — :focus styles not removed
- **Skip to main content link** (+1 pt) — Skip link for keyboard navigation

#### Advanced Manifest (+2 points, now 13 total)
- **note_taking object** (+1 pt) — ChromeOS lock screen notes integration
- **widgets array** (+1 pt) — Windows 11 Widgets Board integration

#### PWA Advanced (+2 points, now 17 total)
- **Web Push configured** (+1 pt) — VAPID or gcm_sender_id in manifest
- **Notification permission UX** (+1 pt) — Permission timing best practice

### Changed
- **BREAKING**: Total scoring increased from 127 to **150 points**
- Updated grading scale thresholds:
  - A+: 135+ points (90%+)
  - A: 120-134 points (80-89%)
  - B: 105-119 points (70-79%)
  - C: 90-104 points (60-69%)
  - D: 60-89 points (40-59%)
  - F: <60 points (<40%)
- Report template updated for new category point totals
- Error handling updated for new SW category total (0/28)
- Issue classification expanded with new warning items

### Migration Notes
- Existing scores cannot be directly compared to v4.0.0 scores
- A "good" PWA that scored 112/127 (88%) might score ~130/150 (87%) with new checks
- New checks are additive — existing functionality still earns the same points

---

## [3.1.1] - 2026-02-04

### Fixed
- Critical Blocker text: "0/20" → "0/22" for Service Worker category (2 places)
- Background Sync check now includes `periodicsync` event detection

---

## [3.1.0] - 2026-02-04

### Added
- **Background Sync check** in Service Worker category (+2 pts) — detects `sync` event listener for offline queue processing
- **COOP/COEP check** in Security category (+2 pts) — Cross-Origin Isolation headers required for SharedArrayBuffer

### Changed
- Total scoring increased from 123 to **127 points**
- Service Worker & Caching: 20 → 22 points
- Security Measures: 10 → 12 points
- Updated grading scale thresholds for new point total
- Synchronized version numbers across all files (was showing v2.3 in some places)

### Fixed
- Version consistency: All files now show v3.1.0
- Updated sample reports to reflect new scoring structure

---

## [3.0.0] - 2026-02-04

### Changed
- **BREAKING**: Converted from Python scripts to native Claude Code skill format
- Embedded complete 123-point checklist directly in SKILL.md
- Added YAML frontmatter for proper skill registration (`user_invocable: true`)
- Added executable workflow instructions for Claude (WebFetch-based)
- Updated README with new installation and usage instructions
- Expanded to 10 categories (123 total points)

### Added
- Detailed error handling documentation
- iOS/Safari limitation notes
- Report template with exact output format
- Category-by-category scoring tables

### Removed
- Python scripts (`discover_pwa.py`, `analyze_pwa.py`, `generate_report.py`) — no longer needed
- Separate `references/pwa-checklist.md` — now embedded in SKILL.md

### Why This Change
- Zero dependencies: Works directly in Claude Code without Python
- Single command: Just run `/pwa-review <url>`
- Better CORS handling: Claude's WebFetch handles cross-origin requests
- Self-contained: All checklist items and instructions in one file

---

## [2.1.0] - 2026-02-04

### Added
- **How-to-Fix code snippets** for every finding — actionable fix instructions in report
- **Quick Wins section** — top 5 easiest fixes highlighted
- **Reference Links** — MDN, web.dev links per category
- **prefer_related_applications check** — CRITICAL installability blocker
- **Push/BackgroundSync detection** — push, notificationclick, sync, periodicsync
- **skipWaiting/clients.claim** — SW update lifecycle detection
- **Sensitive data warning** — token/auth/password keywords in SW
- **Navigation preload** detection
- **launch_handler, scope_extensions** manifest fields
- **Window Controls Overlay** specific display_override detection
- **apple-mobile-web-app-capable** scoring in installability

### Fixed
- discover_pwa.py: eliminated redundant double function calls
- README.md: "6 categories" → "8 categories"
- Font swap: now catches `display=swap` in Google Fonts URLs
- CSP note: clearer about HTTP header CSP being preferred

## [2.0.0] - 2025-02-04

### Added
- 🔒 **Security category** (10 pts) — CSP, SRI, mixed content, SW scope restriction, error handling
- 🧩 **Advanced Manifest category** (10 pts) — screenshots, shortcuts, categories, display_override, share_target, protocol_handlers, file_handlers
- beforeinstallprompt detection
- Workbox library detection
- Theme color meta tag check (separate from manifest)
- Maskable icon detail messaging

### Changed
- Rebalanced scoring to 100 pts across 8 categories (was 6)
- Removed free points for compression and touch-friendliness (can't verify from static HTML)
- More realistic scoring — good PWAs now score ~80-90 instead of inflated 99
- Improved cache strategy detection with Workbox support
- Better SRI checking with external resource ratio analysis
- Enhanced CSP analysis (unsafe-inline, unsafe-eval detection)

### Fixed
- Performance category no longer awards points for unverifiable checks
- UX category scoring proportional to actual detectable features

## [1.0.0] - 2025-02-04

### Added
- Initial release with 6 categories
