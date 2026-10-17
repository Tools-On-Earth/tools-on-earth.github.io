#!/usr/bin/env python3
"""Regenerate anagrams/index.html from the live App Store listing.

Pulls title, description, version, price and icon from Apple's public
Lookup API, merges the hand-maintained subtitle and promo text from
_build/anagrams-manual.json, and fills _build/anagrams-template.html.

Fails safely: every fetch and check happens before any file is written,
so an API outage or bad response never blanks the live page.

Python standard library only. Run from anywhere:
    python3 _build/build_anagrams_page.py
"""

import datetime
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

APP_ID = "6800109189"
COUNTRY = "us"
LOOKUP_URL = f"https://itunes.apple.com/lookup?id={APP_ID}&country={COUNTRY}"

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "_build" / "anagrams-template.html"
MANUAL = ROOT / "_build" / "anagrams-manual.json"
OUT_HTML = ROOT / "anagrams" / "index.html"
OUT_ICON = ROOT / "anagrams" / "icon.jpg"


def fail(message):
    print(f"ERROR: {message} — no files were changed.", file=sys.stderr)
    sys.exit(1)


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "toolsonearth-site-sync"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def paragraphs(text, indent="            "):
    """Apple's plain text → escaped <p> blocks; single newlines become <br>."""
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]
    return "\n".join(
        f"{indent}<p>{'<br>'.join(html.escape(line.strip()) for line in b.splitlines())}</p>"
        for b in blocks
    )


def main():
    try:
        data = json.loads(fetch(LOOKUP_URL))
    except Exception as e:
        fail(f"Lookup API request failed ({e})")
    if data.get("resultCount", 0) < 1:
        fail(f"Lookup API returned no results for app {APP_ID}")
    app = data["results"][0]

    required = ["trackName", "description", "version", "formattedPrice", "artworkUrl512"]
    missing = [k for k in required if not str(app.get(k, "")).strip()]
    if missing:
        fail(f"Lookup API response is missing {', '.join(missing)}")

    try:
        icon = fetch(app["artworkUrl512"])
    except Exception as e:
        fail(f"icon download failed ({e})")
    if len(icon) < 1000:
        fail("icon download looks empty")

    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    subtitle = manual.get("subtitle", "").strip()
    promo = manual.get("promoText", "").strip()

    title = app["trackName"].strip()
    first_sentence = app["description"].strip().split(". ")[0].rstrip(".") + "."
    values = {
        "title": html.escape(title),
        "meta_description": html.escape(subtitle or first_sentence),
        "subtitle_block": f'        <p class="subtitle">{html.escape(subtitle)}</p>\n' if subtitle else "",
        "promo_block": f'            <p class="promo">{html.escape(promo)}</p>\n' if promo else "",
        "price": html.escape(app["formattedPrice"].strip()),
        "version": html.escape(app["version"].strip()),
        "description_html": paragraphs(app["description"]),
        "year": str(datetime.date.today().year),
    }

    page = TEMPLATE.read_text(encoding="utf-8")
    for key, value in values.items():
        page = page.replace("{{" + key + "}}", value)
    leftover = re.findall(r"\{\{\w+\}\}", page)
    if leftover:
        fail(f"template has unfilled placeholders: {', '.join(sorted(set(leftover)))}")

    changed = []
    if not OUT_HTML.exists() or OUT_HTML.read_text(encoding="utf-8") != page:
        OUT_HTML.write_text(page, encoding="utf-8")
        changed.append(OUT_HTML.relative_to(ROOT))
    if not OUT_ICON.exists() or OUT_ICON.read_bytes() != icon:
        OUT_ICON.write_bytes(icon)
        changed.append(OUT_ICON.relative_to(ROOT))

    print(f"{title} · version {app['version']} · {app['formattedPrice']}")
    print("Updated: " + ", ".join(map(str, changed)) if changed else "No changes.")


if __name__ == "__main__":
    main()
