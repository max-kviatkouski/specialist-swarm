# Cost Model — AI Wealth Advisory Swarm

> **Headline: ~$0.65 per full advisory run** (preset #1, full 6-agent roster). Steady-state prompt caching trims it to **~$0.54**; a Sonnet coordinator drops it to **~$0.48**. The whole 3-client demo costs **~$1.67**.

_As-of 2026-06-23. Prices verified live against the Anthropic pricing docs (see [Pricing source](#pricing-source))._

---

## Pricing source (verified, not assumed)

Fetched live from `https://platform.claude.com/docs/en/about-claude/pricing` and the models overview. Both pages agree:

| Model | Model ID | Input $/MTok | Output $/MTok | 5m cache write $/MTok | Cache read $/MTok |
| --- | --- | --: | --: | --: | --: |
| Claude Opus 4.8 | `claude-opus-4-8` | $5.00 | $25.00 | $6.25 | $0.50 |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | $3.00 | $15.00 | $3.75 | $0.30 |
| Claude Haiku 4.5 | `claude-haiku-4-5` | $1.00 | $5.00 | $1.25 | $0.10 |

**Prompt-caching multipliers** (on base input): 5-minute write = **1.25x**, 1-hour write = **2x**, cache read (hit) = **0.10x**.
**Web search** (server tool, Market Strategist): **$10 per 1,000 searches** = $0.01/search, plus standard token cost for the results pulled into context.
**Web fetch / code execution** (the pptx render runs in the session container): no extra charge beyond tokens when bundled with the run — only the standard input/output tokens are billed.
**Managed Agents session runtime:** **$0.08 per session-hour**, metered only while a thread's status is `running` (idle/waiting is free). One advisory run keeps threads `running` ~5–6 min of wall-clock → ~$0.008.

This swarm uses **Haiku 4.5 for no agent** in preset #1, so its prices are listed for reference only (it's available for a future cost-down lever — e.g. moving the Risk Profiler or pptx step to Haiku).

---

## Token assumptions (stated, per agent)

Reasonable per-agent estimates for the full-roster run. Each specialist sees the client profile (~2k tokens) plus its own skill playbook (~2–3k) plus system framing; the coordinator additionally ingests every specialist's reply.

| Agent | Model | Input tok | Output tok | Notes |
| --- | --- | --: | --: | --- |
| Portfolio Analyst | Sonnet 4.6 | 6,000 | 1,500 | profile + asset-allocation-playbook skill |
| Risk Profiler | Sonnet 4.6 | 6,000 | 1,500 | profile + risk-profiling skill |
| Market Strategist | Sonnet 4.6 | 6,000 | 1,500 | + **2 web_search calls** |
| Goals & Wellbeing Planner | Sonnet 4.6 | 6,000 | 1,500 | profile + financial-planning-playbook |
| Tax & Estate Specialist | Sonnet 4.6 | 6,000 | 1,500 | profile + tax rules |
| **Coordinator** (Senior Wealth Advisor) | **Opus 4.8** | 25,000 | 6,000 | aggregates 5 specialist replies + skill; emits `financial_plan.json` |
| **Compliance / Suitability Reviewer** | **Opus 4.8** | 10,000 | 1,000 | reviews the assembled plan; APPROVED/REVISE/STOP |
| **pptx render step** | **Opus 4.8** | 3,000 | 2,000 | coordinator drives the `pptx` skill in-container |

---

## Per-agent cost — one full advisory run (UNCACHED vs CACHED)

The **cached** column reflects *steady-state* operation: each agent's stable prefix (skill text + system prompt + the shared client profile) is served as a **cache read (0.10x)** rather than full-price input. Only the volatile tail is full-priced. For specialists, ~4k of the 6k input is stable; for the coordinator, only ~6k of its 25k is stable (the ~19k of aggregated specialist replies is inherently volatile and **cannot** be cached — this caps the saving).

| Agent | Model | Uncached $ | Cached $ (steady-state) |
| --- | --- | --: | --: |
| Portfolio Analyst | Sonnet 4.6 | $0.0405 | $0.0297 |
| Risk Profiler | Sonnet 4.6 | $0.0405 | $0.0297 |
| Market Strategist | Sonnet 4.6 | $0.0405 | $0.0297 |
| Goals & Wellbeing Planner | Sonnet 4.6 | $0.0405 | $0.0297 |
| Tax & Estate Specialist | Sonnet 4.6 | $0.0405 | $0.0297 |
| Market Strategist — web_search (2×) | — | $0.0200 | $0.0200 |
| Coordinator | Opus 4.8 | $0.2750 | $0.2480 |
| Compliance Reviewer | Opus 4.8 | $0.0750 | $0.0615 |
| pptx render step | Opus 4.8 | $0.0650 | $0.0560 |
| **Token subtotal** | | **$0.6375** | **$0.5340** |
| Session runtime (~6 min @ $0.08/h) | — | $0.0080 | $0.0080 |
| **PER-RUN TOTAL** | | **$0.6455** | **$0.5420** |

**Caching saves ~16% per run at steady state.** Worked example (specialist): uncached `6,000 × $3/MTok + 1,500 × $15/MTok = $0.0405`; cached `(4,000 × $3 × 0.10 + 2,000 × $3 + 1,500 × $15)/MTok = $0.0297`.

> **Honest caveat — a single COLD run barely benefits.** On the very first run the shared prefixes are *cache writes* (1.25x), not reads, with nothing prior to amortize against — so a one-shot cold run nets roughly break-even (the 1.25x write premium offsets the 0.10x reads within the same run). The ~16% saving is realized once the cache is warm: every repeat run, and every agent after the first that shares a prefix, reads at 0.10x. The 3-client demo (3 runs back-to-back, <5 min apart) is exactly that warm-cache regime. **Coordinator dominates cost (~43% of the run); its 19k-token aggregated-reply payload is the part caching can't touch.**

---

## Per-run total

| Scenario | Per advisory run |
| --- | --: |
| Uncached | **$0.65** |
| Cached (steady-state) | **$0.54** |

Comfortably inside the ROADMAP's ~$0.30–$1.00 ballpark.

---

## Full 3-client demo cost

The board reshapes per client, so cost scales with the roster size the router actually staffs:

| # | Preset | Roster | Per-run (uncached) |
| - | --- | --- | --: |
| 1 | Sharma household — `NEW_CLIENT_PLAN` | full 6 agents + pptx | $0.65 |
| 2 | Young accumulator — `PORTFOLIO_REVIEW` | 2 lanes (Portfolio + Goals) + coordinator + compliance + pptx | $0.38 |
| 3 | Risk-averse pre-retiree — `RETIREMENT_READINESS` | full 6 agents, Compliance returns **STOP** | $0.65 |
| | **3-client demo total (uncached)** | | **$1.67** |
| | **3-client demo total (warm cache)** | | **~$1.45** |

Preset #3 costs the same as #1 even though Compliance says STOP — the swarm still does the full analysis before refusing; the refusal is the *output*, not a shortcut. Preset #2 is cheaper purely because the board shrinks to 2 specialists (the demo's "right-sized to the client" beat is also a cost story).

---

## Cheaper variant — Sonnet coordinator + Sonnet compliance

Move the coordinator **and** the Compliance Reviewer (and the pptx render) from Opus 4.8 to Sonnet 4.6; keep the 5 specialists on Sonnet. Same token assumptions.

| Agent | Model | Cost $ |
| --- | --- | --: |
| 5 specialists + 2 web_search | Sonnet 4.6 | $0.2225 |
| Coordinator | **Sonnet 4.6** | $0.1650 |
| Compliance Reviewer | **Sonnet 4.6** | $0.0450 |
| pptx render step | **Sonnet 4.6** | $0.0390 |
| Session runtime | — | $0.0080 |
| **PER-RUN TOTAL** | | **$0.48** |

**~26% cheaper than the default Opus-coordinator run** ($0.48 vs $0.65). The trade-off: the coordinator's plan synthesis and the suitability gate are the two judgment-heavy steps where Opus 4.8 earns its premium — for the demo (and for the STOP punchline's credibility) keep Opus on the coordinator + compliance; use the all-Sonnet config for high-volume production triage where a human advisor still signs off.

---

## Cost-down levers (beyond the table)

- **Warm the cache:** run the 3 presets within the 5-minute cache window during the demo → the ~16% steady-state caching saving applies to presets #2 and #3.
- **Batch API (-50%):** non-interactive nightly portfolio reviews could run through the Batch API at half the token price — not usable for the live demo (sessions are stateful/interactive), but the obvious production lever.
- **Haiku 4.5 for mechanical lanes:** the pptx render step and arguably the Risk Profiler are formulaic; moving them to Haiku 4.5 ($1/$5 vs Sonnet $3/$15) shaves a few cents per run.
- **Trim coordinator input:** the coordinator's 25k input (mostly aggregated specialist replies) is the single largest line item. Having specialists return tight, structured JSON instead of prose directly shrinks the most expensive, least-cacheable token pool.

---

_Fictional demo figures on synthetic data. Token counts are estimates for planning; replace with measured `usage` from a real run for an exact bill._
