# Changelog

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
