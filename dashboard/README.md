# AI Wealth Advisory — Case Console (dashboard)

A self-contained UI for the demo. A **case list** of all client applications; click one to
open it. Two views per case:

- **Client View** — the polished plan you present to the client (wellbeing, risk, allocation
  current→target, goal funding, projection cone, recommendations, compliance banner).
- **Advisor / Internal** — employee-only: the specialist dialog, internal risk flags, and the
  suitability / compliance reasoning.

Three demo cases are seeded (in `cases.js`):

| Case | Routing | Verdict |
|---|---|---|
| **Sharma** — mid-career family | NEW_CLIENT_PLAN · full 6-specialist team | APPROVED (green) |
| **Young Accumulator** | PORTFOLIO_REVIEW · 3 specialists (board shrinks) | APPROVED (green) |
| **Pre-retiree** | RETIREMENT_READINESS · full team | **STOP (red)** — the punchline |

## Run it — Windows (for the demo)

**Easiest — no install, works fully OFFLINE:** double-click **`index.html`**. It opens in your
browser and renders immediately. The libraries (Tailwind + Chart.js) are vendored in `vendor/`,
and the case data is inlined via `cases.js` (loaded with a `<script>` tag, **not** `fetch`), so
there is **no server, no internet, and no `file://` CORS problem**.

Prefer a local server (or your browser blocks local scripts)? Either:
- double-click **`run.bat`**, or
- run **`py serve.py`** (or `python serve.py`) — opens `http://localhost:8000/`.

## Run it — macOS / Linux

Open `index.html` directly, or `python3 serve.py`.

## Add a real case from a swarm run

After `run_advisory.py` produces `outputs/financial_plan.json`:

```bash
python dashboard/build_cases.py        # emits a case object; paste it into cases.js (unique id)
```

## Files

```
dashboard/
├── index.html      — the Case Console (Tailwind + Chart.js, both vendored)
├── cases.js        — window.CASES (the 3 seeded demo cases)
├── vendor/         — offline copies of Tailwind + Chart.js
├── build_cases.py  — turn a real outputs/financial_plan.json into a case
├── run.bat         — Windows one-click local server
└── serve.py        — cross-platform local server
```

> Demo on synthetic, fictional data — not financial advice.
