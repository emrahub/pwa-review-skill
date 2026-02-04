#!/usr/bin/env python3
"""Analyze PWA resources and generate scored findings. v2.2 — comprehensive audit."""

import argparse
import json
import re
import sys
from pathlib import Path


# ── How-to-Fix snippets for common issues ─────────────────────────────
FIX_HINTS = {
    "no_manifest": 'Create a `manifest.json` and add `<link rel="manifest" href="/manifest.json">` in your HTML `<head>`.',
    "no_name": 'Add `"name": "Your App Name"` to manifest.json.',
    "no_short_name": 'Add `"short_name": "AppName"` (≤12 chars) to manifest.json.',
    "no_start_url": 'Add `"start_url": "/"` or `"start_url": "/index.html"` to manifest.json.',
    "display_browser": 'Set `"display": "standalone"` in manifest.json for app-like experience.',
    "no_192_icon": 'Add a 192x192 PNG icon: `{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}`.',
    "no_512_icon": 'Add a 512x512 PNG icon for splash screen support.',
    "no_maskable": 'Add a maskable icon: `{"src": "/icon-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}`. Use https://maskable.app to test.',
    "no_theme_color": 'Add `"theme_color": "#your-color"` to manifest.json.',
    "no_bg_color": 'Add `"background_color": "#ffffff"` to manifest.json for splash screen.',
    "no_description": 'Add `"description": "Brief app description"` to manifest.json — needed for richer install UI.',
    "no_screenshots": 'Add screenshots with form_factor:\n```json\n"screenshots": [\n  {"src": "/ss-wide.png", "sizes": "1280x720", "type": "image/png", "form_factor": "wide"},\n  {"src": "/ss-narrow.png", "sizes": "750x1334", "type": "image/png", "form_factor": "narrow"}\n]\n```',
    "no_shortcuts": 'Add shortcuts:\n```json\n"shortcuts": [{"name": "New Item", "url": "/new", "icons": [{"src": "/icon-new.png", "sizes": "96x96"}]}]\n```',
    "no_sw": 'Register a service worker:\n```js\nif ("serviceWorker" in navigator) {\n  navigator.serviceWorker.register("/sw.js");\n}\n```',
    "no_install_event": 'Precache in SW install:\n```js\nself.addEventListener("install", e => {\n  e.waitUntil(caches.open("v1").then(c => c.addAll(["/", "/style.css", "/app.js"])));\n});\n```',
    "no_activate_event": 'Clean old caches:\n```js\nself.addEventListener("activate", e => {\n  e.waitUntil(caches.keys().then(keys =>\n    Promise.all(keys.filter(k => k !== CURRENT).map(k => caches.delete(k)))\n  ));\n});\n```',
    "no_fetch_handler": 'Add fetch handler:\n```js\nself.addEventListener("fetch", e => {\n  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));\n});\n```',
    "no_cache_version": 'Use versioned cache names: `const CACHE = "app-v2";` and clean old versions in activate.',
    "no_offline_fallback": 'Cache an offline page and serve on fetch fail:\n```js\n.catch(() => caches.match("/offline.html"))\n```',
    "no_offline_indicator": 'Detect offline state:\n```js\nwindow.addEventListener("offline", () => showBanner("You are offline"));\nwindow.addEventListener("online", () => hideBanner());\n```',
    "no_manifest_link": 'Add `<link rel="manifest" href="/manifest.json">` in `<head>`.',
    "no_https": "Serve your site over HTTPS. Use Let's Encrypt for free TLS certificates.",
    "no_apple_touch_icon": 'Add `<link rel="apple-touch-icon" href="/apple-touch-icon.png">` (180×180px).',
    "no_csp": 'Add CSP meta tag:\n```html\n<meta http-equiv="Content-Security-Policy"\n  content="default-src \'self\'; script-src \'self\'; style-src \'self\' \'unsafe-inline\'">\n```\nOr better: set via HTTP header.',
    "no_sri": 'Add integrity to external scripts:\n```html\n<script src="https://cdn.example.com/lib.js"\n  integrity="sha384-..." crossorigin="anonymous"></script>\n```\nGenerate hashes at https://www.srihash.org/',
    "mixed_content": 'Replace all `http://` references with `https://` in src, href, and action attributes.',
    "no_sw_error_handling": 'Wrap fetch logic in .catch():\n```js\nfetch(e.request).catch(() => caches.match("/offline.html"))\n```',
    "render_blocking": 'Add `async`, `defer`, or `type="module"` to `<script>` tags in `<head>`.',
    "no_lazy_loading": 'Add `loading="lazy"` to below-fold `<img>` tags.',
    "no_modern_images": 'Use WebP/AVIF with `<picture>` fallback.',
    "no_resource_hints": 'Add resource hints:\n```html\n<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preload" href="/critical.css" as="style">\n```',
    "no_font_swap": 'Add `font-display: swap` to @font-face, or `&display=swap` to Google Fonts URLs.',
    "no_viewport": 'Add `<meta name="viewport" content="width=device-width, initial-scale=1">` in `<head>`.',
    "no_semantic_html": 'Use semantic elements: `<header>`, `<nav>`, `<main>`, `<footer>`, `<article>`, `<section>`.',
    "no_aria": 'Add ARIA: `role="navigation"`, `aria-label="..."`, `aria-hidden="true"` where needed.',
    "no_lang": 'Add language: `<html lang="en">` (use your BCP-47 language code).',
    "no_theme_meta": 'Add `<meta name="theme-color" content="#your-color">` in `<head>`. Separate from manifest theme_color.',
    "prefer_related": 'Remove or set to false: `"prefer_related_applications": false` — otherwise browser will NOT show PWA install prompt.',
    "no_manifest_lang": 'Add `"lang": "en"` (or your BCP-47 language code) to manifest.json for i18n support.',
    "no_title": 'Add a descriptive `<title>` tag (10-70 chars) in `<head>`.',
    "no_meta_desc": 'Add `<meta name="description" content="Your description (50-160 chars)">` in `<head>`.',
}


class PWAAnalyzer:
    def __init__(self, html: str, manifest: dict | None, sw: str | None, url: str):
        self.html = html
        self.manifest = manifest
        self.sw = sw
        self.url = url
        self.findings = {"critical": [], "warnings": [], "passed": [], "info": []}

    def _add(self, level: str, category: str, message: str, detail: str = "", fix_key: str = ""):
        entry = {"category": category, "message": message, "detail": detail}
        if fix_key and fix_key in FIX_HINTS:
            entry["fix"] = FIX_HINTS[fix_key]
        self.findings[level].append(entry)

    # ── 1. Manifest Compliance (20 pts) ─────────────────────────────────
    def analyze_manifest(self) -> dict:
        score = 0
        cat = "Manifest"
        if not self.manifest:
            self._add("critical", cat, "No manifest.json found",
                       "PWA requires a valid web app manifest", "no_manifest")
            return {"score": 0, "max": 20}

        m = self.manifest

        # name (2)
        if m.get("name"):
            score += 2; self._add("passed", cat, f"name: '{m['name']}'")
        else:
            self._add("critical", cat, "Missing 'name' in manifest", "", "no_name")

        # short_name (2)
        sn = m.get("short_name", "")
        if sn:
            score += 2
            if len(sn) > 12:
                self._add("warnings", cat, f"short_name '{sn}' is {len(sn)} chars — recommend ≤12")
            else:
                self._add("passed", cat, f"short_name: '{sn}' ({len(sn)} chars)")
        else:
            self._add("warnings", cat, "Missing 'short_name'", "", "no_short_name")

        # start_url (2)
        if m.get("start_url"):
            score += 2; self._add("passed", cat, f"start_url: '{m['start_url']}'")
        else:
            self._add("critical", cat, "Missing 'start_url'", "", "no_start_url")

        # display (3)
        display = m.get("display", "browser")
        if display in ("standalone", "fullscreen"):
            score += 3; self._add("passed", cat, f"display: '{display}'")
        elif display == "minimal-ui":
            score += 2; self._add("warnings", cat, "display 'minimal-ui' — 'standalone' preferred")
        else:
            self._add("critical", cat, f"display: '{display}' — not installable as standalone", "", "display_browser")

        # icons (4)
        icons = m.get("icons", [])
        sizes_found = set()
        has_maskable = False
        for icon in icons:
            for s in str(icon.get("sizes", "")).split():
                sizes_found.add(s)
            if "maskable" in str(icon.get("purpose", "")):
                has_maskable = True
        icon_score = 0
        if "192x192" in sizes_found: icon_score += 2
        else: self._add("critical", cat, "Missing 192x192 icon (required for install)", "", "no_192_icon")
        if "512x512" in sizes_found: icon_score += 2
        else: self._add("warnings", cat, "Missing 512x512 icon (splash screen)", "", "no_512_icon")
        if has_maskable:
            icon_score = min(icon_score + 1, 4)
            self._add("passed", cat, "Maskable icon found (adaptive icon support)")
        else:
            self._add("warnings", cat, "No maskable icon — no adaptive icon on Android", "", "no_maskable")
        score += icon_score
        if icon_score >= 3:
            self._add("passed", cat, f"Icons: {', '.join(sorted(sizes_found))}")

        # theme_color (2)
        if m.get("theme_color"):
            score += 2; self._add("passed", cat, f"theme_color: '{m['theme_color']}'")
        else:
            self._add("warnings", cat, "Missing theme_color", "", "no_theme_color")

        # background_color (2)
        if m.get("background_color"):
            score += 2; self._add("passed", cat, f"background_color: '{m['background_color']}'")
        else:
            self._add("warnings", cat, "Missing background_color (splash screen)", "", "no_bg_color")

        # scope (1)
        if m.get("scope"):
            score += 1; self._add("passed", cat, f"scope: '{m['scope']}'")
        else:
            self._add("info", cat, "No explicit scope (defaults to manifest directory)")

        return {"score": min(score, 20), "max": 20}

    # ── 2. Advanced Manifest (11 pts) ───────────────────────────────────
    def analyze_advanced_manifest(self) -> dict:
        score = 0
        cat = "Advanced Manifest"
        if not self.manifest:
            self._add("info", cat, "Skipped — no manifest available")
            return {"score": 0, "max": 11}
        m = self.manifest

        # id (1)
        if m.get("id"):
            score += 1; self._add("passed", cat, f"id: '{m['id']}'")
        else:
            self._add("info", cat, "No 'id' — browser auto-generates from start_url")

        # description (1)
        if m.get("description"):
            score += 1; self._add("passed", cat, "description present")
        else:
            self._add("warnings", cat, "No description — needed for richer install UI", "", "no_description")

        # screenshots (2)
        screenshots = m.get("screenshots", [])
        if screenshots:
            has_wide = any("wide" in str(s.get("form_factor", "")) for s in screenshots)
            has_narrow = any("narrow" in str(s.get("form_factor", "")) for s in screenshots)
            if has_wide and has_narrow:
                score += 2; self._add("passed", cat, f"screenshots: {len(screenshots)} (wide + narrow)")
            else:
                score += 1
                self._add("warnings", cat, "screenshots found but missing form_factor variants (wide/narrow)", "", "no_screenshots")
        else:
            self._add("warnings", cat, "No screenshots — Chrome shows basic install dialog", "", "no_screenshots")

        # shortcuts (2)
        shortcuts = m.get("shortcuts", [])
        if shortcuts:
            valid = all(s.get("name") and s.get("url") for s in shortcuts)
            if valid:
                score += 2; self._add("passed", cat, f"shortcuts: {len(shortcuts)} quick actions")
            else:
                score += 1; self._add("warnings", cat, "shortcuts: some missing name/url", "", "no_shortcuts")
        else:
            self._add("info", cat, "No shortcuts (optional quick actions)")

        # orientation (1)
        if m.get("orientation"):
            score += 1; self._add("passed", cat, f"orientation: '{m['orientation']}'")
        else:
            self._add("info", cat, "No orientation set (defaults to any)")

        # categories (1)
        if m.get("categories"):
            score += 1; self._add("passed", cat, f"categories: {m['categories']}")
        else:
            self._add("info", cat, "No categories (app store discovery)")

        # display_override (1)
        if m.get("display_override"):
            score += 1
            modes = m["display_override"]
            self._add("passed", cat, f"display_override: {modes}")
            if "window-controls-overlay" in modes:
                self._add("info", cat, "Window Controls Overlay enabled — native-like title bar on desktop")
        else:
            self._add("info", cat, "No display_override fallback chain")

        # lang (1) - i18n support
        if m.get("lang"):
            score += 1
            self._add("passed", cat, f"lang: '{m['lang']}' (i18n support)")
        else:
            self._add("warnings", cat, "No 'lang' field — needed for i18n", "", "no_manifest_lang")

        # dir (info) - RTL support
        if m.get("dir") in ("ltr", "rtl", "auto"):
            self._add("passed", cat, f"dir: '{m['dir']}' (text direction)")
        else:
            self._add("info", cat, "No 'dir' field — defaults to 'auto'")

        # Bonus info fields (0 pts)
        for field, label in [
            ("share_target", "Web Share Target API"),
            ("protocol_handlers", "Protocol handlers"),
            ("file_handlers", "File handlers"),
            ("related_applications", "Related native apps"),
            ("launch_handler", "Launch handler"),
            ("scope_extensions", "Scope extensions (multi-origin)"),
            ("handle_links", "Link handling preference"),
        ]:
            if m.get(field):
                self._add("passed", cat, f"{label} configured")

        return {"score": min(score, 11), "max": 11}

    # ── 3. Service Worker & Caching (20 pts) ────────────────────────────
    def analyze_service_worker(self) -> dict:
        score = 0
        cat = "Service Worker"

        sw_registered = bool(re.search(r'serviceWorker\.register', self.html, re.I))
        if sw_registered:
            score += 4; self._add("passed", cat, "Service worker registration found")
        else:
            self._add("critical", cat, "No service worker registration in HTML", "", "no_sw")

        if not self.sw:
            if not sw_registered:
                self._add("critical", cat, "No service worker found", "", "no_sw")
            return {"score": score, "max": 20}

        sw = self.sw

        # Install event (3)
        if re.search(r'addEventListener\s*\(\s*["\']install["\']', sw):
            has_precache = bool(re.search(r'cache\.addAll|caches\.open.*add|precacheAndRoute|__precacheManifest', sw, re.S))
            if has_precache:
                score += 3; self._add("passed", cat, "Install event with precaching")
            else:
                score += 1; self._add("warnings", cat, "Install event but no precaching detected", "", "no_install_event")
        else:
            self._add("warnings", cat, "No install event handler", "", "no_install_event")

        # Activate event (2)
        if re.search(r'addEventListener\s*\(\s*["\']activate["\']', sw):
            has_cleanup = bool(re.search(r'caches\.delete|caches\.keys', sw))
            if has_cleanup:
                score += 2; self._add("passed", cat, "Activate event with cache cleanup")
            else:
                score += 1; self._add("info", cat, "Activate event found but no old cache cleanup")
        else:
            self._add("warnings", cat, "No activate event handler", "", "no_activate_event")

        # Fetch handler (4)
        if re.search(r'addEventListener\s*\(\s*["\']fetch["\']', sw):
            score += 4; self._add("passed", cat, "Fetch event handler found")
        else:
            self._add("critical", cat, "No fetch handler — offline impossible", "", "no_fetch_handler")

        # Cache strategy (3)
        strategy = self._detect_cache_strategy(sw)
        if strategy != "unknown":
            score += 3; self._add("passed", cat, f"Cache strategy: {strategy}")
        else:
            score += 1; self._add("warnings", cat, "Cache strategy unclear — review manually")

        # Cache versioning (2)
        if re.search(r'["\'][a-zA-Z]+-v?\d+["\']|CACHE_VERSION|CACHE_NAME|cacheName', sw):
            score += 2; self._add("passed", cat, "Cache versioning detected")
        else:
            self._add("warnings", cat, "No cache versioning — stale cache risk", "", "no_cache_version")

        # ── Info-level SW capabilities ──
        has_skip = bool(re.search(r'skipWaiting\s*\(\s*\)|self\.skipWaiting', sw))
        has_claim = bool(re.search(r'clients\.claim\s*\(\s*\)', sw))
        if has_skip and has_claim:
            self._add("passed", cat, "skipWaiting + clients.claim (instant SW updates)")
        elif has_skip or has_claim:
            part = "skipWaiting" if has_skip else "clients.claim"
            self._add("info", cat, f"Only {part} found — add both for instant update flow")
        else:
            self._add("info", cat, "No skipWaiting/clients.claim — SW updates require page close/reload")

        if re.search(r'navigationPreload', sw, re.I):
            self._add("passed", cat, "Navigation preload enabled")

        # Push / Background Sync
        if re.search(r'addEventListener\s*\(\s*["\']push["\']', sw):
            self._add("passed", cat, "Push notification handler found")
            if re.search(r'addEventListener\s*\(\s*["\']notificationclick["\']', sw):
                self._add("passed", cat, "Notification click handler configured")
        if re.search(r'addEventListener\s*\(\s*["\']sync["\']', sw):
            self._add("passed", cat, "Background Sync handler detected")
        if re.search(r'addEventListener\s*\(\s*["\']periodicsync["\']', sw):
            self._add("passed", cat, "Periodic Background Sync detected")

        if re.search(r'workbox', sw, re.I):
            self._add("info", cat, "Workbox library detected")

        # Sensitive data warning
        sensitive = re.findall(r'(?:token|auth|password|secret|credential|session_id|jwt|bearer)', sw, re.I)
        if sensitive:
            unique = sorted(set(p.lower() for p in sensitive))
            self._add("warnings", cat,
                       f"Potential sensitive keywords in SW: {', '.join(unique)}",
                       "Avoid caching auth tokens or sensitive data — cached data persists and may be exposed.")

        return {"score": min(score, 20), "max": 20}

    def _detect_cache_strategy(self, sw: str) -> str:
        strategies = []
        if re.search(r'stale.while.revalidate|StaleWhileRevalidate', sw, re.I):
            strategies.append("stale-while-revalidate")
        if re.search(r'caches\.match.*\.then.*fetch|CacheFirst', sw, re.S | re.I):
            strategies.append("cache-first")
        if re.search(r'fetch.*\.catch.*caches\.match|NetworkFirst', sw, re.S | re.I):
            strategies.append("network-first")
        if re.search(r'NetworkOnly|network.only', sw, re.I):
            strategies.append("network-only")
        if re.search(r'CacheOnly|cache.only', sw, re.I):
            strategies.append("cache-only")
        if re.search(r'workbox', sw, re.I):
            strategies.append("workbox-powered")
        return " + ".join(strategies) if strategies else "unknown"

    # ── 4. Offline Capability (10 pts) ──────────────────────────────────
    def analyze_offline(self) -> dict:
        score = 0; cat = "Offline"; sw = self.sw or ""

        if re.search(r'offline\.html|offline-page|fallback.*\.html|/offline', sw, re.I):
            score += 3; self._add("passed", cat, "Offline fallback page detected")
        else:
            self._add("warnings", cat, "No offline fallback page", "", "no_offline_fallback")

        shell_exts = [r'\.html', r'\.css', r'\.js']
        cached = sum(1 for p in shell_exts if re.search(p, sw))
        if cached >= 2:
            score += 3; self._add("passed", cat, "App shell (HTML/CSS/JS) precached")
        elif cached >= 1:
            score += 1; self._add("warnings", cat, "Partial app shell caching")
        else:
            self._add("warnings", cat, "No app shell caching detected")

        if re.search(r'\.(png|jpg|jpeg|svg|webp|gif|woff|woff2|ttf|ico)', sw, re.I):
            score += 2; self._add("passed", cat, "Static assets cached")
        else:
            self._add("info", cat, "No static asset caching in SW")

        if re.search(r'navigator\.onLine|addEventListener.*["\']offline["\']|addEventListener.*["\']online["\']', self.html, re.I):
            score += 2; self._add("passed", cat, "Offline state detection in UI")
        else:
            self._add("warnings", cat, "No offline/online state indicator", "", "no_offline_indicator")

        return {"score": min(score, 10), "max": 10}

    # ── 5. Installability (10 pts) ──────────────────────────────────────
    def analyze_installability(self) -> dict:
        score = 0; cat = "Installability"

        if re.search(r'<link[^>]*rel=["\']manifest["\']', self.html, re.I):
            score += 2; self._add("passed", cat, "Manifest linked in HTML")
        else:
            self._add("critical", cat, "No <link rel='manifest'> in HTML", "", "no_manifest_link")

        if self.url.startswith("https://") or "localhost" in self.url or "127.0.0.1" in self.url:
            score += 2; self._add("passed", cat, "Served over HTTPS")
        else:
            self._add("critical", cat, "Not HTTPS — install blocked", "", "no_https")

        if self.sw and re.search(r'addEventListener\s*\(\s*["\']fetch["\']', self.sw):
            score += 2; self._add("passed", cat, "SW fetch handler (install requirement)")
        else:
            self._add("warnings", cat, "No SW fetch handler — may block install", "", "no_fetch_handler")

        if self.manifest:
            icons = self.manifest.get("icons", [])
            all_sizes = " ".join(str(i.get("sizes", "")) for i in icons)
            if "192x192" in all_sizes:
                score += 1; self._add("passed", cat, "192x192 icon present")
            else:
                self._add("critical", cat, "Missing 192x192 icon", "", "no_192_icon")
            if "512x512" in all_sizes:
                score += 1; self._add("passed", cat, "512x512 icon present")

        if re.search(r'apple-touch-icon', self.html, re.I):
            score += 1; self._add("passed", cat, "Apple touch icon (iOS support)")
        else:
            self._add("warnings", cat, "No apple-touch-icon — generic iOS icon", "", "no_apple_touch_icon")

        # CRITICAL: prefer_related_applications
        if self.manifest and self.manifest.get("prefer_related_applications") is True:
            self._add("critical", cat,
                       "prefer_related_applications=true — browser will NOT show PWA install prompt!",
                       "This directs users to native app stores instead",
                       "prefer_related")

        if re.search(r'beforeinstallprompt', self.html, re.I):
            self._add("passed", cat, "Custom install prompt (beforeinstallprompt) detected")
        else:
            self._add("info", cat, "No custom install prompt (browser default)")

        if re.search(r'apple-mobile-web-app-capable', self.html, re.I):
            self._add("passed", cat, "iOS web app capable meta tag")

        return {"score": min(score, 10), "max": 10}

    # ── 6. Security (10 pts) ────────────────────────────────────────────
    def analyze_security(self) -> dict:
        score = 0; cat = "Security"

        # HTTPS (2)
        if self.url.startswith("https://") or "localhost" in self.url:
            score += 2; self._add("passed", cat, "HTTPS enforced")
        else:
            self._add("critical", cat, "Not HTTPS — all PWA features require secure origin", "", "no_https")

        # CSP (3)
        csp_meta = re.search(
            r'<meta[^>]*http-equiv=["\']Content-Security-Policy["\'][^>]*content=["\']([^"\']+)["\']',
            self.html, re.I)
        if csp_meta:
            csp = csp_meta.group(1)
            has_default = "default-src" in csp
            has_script = "script-src" in csp
            has_unsafe_eval = "'unsafe-eval'" in csp
            if has_default and has_script and not has_unsafe_eval:
                score += 3; self._add("passed", cat, "Strong Content Security Policy")
            elif has_default or has_script:
                score += 2
                issues = []
                if "'unsafe-inline'" in csp: issues.append("unsafe-inline")
                if has_unsafe_eval: issues.append("unsafe-eval")
                self._add("warnings", cat, "CSP present but could be stricter",
                           "; ".join(issues) if issues else "")
            else:
                score += 1; self._add("warnings", cat, "CSP lacks default-src/script-src")
        else:
            self._add("warnings", cat, "No CSP meta tag detected",
                       "CSP via HTTP header is preferred and not detectable from HTML alone.",
                       "no_csp")

        # SRI (2)
        sri_count = len(re.findall(r'integrity=["\']', self.html, re.I))
        ext_scripts = len(re.findall(r'<script[^>]*src=["\']https?://', self.html, re.I))
        ext_links = len(re.findall(r'<link[^>]*href=["\']https?://[^"\']*\.(?:css|js)', self.html, re.I))
        total_ext = ext_scripts + ext_links

        if total_ext == 0:
            score += 2; self._add("passed", cat, "No external resources — SRI not needed")
        elif sri_count > 0 and sri_count / max(total_ext, 1) >= 0.5:
            score += 2; self._add("passed", cat, f"SRI: {sri_count}/{total_ext} external resources protected")
        elif sri_count > 0:
            score += 1; self._add("warnings", cat, f"SRI only {sri_count}/{total_ext} external resources", "", "no_sri")
        else:
            self._add("warnings", cat, f"{total_ext} external resources without SRI", "", "no_sri")

        # Mixed content (1)
        http_refs = re.findall(r'(?:src|href|action)=["\']http://(?!localhost)', self.html, re.I)
        if not http_refs:
            score += 1; self._add("passed", cat, "No mixed content")
        else:
            self._add("critical", cat, f"{len(http_refs)} mixed content references (http://)",
                       "Blocked by browsers, breaks SW", "mixed_content")

        # SW scope (1)
        if self.sw:
            if re.search(r'register\s*\(\s*["\'][^"\']+["\']\s*,\s*\{[^}]*scope\s*:', self.html, re.I):
                score += 1; self._add("passed", cat, "SW scope explicitly restricted")
            else:
                self._add("info", cat, "SW scope not restricted (defaults to SW location)")

        # Error handling (1)
        if self.sw:
            if re.search(r'\.catch\s*\(|try\s*\{', self.sw):
                score += 1; self._add("passed", cat, "Error handling in SW")
            else:
                self._add("warnings", cat, "No error handling in SW", "", "no_sw_error_handling")

        return {"score": min(score, 10), "max": 10}

    # ── 7. Performance Signals (10 pts) ─────────────────────────────────
    def analyze_performance(self) -> dict:
        score = 0; cat = "Performance"; html = self.html

        # Render-blocking (2)
        head_match = re.search(r'<head[^>]*>(.*?)</head>', html, re.S | re.I)
        head = head_match.group(1) if head_match else ""
        blocking = len(re.findall(
            r'<script(?![^>]*(?:async|defer|type=["\']module["\']))[^>]*src=', head, re.I))
        if blocking == 0:
            score += 2; self._add("passed", cat, "No render-blocking scripts in <head>")
        elif blocking <= 2:
            score += 1; self._add("warnings", cat, f"{blocking} render-blocking script(s)", "", "render_blocking")
        else:
            self._add("critical", cat, f"{blocking} render-blocking scripts", "", "render_blocking")

        # Images (2)
        total_imgs = len(re.findall(r'<img\s', html, re.I))
        lazy_imgs = len(re.findall(r'loading=["\']lazy["\']', html, re.I))
        has_modern = bool(re.search(r'\.(webp|avif)', html, re.I))
        img_score = 0
        if total_imgs == 0:
            img_score = 2
        else:
            if lazy_imgs / max(total_imgs, 1) >= 0.5: img_score += 1; self._add("passed", cat, f"Lazy loading: {lazy_imgs}/{total_imgs}")
            elif total_imgs > 3: self._add("warnings", cat, f"Only {lazy_imgs}/{total_imgs} lazy", "", "no_lazy_loading")
            if has_modern: img_score += 1; self._add("passed", cat, "Modern image formats (webp/avif)")
            else: self._add("info", cat, "No webp/avif detected")
        score += min(img_score, 2)

        # Async/defer (2)
        async_s = len(re.findall(r'<script[^>]*(?:async|defer|type=["\']module["\'])', html, re.I))
        total_s = len(re.findall(r'<script[^>]*src=', html, re.I))
        if total_s == 0 or async_s / max(total_s, 1) >= 0.5:
            score += 2
            if async_s > 0: self._add("passed", cat, f"{async_s}/{total_s} scripts async/defer/module")
        elif async_s > 0:
            score += 1; self._add("warnings", cat, f"Only {async_s}/{total_s} async/defer")
        else:
            self._add("warnings", cat, "No async/defer", "", "render_blocking")

        # Resource hints (2)
        preloads = len(re.findall(
            r'<link[^>]*rel=["\'](?:preload|prefetch|preconnect|dns-prefetch|modulepreload)["\']', html, re.I))
        if preloads >= 2:
            score += 2; self._add("passed", cat, f"{preloads} resource hints")
        elif preloads > 0:
            score += 1; self._add("info", cat, f"Only {preloads} resource hint(s)")
        else:
            self._add("warnings", cat, "No resource hints", "", "no_resource_hints")

        # Fonts (1)
        has_fonts = bool(re.search(r'@font-face|fonts\.googleapis|fonts\.gstatic', html, re.I))
        has_swap = bool(re.search(r'font-display\s*:\s*swap|display=swap', html, re.I))
        if has_fonts:
            if has_swap: score += 1; self._add("passed", cat, "font-display: swap")
            else: self._add("warnings", cat, "Fonts without font-display: swap", "", "no_font_swap")
        else:
            score += 1

        # Viewport (1)
        if re.search(r'<meta[^>]*name=["\']viewport["\']', html, re.I):
            score += 1; self._add("passed", cat, "Viewport meta tag present")
        else:
            self._add("critical", cat, "Missing viewport meta tag", "", "no_viewport")

        return {"score": min(score, 10), "max": 10}

    # ── 8. UX & Accessibility (10 pts) ──────────────────────────────────
    def analyze_ux(self) -> dict:
        score = 0; cat = "UX & A11y"; html = self.html

        # Responsive viewport (2)
        vp = re.search(r'<meta[^>]*name=["\']viewport["\'][^>]*content=["\']([^"\']+)["\']', html, re.I)
        if vp and "width=device-width" in vp.group(1):
            score += 2; self._add("passed", cat, "Responsive viewport configured")
        else:
            self._add("critical", cat, "No responsive viewport", "", "no_viewport")

        # Splash screen (1)
        if self.manifest:
            has_n = bool(self.manifest.get("name"))
            has_bg = bool(self.manifest.get("background_color"))
            has_ic = len(self.manifest.get("icons", [])) > 0
            if has_n and has_bg and has_ic:
                score += 1; self._add("passed", cat, "Splash screen ready")
            else:
                missing = [x for x, v in [("name", has_n), ("bg_color", has_bg), ("icons", has_ic)] if not v]
                self._add("warnings", cat, f"Splash incomplete — missing: {', '.join(missing)}")

        # Semantic HTML (2)
        semantic = ["<header", "<nav", "<main", "<footer", "<article", "<section", "<aside"]
        found = sum(1 for t in semantic if t in html.lower())
        if found >= 3: score += 2; self._add("passed", cat, f"Semantic HTML: {found} landmarks")
        elif found >= 1: score += 1; self._add("warnings", cat, f"Limited semantic HTML ({found})", "", "no_semantic_html")
        else: self._add("warnings", cat, "No semantic HTML landmarks", "", "no_semantic_html")

        # ARIA (2)
        aria = len(re.findall(r'(?:role=["\'][^"\']+["\']|aria-[a-z]+=)', html, re.I))
        if aria >= 5: score += 2; self._add("passed", cat, f"ARIA: {aria} attributes")
        elif aria >= 1: score += 1; self._add("warnings", cat, f"Limited ARIA ({aria})", "", "no_aria")
        else: self._add("warnings", cat, "No ARIA attributes", "", "no_aria")

        # Lang (1)
        if re.search(r'<html[^>]*lang=["\']', html, re.I):
            score += 1; self._add("passed", cat, "lang attribute on <html>")
        else:
            self._add("warnings", cat, "Missing lang on <html>", "", "no_lang")

        # iOS status bar (1)
        if re.search(r'apple-mobile-web-app-status-bar-style', html, re.I):
            score += 1; self._add("passed", cat, "iOS status bar styling")
        else:
            self._add("info", cat, "No iOS status bar styling")

        # Theme-color meta (1)
        if re.search(r'<meta[^>]*name=["\']theme-color["\']', html, re.I):
            score += 1; self._add("passed", cat, "Theme color meta tag")
        else:
            self._add("warnings", cat, "No <meta name='theme-color'>", "", "no_theme_meta")

        return {"score": min(score, 10), "max": 10}

    # ── 9. SEO & Discoverability (7 pts) ─────────────────────────────────
    def analyze_seo(self) -> dict:
        score = 0
        cat = "SEO & Discoverability"
        html = self.html

        # title tag (2 pts)
        title_match = re.search(r'<title>([^<]+)</title>', html, re.I)
        if title_match:
            title = title_match.group(1).strip()
            if 10 < len(title) < 70:
                score += 2
                display = title[:50] + "..." if len(title) > 50 else title
                self._add("passed", cat, f"title: '{display}' ({len(title)} chars)")
            else:
                score += 1
                self._add("warnings", cat, f"title length {len(title)} — recommend 10-70 chars")
        else:
            self._add("warnings", cat, "No <title> tag", "", "no_title")

        # meta description (2 pts)
        desc_match = re.search(
            r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', html, re.I)
        if not desc_match:
            desc_match = re.search(
                r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*name=["\']description["\']', html, re.I)
        if desc_match:
            desc = desc_match.group(1)
            if 50 < len(desc) < 160:
                score += 2
                self._add("passed", cat, f"meta description: {len(desc)} chars")
            else:
                score += 1
                self._add("warnings", cat, f"meta description {len(desc)} chars — recommend 50-160")
        else:
            self._add("warnings", cat, "No meta description", "", "no_meta_desc")

        # Open Graph tags (2 pts)
        og_tags = ["og:title", "og:description", "og:image", "og:url"]
        og_found = []
        for tag in og_tags:
            if re.search(rf'<meta[^>]*property=["\']' + tag + r'["\']', html, re.I):
                og_found.append(tag)
        if len(og_found) >= 3:
            score += 2
            self._add("passed", cat, f"Open Graph: {', '.join(og_found)}")
        elif og_found:
            score += 1
            self._add("warnings", cat, f"Partial Open Graph: {', '.join(og_found)}")
        else:
            self._add("info", cat, "No Open Graph meta tags (og:title, og:image, etc.)")

        # canonical URL (1 pt)
        if re.search(r'<link[^>]*rel=["\']canonical["\']', html, re.I):
            score += 1
            self._add("passed", cat, "Canonical URL defined")
        else:
            self._add("info", cat, "No canonical URL")

        return {"score": min(score, 7), "max": 7}

    # ── Run All ─────────────────────────────────────────────────────────
    def analyze(self) -> dict:
        categories = {
            "manifest": self.analyze_manifest(),
            "advanced_manifest": self.analyze_advanced_manifest(),
            "service_worker": self.analyze_service_worker(),
            "offline": self.analyze_offline(),
            "installability": self.analyze_installability(),
            "security": self.analyze_security(),
            "performance": self.analyze_performance(),
            "ux_accessibility": self.analyze_ux(),
            "seo": self.analyze_seo(),
        }
        total = sum(c["score"] for c in categories.values())
        mx = sum(c["max"] for c in categories.values())

        # Grade based on percentage (total max is now 108)
        pct = (total / mx * 100) if mx > 0 else 0
        if pct >= 90: grade = "A+"
        elif pct >= 80: grade = "A"
        elif pct >= 70: grade = "B"
        elif pct >= 60: grade = "C"
        elif pct >= 40: grade = "D"
        else: grade = "F"

        return {
            "url": self.url, "total_score": total, "total_max": mx,
            "grade": grade, "categories": categories, "findings": self.findings,
        }


def main():
    parser = argparse.ArgumentParser(description="Analyze PWA resources v2.1")
    parser.add_argument("--html", required=True)
    parser.add_argument("--manifest", default=None)
    parser.add_argument("--sw", default=None)
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", default="/tmp/pwa_analysis.json")
    args = parser.parse_args()

    try:
        with open(args.html, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()
    except FileNotFoundError:
        print(json.dumps({"error": f"HTML not found: {args.html}"})); sys.exit(1)

    manifest = None
    if args.manifest:
        try:
            with open(args.manifest, "r", encoding="utf-8", errors="replace") as f:
                manifest = json.loads(f.read().strip())
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: manifest parse error: {e}", file=sys.stderr)

    sw = None
    if args.sw:
        try:
            with open(args.sw, "r", encoding="utf-8", errors="replace") as f:
                sw = f.read()
        except FileNotFoundError:
            print(f"Warning: SW not found: {args.sw}", file=sys.stderr)

    analyzer = PWAAnalyzer(html, manifest, sw, args.url)
    result = analyzer.analyze()

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Analysis complete: {result['total_score']}/{result['total_max']} ({result['grade']})")
    print(f"Results saved to: {args.output}")


if __name__ == "__main__":
    main()
