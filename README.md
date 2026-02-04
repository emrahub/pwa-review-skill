# PWA Review Skill for Claude Code

A comprehensive Progressive Web App audit skill that goes beyond standard Lighthouse testing. Analyzes PWAs across **10 categories** with a **127-point scoring system**, including advanced features that typical audits miss.

## Features

- **127-point scoring system** across 10 categories
- **Beyond Lighthouse**: Checks advanced PWA features like `handle_links`, `launch_handler`, `file_handlers`, `protocol_handlers`
- **Actionable reports**: Each issue includes specific fix recommendations
- **No dependencies**: Runs natively in Claude Code using WebFetch

## Categories Evaluated

| Category | Points | What It Checks |
|----------|--------|----------------|
| Manifest Compliance | 20 | Required manifest fields (name, icons, display, colors) |
| Advanced Manifest | 11 | Screenshots, shortcuts, i18n, maskable icons |
| Service Worker & Caching | 22 | Registration, events, cache strategies, background sync |
| Offline Capability | 10 | Fallback pages, app shell, offline indicators |
| Installability | 10 | HTTPS, manifest link, install requirements |
| Security | 12 | CSP, SRI, HTTPS, COOP/COEP |
| Performance Signals | 10 | Render-blocking, lazy loading, resource hints |
| UX & Accessibility | 10 | Viewport, semantic HTML, ARIA |
| SEO & Discoverability | 7 | Meta tags, Open Graph, structured data |
| **PWA Advanced** | 15 | Cutting-edge PWA capabilities |

## Grading Scale

| Grade | Score Range |
|-------|-------------|
| A+ | 90%+ (115+ points) |
| A | 80-89% (102-114 points) |
| B | 70-79% (89-101 points) |
| C | 60-69% (77-88 points) |
| D | 40-59% (51-76 points) |
| F | <40% (<51 points) |

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
3. Analyze both files against the 127-point checklist
4. Generate a detailed report with scores and recommendations

## Sample Output

```markdown
# PWA Audit Report

**URL:** https://example.com
**Date:** 2024-01-15
**Overall Score:** 112/127 (88%) — Grade: A

## Score Breakdown

| Category | Score | Status |
|----------|-------|--------|
| Manifest Compliance | 18/20 | ✅ |
| Advanced Manifest | 9/11 | ✅ |
| Service Worker & Caching | 20/20 | ✅ |
| Offline Capability | 10/10 | ✅ |
| Installability | 10/10 | ✅ |
| Security | 7/10 | ⚠️ |
| Performance Signals | 10/10 | ✅ |
| UX & Accessibility | 10/10 | ✅ |
| SEO & Discoverability | 5/7 | ⚠️ |
| PWA Advanced | 9/15 | ⚠️ |

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
| Cache strategy analysis | Basic | Detailed |
| iOS-specific guidance | Limited | Comprehensive |

## Contributing

Contributions welcome! Please submit issues and PRs to improve the checklist or add new checks.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Resources

- [Web App Manifest | web.dev](https://web.dev/add-manifest/)
- [Service Workers | MDN](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [PWA Checklist | web.dev](https://web.dev/pwa-checklist/)
- [Workbox | Google](https://developer.chrome.com/docs/workbox/)

---

**Version:** 3.1.1
**Author:** [@emrahub](https://github.com/emrahub)
