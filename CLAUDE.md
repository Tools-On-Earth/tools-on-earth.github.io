# Tools On Earth LLC — Landing Site

Single-page landing site for Tools On Earth LLC.

## Tech constraints
- Static HTML + CSS only. No JavaScript. No build tools.
- Single self-contained `index.html` with embedded `<style>`.
- Only external dependency is IBM Plex Mono from Google Fonts (via CSS `@import`).

## Layout constraint
- Must fit in one viewport with no scrolling on standard desktop and mobile sizes.
- Content centered horizontally and vertically using `display: grid; place-items: center; min-height: 100dvh`.
- Use `100dvh` (not `100vh`) so mobile browser chrome does not cause a scrollbar.

## Content inventory (exhaustive — do not add without being asked)
- Organization name
- One-line description
- Email contact (`timothy@toolsonearth.org`)
- Copyright line (year 2026)

Sections, navigation, CTAs, images, social links, and section headings are out of scope.

## Design system
- Background: `#13141a` (warm near-black)
- Primary text: `#e8e6e1` (warm off-white)
- Secondary text: `#8a8a82` (muted warm gray — copyright only)
- Hairline divider: `#2a2b33` (40px wide, 1px tall, centered between name and description)
- Typography: IBM Plex Mono, weights 400 and 600 only. All content uses this family; hierarchy comes from size and weight, not multiple families.
- Base font size: `clamp(16px, 1rem + 0.3vw, 18px)` for fluid scaling.
- Vertical rhythm: name → 28px → hairline → 28px → description → 40px → email → 32px → copyright.

## Values the design serves
Credible, engineered, quality, mature, for people of all ages. When in doubt, choose restraint over decoration — the whole aesthetic *is* the precision signal.
