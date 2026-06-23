# AI Wealth Advisory Swarm — 50-Minute MVP Roadmap

**Pitch:** Drop a client's financial life into the swarm. A Senior Wealth Advisor (coordinator)
routes the right specialists — each an expert in one lane — they analyze in parallel, a
**Compliance / Suitability Reviewer** gates the result, and the swarm produces a personalized,
graphics-rich plan. Different client → different specialist team assembles itself live.

Edward-Jones-grade advice, built on the existing `coordinator + specialists + skills` skeleton.

---

## The architecture (grounded in the Managed Agents API — verified against docs)

- **One coordinator, superset roster, subset per ticket.** The API does **not** allow a
  coordinator to recruit unknown agents mid-session — the roster is snapshotted at create time.
  So we register the full specialist roster once, and the coordinator **delegates to a subset**
  per client. That subset-selection *is* the "dynamic team," and it's visible on the event stream.
  Caps: ≤20 agents, ≤25 concurrent threads, depth 1.
- **The event stream is the message bus.** `session.thread_created` / `thread_status_running` /
  `agent.thread_message_sent` / `agent.thread_message_received` already carry every delegate→/reply←
  with agent names. **No NATS in the MVP** — it's a single "productionization" slide only (ingest
  queue at the Salesforce/CRM seam). Saying this out loud is a credibility point.
- **The wow = the board reshapes per client + a Compliance STOP.** See demo script below.

## The deliverable strategy (two layers — guaranteed + wow)

1. **Guaranteed (near-zero code):** the coordinator emits **`financial_plan.json`** (the contract
   in `schemas/financial_plan.schema.json`) **and** produces a branded deck via the pre-built
   Anthropic **`pptx`** skill (or `docx`). Attaching it is one line — `skills=[{"type":"anthropic","skill_id":"pptx"}]`.
2. **Wow (Track 2):** a personalized **interactive HTML dashboard** rendered from `financial_plan.json`
   (Chart.js: allocation donut current→target, goal-funding bars, projection cone, risk gauge,
   wellbeing score, compliance banner). Built against the fixture `synthetic-data/sample-plan.json`
   — **available now**, so Track 2 starts immediately, in parallel.

---

## Demo scenario — 3 presets, one engine, zero code changes between them

| # | Client preset | Router classifies | Specialist subset (board) | Punch |
| - | --- | --- | --- | --- |
| 1 | **Sharma household** (mid-career family, single-stock concentration) — `client-mid-career-family.md` | `NEW_CLIENT_PLAN` | **full roster (6)** fans out | rich plan + pptx deck + APPROVED |
| 2 | **Young accumulator** (28, first $40K, simple) — *to author* | `PORTFOLIO_REVIEW` | **2 lanes** (Portfolio + Goals) — board shrinks | "right-sized to the client" |
| 3 | **Risk-averse pre-retiree pitched an aggressive product** — *to author* | `RETIREMENT_READINESS` | full roster, but **Compliance returns STOP** | 🎤 the swarm **refuses** an unsuitable recommendation |

**90-second narration:** "This is our advisory desk — three clients just came in. No code between them."
Drop #1 → board explodes into 6 parallel lanes, web_search fires on the Market Strategist, a branded
deck pops out. Drop #2 → board **shrinks to 2 lanes** (audible gasp). Drop #3 → full team works, then the
**Compliance lane turns red: `VERDICT: STOP — recommended product exceeds the client's stated risk
tolerance; unsuitable under Reg BI.`** The swarm staffed itself to each client and *walked away* from the
bad one. That's the discipline a real advisory firm sells.

---

## The data contract (what unblocks Track 2 right now)

`schemas/financial_plan.schema.json` + fixture `synthetic-data/sample-plan.json`. Key fields the
dashboard renders: `financialWellbeing.score`, `riskProfile`, `allocation.current/target`, `goals[]`,
`projections.series[]` (low/mid/high cone), `recommendations[]`, and **`compliance.verdict`** (APPROVED/
REVISE/STOP → drives the banner color). `routedSpecialists[]` proves the subset that assembled.

---

## Tracks (Trello-ready — one card each)

### Track 1 — Swarm brains  ·  owner: **eng-1 (Dmitriy)**
Pivot Deal Desk → Wealth Advisory, keeping (corrected) plumbing.
- Rewrite `create_specialists.py` → financial roster: **Portfolio Analyst, Risk Profiler,
  Market Strategist (web_search), Goals & Wellbeing Planner, Tax & Estate Specialist**.
- Author 3 skills under `skills/`: `asset-allocation-playbook`, `risk-profiling`,
  `financial-planning-playbook` (model after the existing `pricing-playbook` shape).
- Rewrite coordinator → **Senior Wealth Advisor router** with a hard-pinned routing table; instruct it
  to emit `financial_plan.json` matching the schema, then produce the pptx deck.
- Add **Compliance / Suitability Reviewer** (adapt `stretch_critic_subagent.py`; APPROVED/REVISE/**STOP**).
- Author presets #2 and #3.

### Track 2 — The face (HTML dashboard)  ·  owner: **eng-2 (partner)** — *unblocked now*
- Render `synthetic-data/sample-plan.json` → a beautiful single-page HTML report (Chart.js + Tailwind).
- Compliance banner switches on `compliance.verdict`. Personalize header to `generatedFor`.
- Bonus: a preset switcher so the demo flips between the 3 clients.

### Track 3 — Make-it-work fixes + evals + cost  ·  owner: **automated workflow + eng-1**
Apply the verified fixes below; the parallel workflow is producing `evals/` + `docs/COST.md` +
`docs/DECK_SPEC.md` + presets #2/#3.

---

## Make-it-work punch list (verified against the live API docs)

1. `pip install -r requirements.txt`; provide the test key in **`.env`** (loaded inline, never printed);
   confirm the workspace has the `managed-agents-2026-04-01` beta grant.
2. **DOCX/PPTX BLOCKER:** the coordinator is created with **no skills array** → no document is ever
   produced. Add `skills=[{"type":"anthropic","skill_id":"pptx"}]` (or `docx`) to
   `create_coordinator.py`'s `beta.agents.create`.
3. **EVENT-LOOP BUG:** `run_deal_desk.py` breaks on `session.status_idle` — **not a real event**.
   Use `session.thread_status_idle` on the coordinator thread (stop_reason `end_turn`), or the loop hangs.
4. **FILES LAG:** wrap `client.beta.files.list(scope_id=...)` in a 1–3s retry (×2–3) after idle.
5. **RUN ORDER:** `setup_environment.py` is missing from the README but required. Correct order:
   `create_specialists → upload_skills → create_coordinator → setup_environment → run_*`.
6. **MODEL BUMP:** `claude-opus-4-7` → **`claude-opus-4-8`** (current) for coordinator + compliance reviewer.
   Keep `claude-sonnet-4-6` (specialists) and `claude-haiku-4-5-20251001`.
7. **upload_skills.py idempotency:** `s.get('skill_id')` crashes on re-run (skills are pydantic models) —
   use `getattr(s, 'skill_id', None)` and serialize to dicts before re-submitting. Matters for our dev loop.
8. **GATE:** run the base swarm end-to-end and confirm a real document lands in `outputs/` **before** any twist.

## ~50-minute timeline
- **0–15 (both):** fixes #1–#7, base swarm green against preset #1, document in `outputs/`. **Gate.**
- **15–35 (split):** eng-1 = financial specialists + skills + Compliance STOP; eng-2 = HTML dashboard on the fixture.
- **35–45 (both):** wire presets #2/#3, dry-run until board grow/shrink + STOP are deterministic.
- **45–50 (both):** dress rehearsal + **record a clean fallback run** (guards against a live 429).

## Evals & cost (Track 3 — workflow output)
- **Eval:** `evals/validate_plan.py` — schema-validate `financial_plan.json` + structural checks
  (allocations sum ~100, funded% in range, projection cone ordered, compliance verdict present,
  routedSpecialists is a valid subset). Optional LLM-judge for coverage/personalization/suitability.
- **Cost:** `docs/COST.md` — per-run $ from real token usage (Opus coordinator + Sonnet×3/Haiku
  specialists + Opus compliance + skill render). Rough ballpark **~$0.30–$1.00 per advisory run**;
  the workflow produces the exact per-model table from a measured test run.

## Conventions
- **Secrets:** test key in `.env` only (git-ignored). Never commit `.env`; never print values.
- **Branching:** feature branches → PR to `main`. Coordinate lanes on Trello so Track 1/2 don't collide.
