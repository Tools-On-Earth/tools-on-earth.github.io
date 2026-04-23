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
- Organization name (single line)
- Description — same sentence, responsive line count:
  - Desktop (viewport > 600px): 2 lines, break after "building"
  - Mobile (viewport ≤ 600px): 3 lines, breaks after "company" and "tools"
- Email contact (`timothy@toolsonearth.org`, single line)
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
- Email `timothy@toolsonearth.org` = 24 / 60
- Copyright `© 2026 Tools On Earth LLC. All rights reserved.` = 47 / 71

**Mobile view, 3-line description, 2-line copyright:**
- Title `Tools On Earth LLC` = 18 / 19
- Description line 1 `An independent software company` = 31 / 32
- Description line 2 `building simple, edifying tools` = 31 / 32
- Description line 3 `for people of all ages.` = 23 / 32
- Email `timothy@toolsonearth.org` = 24 / 36
- Copyright line 1 `© 2026 Tools On Earth LLC.` = 26 / 43
- Copyright line 2 `All rights reserved.` = 20 / 43

## Values the design serves
Credible, engineered, quality, mature, for people of all ages. When in doubt, choose restraint over decoration — the whole aesthetic *is* the precision signal.
