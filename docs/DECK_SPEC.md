# DECK_SPEC.md — Interactive HTML Dashboard Spec (Track 2)

> **Owner:** eng-2 · **Consumes:** `financial_plan.json` (contract: `schemas/financial_plan.schema.json`) · **Fixture available now:** `synthetic-data/sample-plan.json`
>
> Build a **single static HTML file** (`dashboard.html`) that reads one `plan.json` and renders the whole advisory report. **Chart.js + Tailwind via CDN only** — no build step, no bundler, no framework. Open it with a tiny static server (or `file://`) and it just works. This is the **wow layer** of the demo: the board reshapes per client and the compliance banner turns red on a STOP.

---

## 1. Technical approach (single-file, zero-build)

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AI Wealth Advisory — Personalized Plan</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
</head>
<body class="bg-slate-50 text-slate-800">
  <!-- sections render here -->
  <script>
    // 1. Load the plan. Default to the fixture; allow ?plan=<file> + preset switcher.
    const params = new URLSearchParams(location.search);
    const planFile = params.get('plan') || 'sample-plan.json';
    fetch(planFile).then(r => r.json()).then(renderPlan).catch(showLoadError);
    function renderPlan(plan) { /* bind every section below */ }
  </script>
</body>
</html>
```

**Rules of the road**
- **One fetch, one object.** Everything binds off the single `plan` object that matches `financial_plan.schema.json`. Never hard-code a client's numbers into the HTML.
- **CDN pins:** Tailwind Play CDN (`cdn.tailwindcss.com`) and `chart.js@4` (jsdelivr). Pin Chart.js to major v4 so the API (`new Chart(ctx, {type, data, options})`) is stable.
- **`fetch` needs http(s) for some browsers.** Ship a one-liner in the README: `python3 -m http.server` from the repo root, then open `http://localhost:8000/<path>/dashboard.html?plan=../../synthetic-data/sample-plan.json`. (Keep `dashboard.html` + the json reachable by relative path.)
- **Money formatter:** one helper `fmt$(n)` → `Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0})`. Used by projection axis ticks, tooltips, allocation values, goal target amounts.
- **Percent values are already 0–100** in the schema (`allocation[].percent`, `goals[].fundedPercent`, `riskProfile.*Score`, `financialWellbeing.score`) — do **not** multiply by 100.
- **Empty-array tolerance:** `marketContext.sources` / `tacticalTilts`, `goals`, `recommendations` may be short or (for tilts/sources) absent. Guard with `(plan.x || [])`. The board **shrinks** for preset #2, so do not assume the full roster is present.
- **Color tokens** (use consistently across charts + banner):
  - on-track / APPROVED / good: `#16a34a` (green-600)
  - caution / REVISE / medium: `#d97706` (amber-600)
  - off-track / STOP / high: `#dc2626` (red-600)
  - target series / accent: `#2563eb` (blue-600); current series: `#64748b` (slate-500)
  - cone fill (mid): `#3b82f6` at low opacity; low/high band: `#93c5fd`

---

## 2. Page sections — in render order

| # | Section | Source fields | Render |
| - | --- | --- | --- |
| 0 | **Compliance banner** (pinned to top — it is the punchline) | `compliance.verdict`, `compliance.notes`, `compliance.reviewer` | full-width colored bar; see §3.8 |
| 1 | **Header / household identity** | `generatedFor`, `asOf`, `advisor`, `ticketType` | `H1 = generatedFor`; subline = `"{ticketType} · prepared by {advisor} · as of {asOf}"` |
| 2 | **Routed specialists (the board)** | `routedSpecialists[]` | a row of pill chips, one per specialist — **this visibly grows/shrinks per client**. Chip label = specialist name. Caption: `"{n} specialists engaged for this client"` |
| 3 | **Executive summary** | `executiveSummary[]` | bulleted card (3–6 items) |
| 4 | **Wellbeing score gauge** | `financialWellbeing.score`, `.band`, `.drivers[]` | gauge (§3.1) + driver list (color +/− by leading character) |
| 5 | **Risk profile** | `riskProfile.capacityScore`, `.toleranceScore`, `.band`, `.rationale` | capacity-vs-tolerance bars + band label + rationale (§3.2) |
| 6 | **Allocation: current vs target** | `allocation.current[]`, `allocation.target[]`, `allocation.keyChanges[]` | two donuts side-by-side (§3.3) + keyChanges list |
| 7 | **Goal funding** | `goals[]` (`name`, `fundedPercent`, `onTrack`, `targetYear`, `targetAmount`, `gap`, `recommendation`) | horizontal bars (§3.4) + per-goal detail |
| 8 | **Projection cone** | `projections.series[]` (`year`,`age`,`low`,`mid`,`high`), `projections.assumptions` | line chart with band (§3.5) + assumptions footnote |
| 9 | **Market context** | `marketContext.summary`, `.asOf`, `.sources[]`, `.tacticalTilts[]` | prose card + tilt bullets + linked sources (§3.6) |
| 10 | **Recommendations** | `recommendations[]` (`title`,`detail`,`priority`,`owner`,`id`) | priority-colored list (§3.7) |
| 11 | **Disclaimers footer** | `disclaimers` | muted small print, always visible |

Layout: section 0 sticky/top, section 1–2 a header block, then a responsive 2-column grid (`md:grid-cols-2`) for the cards; charts that need width (projection cone, goal bars) span both columns (`md:col-span-2`).

---

## 3. Charts — exact field bindings + Chart.js type

Each chart gets its own `<canvas id="...">` and a `new Chart(...)` call. All bindings below are **literal `financial_plan.json` paths**.

### 3.1 Wellbeing score gauge
- **Chart.js type:** `doughnut` with `circumference: 180, rotation: 270` (half-donut gauge), `cutout: '75%'`.
- **Binds:** `financialWellbeing.score` (0–100).
- **Data:** `data: [score, 100 - score]`. Arc 1 = score (colored), arc 2 = remainder (`#e2e8f0` track).
- **Arc color by score band:** `>=70` green `#16a34a`; `40–69` amber `#d97706`; `<40` red `#dc2626`.
- **Center label (plugin or absolutely-positioned div):** big number = `score`, under it `financialWellbeing.band` (e.g. "On Track — with funding gaps").
- **Below the gauge:** render `financialWellbeing.drivers[]` as a list. If a driver string starts with `+` color it green, if `−`/`-` color it red (the fixture uses `+`/`−` prefixes).
- **options:** `plugins.tooltip.enabled = false`, `plugins.legend.display = false` (the gauge reads from the center label).

### 3.2 Risk profile — capacity vs tolerance (+ band)
- **Chart.js type:** `bar` with `indexAxis: 'y'` (horizontal), `scales.x: { min: 0, max: 100 }`.
- **Binds:** `riskProfile.capacityScore`, `riskProfile.toleranceScore`.
- **Data:** two bars — labels `['Capacity (ability)', 'Tolerance (willingness)']`, `data: [capacityScore, toleranceScore]`. Capacity bar `#2563eb`, tolerance bar `#64748b`.
- **Band callout (HTML, not chart):** a pill showing `riskProfile.band` (one of Conservative / Moderate / Moderate Growth / Growth / Aggressive) colored on a conservative→aggressive ramp (Conservative green → Aggressive red). Caption note: "We anchor to the **lower** of the two scores."
- **Rationale:** `riskProfile.rationale` as prose under the chart.
- **STOP tie-in:** when `tolerance < capacity` by a wide margin AND the recommended band reads aggressive, this section is the visual evidence for the compliance STOP — keep both bars on one axis so the mismatch is obvious.

### 3.3 Allocation — CURRENT vs TARGET
- **Chart.js type:** two `doughnut` charts side by side (one CURRENT, one TARGET). (Acceptable alternative for accessibility: a single grouped `bar` with current/target per asset class — but donuts are the spec default for the demo.)
- **Binds:**
  - CURRENT donut: `labels = allocation.current[].assetClass`, `data = allocation.current[].percent`.
  - TARGET donut: `labels = allocation.target[].assetClass`, `data = allocation.target[].percent`.
- **Shared color map:** build one `assetClass → color` map so the SAME asset class is the SAME color in both donuts (this is what makes the "before/after" read instantly). Suggested palette: US Equity `#2563eb`, Employer Stock (concentrated) `#dc2626` (red on purpose — it is the risk), International Equity `#0ea5e9`, Bonds `#16a34a`, Cash `#eab308`, Alternatives / Other `#8b5cf6`. Fall back to a deterministic palette for unknown classes.
- **Tooltip:** `label + ': ' + percent + '%'`; for CURRENT also append `fmt$(value)` from `allocation.current[].value`.
- **Below the pair:** render `allocation.keyChanges[]` as a bulleted "what's changing" list.
- **Sanity (dev only):** assert each donut's percents sum to ~100 (console.warn if off by >1) — matches the eval check.

### 3.4 Goal-funding horizontal bars
- **Chart.js type:** `bar` with `indexAxis: 'y'`, `scales.x: { min: 0, max: 100, ticks: { callback: v => v + '%' } }`.
- **Binds:** `labels = goals[].name`, `data = goals[].fundedPercent`.
- **Per-bar color by `goals[].onTrack`:** `true` → green `#16a34a`; `false` → red `#dc2626`. (Use a `backgroundColor` array computed from `goals.map(g => g.onTrack ? green : red)`.)
- **Tooltip:** `name + ': ' + fundedPercent + '% funded · target ' + fmt$(targetAmount) + ' by ' + targetYear`.
- **Per-goal detail cards** beneath the chart: for each goal show `name`, `targetYear`, `fmt$(targetAmount)`, an on/off-track badge (same green/red), and `gap` + `recommendation` text. (`gap` and `recommendation` are optional in the schema — guard.)

### 3.5 Projection cone — low / mid / high
- **Chart.js type:** `line` (3 datasets sharing one X axis).
- **Binds:** X = `projections.series[].year` (label can append age: `"${year} (age ${age})"`). Three datasets:
  - **high:** `data = series[].high`, `borderColor #93c5fd`, `fill: '+1'` (fill down to the next dataset = mid) OR fill to `low` for a single band.
  - **mid:** `data = series[].mid`, `borderColor #2563eb`, `borderWidth: 3`, `fill: false` — the headline line.
  - **low:** `data = series[].low`, `borderColor #93c5fd`, `fill: false`.
  - To shade the cone: set high dataset `fill: '+2'` (down to low) with `backgroundColor 'rgba(59,130,246,0.12)'`, or render high with `fill:'+1'`→mid and low as the lower bound. Either reads as a cone.
- **Axes:** Y `ticks.callback = fmt$`; `pointRadius: 0` for a clean cone; tooltip shows all three (low/mid/high) for the hovered year.
- **Footnote:** `projections.assumptions` rendered verbatim under the chart (it states return %, inflation, contributions, spend, and that bands are 10th/50th/90th percentile).
- **Ordering guard (dev):** assert `low <= mid <= high` per point (matches the eval's cone-ordered check).

### 3.6 Market context
- **Not a chart** — a prose card.
- **Binds:** `marketContext.summary` (paragraph), `marketContext.asOf` (small "as of" tag), `marketContext.tacticalTilts[]` (bulleted), `marketContext.sources[]` (rendered as clickable `<a>` links — these come from the Market Strategist's live `web_search`). Guard: tilts/sources may be empty; if `marketContext` is absent entirely (board shrank and Market Strategist wasn't routed), hide the whole section.

### 3.7 Recommendations list
- **Not a chart** — a styled list.
- **Binds:** `recommendations[]` → each row shows `title` (bold), `detail`, an `owner` chip, and a **priority dot/badge colored by `priority`:** `high` → red `#dc2626`, `medium` → amber `#d97706`, `low` → green `#16a34a`. Sort `high → medium → low` for visual scan order. Use `id` as a stable `key`/anchor.

### 3.8 Compliance banner (verdict-driven)
- **Not a chart** — a full-width bar at the very top (section 0), sticky.
- **Binds:** `compliance.verdict` drives color + headline; `compliance.notes[]` listed under it; `compliance.reviewer` shown as the signer.
- **Verdict → style map (exact):**

| `compliance.verdict` | Banner bg | Headline text |
| --- | --- | --- |
| `APPROVED` | green `#16a34a` (light: `bg-green-100 text-green-800 border-green-600`) | "COMPLIANCE: APPROVED — plan is suitable and may be presented to the client." |
| `REVISE` | amber `#d97706` (light: `bg-amber-100 text-amber-800 border-amber-600`) | "COMPLIANCE: REVISE — changes required before this plan can be presented." |
| `STOP` | red `#dc2626` (light: `bg-red-100 text-red-800 border-red-700`) | "COMPLIANCE: STOP — recommendation is unsuitable and will NOT be presented." |

- Render `compliance.notes[]` as a bulleted list inside the banner (these carry the *why* — e.g. "exceeds the client's stated risk tolerance; unsuitable under Reg BI"). On STOP, optionally dim/strike-through the recommendations section to dramatize "the swarm walked away."
- **No verdict text beyond the three enum values** — switch purely on `compliance.verdict`.

---

## 4. Preset switcher (optional, demo bonus)

A small fixed control (top-right) to flip the loaded plan across the 3 demo clients **without reloading the page from scratch** (or by setting `?plan=` and reloading — simplest). Mapping:

| Button | plan file | Expected on screen |
| --- | --- | --- |
| **#1 Sharma (family)** | `sample-plan.json` | 6 specialist chips · green APPROVED banner · rich allocation/cone |
| **#2 Young accumulator** | `plan-young-accumulator.json` | **2 specialist chips** (board shrinks) · APPROVED · simple allocation |
| **#3 Pre-retiree (STOP)** | `plan-preretiree-stop.json` | 6 chips · **red STOP banner** · risk bars show tolerance≪recommended |

Implementation: `<button data-plan="...">` → on click set `location.search = '?plan=' + file` (reload-based, dead simple), OR re-`fetch` + re-run `renderPlan` and `chart.destroy()` existing charts before re-instantiating (keep references in a `charts[]` array). The fixture for #1 ships now; #2/#3 plan JSONs are produced when Track 1 runs the swarm on those presets — until then the switcher's #2/#3 buttons can point at hand-built fixtures with the same shape.

**Important for re-render:** keep every `Chart` instance in an array and call `c.destroy()` before re-`fetch` to avoid "Canvas is already in use" errors.

---

## 5. 90-second demo narration

> *(Dashboard open on preset #1, advisor desk framing.)*
>
> **[0:00]** "This is our AI advisory desk. Three clients just walked in — and there is **zero code** changed between them. The same swarm staffs itself to each one."
>
> **[0:10]** *Preset #1 — Sharma family.* "New mid-career family, complex: single-stock concentration, college, retirement, a vacation home. Watch the board." *Point at the specialist chips.* "**Six specialists** engaged — the full roster fanned out in parallel. The Market Strategist ran a live web search; those source links are real." *Scroll.* "Wellbeing 72, on track with gaps. Allocation **current vs target** — see that red slice, 34% in one employer stock? The target cuts it to 10%. Goals in green and red. The projection cone out to age 80. And up top — the **green APPROVED** banner. Compliance signed off; suitable."
>
> **[0:40]** *Switch to preset #2 — Young accumulator.* "Different client: 28, first \$40K, simple situation. Same engine — but watch the board **shrink**." *Chips collapse from six to two.* "Just **two** specialists — Portfolio and Goals. The router right-sized the team to the client. No compliance theater, no tax-estate lane it doesn't need. Clean, proportional plan, APPROVED."
>
> **[1:05]** *Switch to preset #3 — Pre-retiree.* "Last one is the punchline. 63, retiring in two years, capital-preservation mindset — and he's been pitched a concentrated, aggressive, high-fee product. The **full team** engages..." *charts populate, risk bars show tolerance far below the recommended aggressive band* "...and then the **Compliance lane turns red**." *Point at the STOP banner.* "**STOP — recommendation is unsuitable; exceeds the client's stated risk tolerance; fails Reg BI.** The swarm **refuses** to present it."
>
> **[1:25]** "It staffed itself to each client, and it walked away from the bad recommendation. That discipline — suitability you can't override — is exactly what a real advisory firm sells."

---

## 6. Acceptance checklist for eng-2

- [ ] `dashboard.html` loads `synthetic-data/sample-plan.json` and renders all 12 sections with no console errors.
- [ ] Every chart in §3 binds to the exact schema path listed — no hard-coded numbers.
- [ ] Compliance banner color switches purely on `compliance.verdict` (test all three by editing the fixture's verdict to APPROVED/REVISE/STOP).
- [ ] Header personalizes to `generatedFor`; specialist chips count == `routedSpecialists.length`.
- [ ] Allocation donuts use ONE shared assetClass→color map so before/after read as the same legend.
- [ ] Goal bars + projection cone span full width; gauge + risk + recs fit the 2-col grid.
- [ ] Disclaimers footer always visible.
- [ ] (Bonus) Preset switcher flips across the 3 plan files; charts `.destroy()` cleanly on re-render.
