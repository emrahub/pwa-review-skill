#!/usr/bin/env python3
"""Discover PWA manifest and service worker URLs from HTML content."""

import argparse
import json
import re
import sys
from urllib.parse import urljoin


def discover_manifest(html: str, base_url: str) -> str | None:
    """Find manifest.json link in HTML."""
    patterns = [
        r'<link[^>]*rel=["\']manifest["\'][^>]*href=["\']([^"\']+)["\']',
        r'<link[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']manifest["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            return urljoin(base_url, match.group(1))
    return None


def discover_service_worker(html: str, base_url: str) -> str | None:
    """Find service worker registration in HTML/inline JS."""
    patterns = [
        r'navigator\.serviceWorker\.register\s*\(\s*["\']([^"\']+)["\']',
        r'serviceWorker\.register\s*\(\s*["\']([^"\']+)["\']',
        r'navigator\[.serviceWorker.\]\.register\s*\(\s*["\']([^"\']+)["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            return urljoin(base_url, match.group(1))
    return None


def discover_additional_meta(html: str) -> dict:
    """Extract PWA-relevant meta tags and link elements."""
    meta = {}
    checks = [
        ("theme_color", r'<meta[^>]*name=["\']theme-color["\'][^>]*content=["\']([^"\']+)["\']'),
        ("apple_touch_icon", r'<link[^>]*rel=["\']apple-touch-icon["\'][^>]*href=["\']([^"\']+)["\']'),
        ("apple_web_app_capable", r'<meta[^>]*name=["\']apple-mobile-web-app-capable["\'][^>]*content=["\']([^"\']+)["\']'),
        ("apple_status_bar_style", r'<meta[^>]*name=["\']apple-mobile-web-app-status-bar-style["\'][^>]*content=["\']([^"\']+)["\']'),
        ("viewport", r'<meta[^>]*name=["\']viewport["\'][^>]*content=["\']([^"\']+)["\']'),
        ("lang", r'<html[^>]*lang=["\']([^"\']+)["\']'),
        ("csp", r'<meta[^>]*http-equiv=["\']Content-Security-Policy["\'][^>]*content=["\']([^"\']+)["\']'),
    ]
    for key, pattern in checks:
        m = re.search(pattern, html, re.I)
        if m:
            meta[key] = m.group(1)
    return meta


def main():
    parser = argparse.ArgumentParser(description="Discover PWA resources from HTML")
    parser.add_argument("--html", required=True, help="Path to saved HTML file")
    parser.add_argument("--base-url", required=True, help="Base URL for resolving relative paths")
    args = parser.parse_args()

    try:
        with open(args.html, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()
    except FileNotFoundError:
        print(json.dumps({"error": f"HTML file not found: {args.html}"}))
        sys.exit(1)

    manifest_url = discover_manifest(html, args.base_url)
    sw_url = discover_service_worker(html, args.base_url)

    result = {
        "manifest_url": manifest_url,
        "sw_url": sw_url,
        "meta": discover_additional_meta(html),
        "manifest_found": manifest_url is not None,
        "sw_found": sw_url is not None,
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
