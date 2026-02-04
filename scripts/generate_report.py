#!/usr/bin/env python3
"""Generate PWA review report from analysis results. v2.2"""

import argparse
import json
import sys
from datetime import datetime, timezone


CATEGORY_LABELS = {
    "manifest": "📋 Manifest Compliance",
    "advanced_manifest": "🧩 Advanced Manifest",
    "service_worker": "⚙️ Service Worker & Caching",
    "offline": "📡 Offline Capability",
    "installability": "📲 Installability",
    "security": "🔒 Security",
    "performance": "⚡ Performance Signals",
    "ux_accessibility": "🎨 UX & Accessibility",
    "seo": "🔍 SEO & Discoverability",
}

GRADE_EMOJI = {"A+": "🏆", "A": "🥇", "B": "🥈", "C": "🥉", "D": "⚠️", "F": "🚫"}

GRADE_LABEL = {
    "A+": "Excellent PWA",
    "A": "Strong PWA",
    "B": "Good PWA — Room for Improvement",
    "C": "Functional — Needs Significant Work",
    "D": "Major PWA Gaps",
    "F": "Not a Functional PWA",
}

REF_LINKS = {
    "Manifest": "https://web.dev/add-manifest/",
    "Advanced Manifest": "https://developer.mozilla.org/en-US/docs/Web/Manifest",
    "Service Worker": "https://web.dev/learn/pwa/service-workers/",
    "Offline": "https://web.dev/learn/pwa/offline-data/",
    "Installability": "https://web.dev/learn/pwa/installation/",
    "Security": "https://web.dev/articles/csp",
    "Performance": "https://web.dev/learn/performance/",
    "UX & A11y": "https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Best_practices",
    "SEO & Discoverability": "https://web.dev/articles/discoverable",
}


def bar(score: int, mx: int, w: int = 20) -> str:
    pct = score / mx if mx > 0 else 0
    filled = round(pct * w)
    return f"[{'█' * filled}{'░' * (w - filled)}] {score}/{mx}"


def generate_report(data: dict) -> str:
    url = data["url"]
    total = data["total_score"]
    mx = data["total_max"]
    grade = data["grade"]
    cats = data["categories"]
    findings = data["findings"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    L = []
    w = L.append

    w(f"# PWA Review Report")
    w(f"")
    w(f"**URL:** {url}")
    w(f"**Date:** {now}")
    w(f"**Overall Score:** {total}/{mx} — Grade: {GRADE_EMOJI.get(grade, '')} **{grade}** ({GRADE_LABEL.get(grade, '')})")
    w(f"")

    # Score overview
    w(f"## Score Overview")
    w(f"")
    w(f"```")
    w(f"Overall: {bar(total, mx, 30)}")
    w(f"```")
    w(f"")
    w(f"| Category | Score | Bar |")
    w(f"|----------|-------|-----|")
    for key, label in CATEGORY_LABELS.items():
        if key in cats:
            c = cats[key]
            pct = round(c["score"] / c["max"] * 100) if c["max"] > 0 else 0
            w(f"| {label} | {c['score']}/{c['max']} ({pct}%) | `{bar(c['score'], c['max'], 10)}` |")
    w(f"")

    # Findings sections
    sections = [
        ("critical", "🚨 Critical Findings", "These issues **block** PWA functionality or installability:"),
        ("warnings", "⚠️ Warnings", "These items need improvement:"),
        ("passed", "✅ Passed Checks", None),
        ("info", "ℹ️ Notes", None),
    ]
    for level, title, subtitle in sections:
        items = findings.get(level, [])
        if not items:
            continue
        w(f"## {title}")
        w(f"")
        if subtitle:
            w(subtitle)
            w(f"")
        for it in items:
            w(f"- **[{it['category']}]** {it['message']}")
            if it.get("detail"):
                w(f"  - {it['detail']}")
        w(f"")

    # Recommendations with How-to-Fix
    critical = findings.get("critical", [])
    warnings = findings.get("warnings", [])

    if critical or warnings:
        w(f"## 📌 Prioritized Recommendations")
        w(f"")

        if critical:
            w(f"### 🔴 High Priority (Blockers)")
            w(f"")
            for i, it in enumerate(critical, 1):
                w(f"{i}. **{it['message']}** ({it['category']})")
                if it.get("detail"):
                    w(f"   - {it['detail']}")
                if it.get("fix"):
                    w(f"   - 💡 **How to fix:** {it['fix']}")
            w(f"")

        if warnings:
            w(f"### 🟡 Medium Priority (Improvements)")
            w(f"")
            for i, it in enumerate(warnings, 1):
                w(f"{i}. **{it['message']}** ({it['category']})")
                if it.get("fix"):
                    w(f"   - 💡 **How to fix:** {it['fix']}")
            w(f"")

        # Quick Wins section
        quick_wins = [it for it in (critical + warnings) if it.get("fix") and len(it["fix"]) < 120]
        if quick_wins:
            w(f"### ⚡ Quick Wins")
            w(f"")
            w(f"These fixes take less than 5 minutes each:")
            w(f"")
            for i, it in enumerate(quick_wins[:5], 1):
                w(f"{i}. {it['message']} → {it['fix']}")
            w(f"")

    # Reference links
    unique_cats = set()
    for level in ["critical", "warnings"]:
        for it in findings.get(level, []):
            unique_cats.add(it["category"])

    if unique_cats:
        w(f"## 📚 Reference Links")
        w(f"")
        for cat in sorted(unique_cats):
            if cat in REF_LINKS:
                w(f"- **{cat}**: {REF_LINKS[cat]}")
        w(f"- **PWA Checklist**: https://web.dev/articles/pwa-checklist")
        w(f"- **Lighthouse**: https://developer.chrome.com/docs/lighthouse")
        w(f"")

    w(f"---")
    w(f"*Generated by PWA Review Skill v2.2*")

    return "\n".join(L)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    try:
        with open(args.analysis, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    report = generate_report(data)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Report generated: {args.output}")
    print(f"Score: {data['total_score']}/{data['total_max']} ({data['grade']})")


if __name__ == "__main__":
    main()
