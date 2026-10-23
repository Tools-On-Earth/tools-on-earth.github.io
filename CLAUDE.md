# Tools On Earth LLC — Landing Site

Single-page landing site for Tools On Earth LLC, plus unlinked App Store compliance subpages.

## Site structure
- `index.html` — landing page. All constraints below apply to it.
- `anagrams/index.html` → `https://toolsonearth.org/anagrams/` — Anagrams marketing page. **GENERATED — never edit by hand** (see "Anagrams marketing page" below).
- `anagrams/privacy/index.html` → `https://toolsonearth.org/anagrams/privacy/` — Privacy Policy for the Anagrams iOS app (App Store requirement).
- `anagrams/support/index.html` → `https://toolsonearth.org/anagrams/support/` — Support/FAQ page for Anagrams (App Store requirement).
- `anagrams/family-friendly/index.html` → `https://toolsonearth.org/anagrams/family-friendly/` — age-suitability page: explains the curated (censored) word and definition lists and invites removal suggestions by email.
- `anagrams/get/…/index.html` — channel-tracked App Store redirect pages (see below).
- `temp/` — local working assets, **git-ignored** via `.gitignore`, never published. Holds `temp/qr/` (print QR code for `https://toolsonearth.org/anagrams/get/print/`: SVG + ~2000px PNG, error correction Q, with a README of print tips). The QR never needs regenerating — its destination is controlled by the redirect page.

### App Store redirect pages (`anagrams/get/…`)
Static meta-refresh pages that forward to Apple **campaign links**, so App Store Connect's App Analytics (Acquisition → Campaigns) reports page views/downloads per distribution channel. One page per channel; each differs only in its `ct` campaign token:

| Channel | URL | `ct` token |
|---|---|---|
| Word of mouth (short, speakable) | `/anagrams/get/` | `grapevine` |
| QR code / print | `/anagrams/get/print/` | `print` |
| Email / direct message | `/anagrams/get/email/` | `email` |
| Website visitors | `/anagrams/get/site/` | `site` |

They carry `<meta name="robots" content="noindex">`, use the design system for the visible fallback (four rows, each its own `<p>`: **Anagrams** (`.title`, weight 600) / Redirecting to the App Store… (`.status`, followed by one blank line via `margin-bottom: 1.7em`) / If nothing happens, / [tap or click here]. — always "the App Store", never "Apple App Store", per Apple's marketing guidelines), and are exempt from the landing-page layout constraints. **Live since launch (2026-10):** all four pages target `https://apps.apple.com/app/apple-store/id6800109189?pt=2423924&ct=<token>&mt=8` — App ID `6800109189` and provider token `2423924` are shared; only `ct` differs. Each URL appears twice per page (meta refresh and fallback `<a>`), with `&` escaped as `&amp;`. To add a channel: copy a page folder, change `ct` in both places and the channel comment, and add a row to the table above. App Store Connect doesn't save generated links; a campaign appears under Analytics → Acquisition → Campaigns only after ≥24h and ~5 first-time downloads. Never rename or delete a distributed URL.

### Anagrams marketing page (`anagrams/`) — auto-synced from the App Store
Mirrors the App Store listing: icon, title, subtitle, price · version, official "Download on the App Store" badge, then (40px gap, no hairline) promo text, one blank line, the description, (40px gap, no hairline) a QR code + printed link, then a hairline and the footer — badge, QR and link all go to the `site` campaign (`/anagrams/get/site/`).

- **Build:** `python3 _build/build_anagrams_page.py` (stdlib only) fetches Apple's public Lookup API (`itunes.apple.com/lookup?id=6800109189&country=us`) for title, description, version, price and icon; merges `_build/anagrams-manual.json`; fills `_build/anagrams-template.html`; writes `anagrams/index.html` and `anagrams/icon.jpg` only if changed. Fails safely: any API/validation error exits non-zero before writing anything. The request carries a unique `&cb=<timestamp>` because Apple's CDN (Akamai) caches each exact lookup URL for ~24h — without it the page lagged a day behind a new release (found with v1.0.2, 2026-10-23).
- **Subtitle and promo text are NOT in the public API** (only the authenticated App Store Connect API has them) — they're hand-maintained in `_build/anagrams-manual.json`; an empty value hides that line. Decided (2026-10) not to use the App Store Connect API: it would add a credential to protect and a third-party JWT-signing dependency to save a few manual edits a year. Revisit only if promo text starts changing frequently or more apps are added.
- **Layout changes** go in `_build/anagrams-template.html`, then re-run the build. `_build/` is excluded from publishing because Jekyll skips `_`-prefixed folders.
- **Automation:** `.github/workflows/sync-anagrams-listing.yml` runs daily at 10:00 UTC, on the manual "Run workflow" button, and on pushes touching `_build/**`. Commits as `github-actions[bot]` only when something changed, then requests a Pages build. No secrets.
- **Because the bot commits to `main`, always `git pull` before starting local work.**
- Static assets: `anagrams/app-store-badge.svg` (Apple's official black badge, from Apple Marketing Tools — don't modify), `anagrams/qr-site.svg` (encodes `https://toolsonearth.org/anagrams/get/site/`; never needs regenerating).
- Visitors' browsers load nothing from Apple — the icon is downloaded at build time.
- **Generated head metadata:** meta description (promo text → subtitle → first sentence of description, first available), canonical URL, Open Graph/Twitter link-preview tags (icon as image), and `MobileApplication` JSON-LD (version, price, minimum iOS from the API). The JSON-LD `<script type="application/ld+json">` is an inert data block, not executable JavaScript, so it doesn't violate the no-JS rule.

### Search discovery
- Canonical host is **`https://www.toolsonearth.org`** (the bare domain 301-redirects to `www`); use it in canonical tags, the sitemap and structured data.
- `robots.txt` allows everything and points to `sitemap.xml`. `sitemap.xml` lists the five public pages (`/`, `/anagrams/`, support, privacy, family-friendly); add new public pages there. The `anagrams/get/…` redirect pages are deliberately excluded and carry `noindex` — don't block them in robots.txt, or crawlers can't see the `noindex`.
- Every public page has a `<meta name="description">` and `<link rel="canonical">`. Don't add `<meta name="keywords">` — Google ignores it and Bing treats it as a spam signal. App Store keywords only affect App Store search.
- Google Search Console (domain property `toolsonearth.org`, DNS-verified) is where the sitemap is submitted and indexing is monitored. App Store Connect's **Marketing URL** should point at `https://www.toolsonearth.org/anagrams/`.

The Anagrams subpages are intentionally NOT linked from the landing page — they exist only as public URLs for App Store Connect. They reuse the design system (colors, IBM Plex Mono, hairlines, base font size) but are scrollable, left-aligned articles in a `min(92vw, 640px)` column; the one-viewport, centered-grid, and wrap-budget constraints below apply to the landing page only. Contact email on the landing page and all Anagrams subpages is support@toolsonearth.org.

## Tech constraints
- Static HTML + CSS only. No JavaScript. No build tools. (Exceptions: inert JSON-LD data blocks are allowed; the Anagrams marketing page is generated by `_build/`, see above.)
- Single self-contained `index.html` with embedded `<style>`.
- Only external dependency is IBM Plex Mono from Google Fonts (via CSS `@import`).

## Layout constraint
- Must fit in one viewport with no scrolling on standard desktop and mobile sizes.
- Content centered horizontally and vertically using `display: grid; place-items: center; min-height: 100dvh`.
- Use `100dvh` (not `100vh`) so mobile browser chrome does not cause a scrollbar.

## Content inventory (exhaustive — do not add without being asked)
- Organization name (single line)
- Description — same sentence, responsive line count:
  - Desktop (viewport > 600px): 2 lines, break after "building"
  - Mobile (viewport ≤ 600px): 3 lines, breaks after "company" and "tools"
- Email contact (`support@toolsonearth.org`, single line)
- Copyright — responsive:
  - Desktop: 1 line (`© YEAR Tools On Earth LLC. All rights reserved.`)
  - Mobile: 2 lines (`© YEAR Tools On Earth LLC.` / `All rights reserved.`)

Sections, navigation, CTAs, images, social links, and section headings are out of scope.

## Design system
- Background: `#13141a` (warm near-black)
- Primary text: `#e8e6e1` (warm off-white)
- Secondary text: `#8a8a82` (muted warm gray — copyright only)
- Hairline divider: `#2a2b33` (40px wide, 1px tall, centered between name and description)
- Typography: IBM Plex Mono, weights 400 and 600 only. All content uses this family; hierarchy comes from size and weight, not multiple families.
- Base font size: `clamp(16px, 1rem + 0.3vw, 18px)` for fluid scaling.
- Vertical rhythm: name → 28px → hairline → 28px → description → 28px → hairline → 28px → email → 32px → copyright. Twin hairlines frame the description, creating a three-part composition (name / description / contact).

## Wrap rule (hard constraint)
Responsive layout switches at **600px** via `@media (max-width: 600px)`. Default markup holds both views; classed `<br>` elements (`.br-desktop` and `.br-mobile`) are toggled by CSS — no duplicated content.

### Default (desktop) view — viewport > 600px
Container `min(92vw, 560px)`. At the breakpoint edge (V=601), 92vw = 553px.

| Element | Font-size | Max chars per line at 553px |
|---|---|---|
| Title (`h1`) | 1.75rem (~28px) | ~32 |
| Description | 1rem (~18px) | ~51 |
| Email | 0.95rem (~15.2px) | ~60 |
| Copyright | 0.8rem (~12.8px) | ~71 |

### Mobile view — viewport ≤ 600px
Smallest supported viewport: 360px (Galaxy S class). 92vw = ~331px.

| Element | Font-size | Max chars per line at 331px |
|---|---|---|
| Title (`h1`) | 1.75rem (~28px) | **19** |
| Description | 1rem (~17px) | **32** |
| Email | 0.95rem (~15.2px) | **36** |
| Copyright | 0.8rem (~12.8px) | **43** |

### Rule
Before changing any copy, count characters for **both** views against the budget above. If a line exceeds its budget, shorten the content or add a `<br>` at the appropriate position using the `.br-desktop` / `.br-mobile` classes.

### Current content conformance

**Default (desktop) view, 2-line description, 1-line copyright:**
- Title `Tools On Earth LLC` = 18 / 32
- Description line 1 `An independent software company building` = 40 / 51
- Description line 2 `simple, edifying tools for people of all ages.` = 47 / 51
- Email `support@toolsonearth.org` = 24 / 60
- Copyright `© 2026 Tools On Earth LLC. All rights reserved.` = 47 / 71

**Mobile view, 3-line description, 2-line copyright:**
- Title `Tools On Earth LLC` = 18 / 19
- Description line 1 `An independent software company` = 31 / 32
- Description line 2 `building simple, edifying tools` = 31 / 32
- Description line 3 `for people of all ages.` = 23 / 32
- Email `support@toolsonearth.org` = 24 / 36
- Copyright line 1 `© 2026 Tools On Earth LLC.` = 26 / 43
- Copyright line 2 `All rights reserved.` = 20 / 43

## Values the design serves
Credible, engineered, quality, mature, for people of all ages. When in doubt, choose restraint over decoration — the whole aesthetic *is* the precision signal.
