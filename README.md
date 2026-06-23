# AI Wealth Advisory Swarm

A coordinator + specialist **swarm** that turns a client's financial situation into a
personalized plan — Edward-Jones-style advice, built on Anthropic's
[Managed Agents multi-agent API](https://platform.claude.com/docs/en/managed-agents/multi-agent)
+ custom [Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

Drop a client ticket in → a **Senior Wealth Advisor** classifies it and delegates to the
right **subset** of specialists → they analyze in parallel → a **Compliance / Suitability
Reviewer** gates the result (and can say **STOP**) → out comes `financial_plan.json` + a
branded `financial_plan.pptx`.

## The idea in one picture

```
client ticket ─▶ Senior Wealth Advisor (coordinator, opus-4-8)
                   │  classify → delegate to a SUBSET (the team self-sizes)
                   ├─▶ Portfolio Analyst        (sonnet · asset-allocation-playbook)
                   ├─▶ Risk Profiler            (sonnet · risk-profiling)
                   ├─▶ Market Strategist        (sonnet · live web_search)
                   ├─▶ Goals & Wellbeing Planner(sonnet · financial-planning-playbook)
                   ├─▶ Tax & Estate Specialist  (haiku)
                   └─▶ Compliance Reviewer      (opus · APPROVED / REVISE / STOP)
                         │
                         ▼
              financial_plan.json  +  financial_plan.pptx
```

**Different client → different subset.** A simple `PORTFOLIO_REVIEW` wakes 2 specialists; a
full `NEW_CLIENT_PLAN` wakes 5 + Compliance. You watch the team assemble itself on the event
stream — that's the demo. (No NATS/message bus needed: the session event stream *is* the bus.)

## Quickstart

```bash
cp .env.sample .env        # then put your workspace ANTHROPIC_API_KEY in .env
./run_demo.sh              # installs deps + runs the full pipeline against the default client
```

`run_demo.sh` runs the whole chain and leaves the deliverables in `outputs/`:

```bash
open outputs/financial_plan.pptx                              # the branded deck
python evals/validate_plan.py outputs/financial_plan.json     # check the plan is well-formed
```

Run a different client to watch the swarm resize:

```bash
./run_demo.sh synthetic-data/clients/client-young-accumulator.md   # board shrinks to 2 lanes
./run_demo.sh synthetic-data/clients/client-preretiree-stop.md     # Compliance returns STOP
```

> Requires a workspace API key granted the `managed-agents-2026-04-01` research-preview beta.

### Manual steps (what run_demo.sh does)

```bash
pip install -r requirements.txt
python create_specialists.py   # -> .specialist_ids.json  (6 specialists)
python upload_skills.py        # uploads + attaches the 3 domain skills
python create_coordinator.py   # -> .coordinator_id       (router + pptx skill)
python setup_environment.py    # -> .environment_id
python run_advisory.py [client.md]   # streams events, saves outputs/
```

## Demo scenario (3 presets)

| Client | Ticket | Subset | Punch |
| --- | --- | --- | --- |
| `client-mid-career-family.md` | NEW_CLIENT_PLAN | full roster | rich plan + APPROVED |
| `client-young-accumulator.md` | PORTFOLIO_REVIEW | 2 lanes | board shrinks |
| `client-preretiree-stop.md` | RETIREMENT_READINESS | full | **Compliance STOP** |

## Repo map

- `create_*.py`, `upload_skills.py`, `run_advisory.py` — the swarm pipeline
- `skills/` — the three custom domain skills (allocation, risk, planning)
- `synthetic-data/clients/` — demo client tickets · `synthetic-data/sample-plan.json` — render fixture
- `schemas/financial_plan.schema.json` — the coordinator's output **contract**
- `evals/` — `validate_plan.py` (structural) + `judge_plan.py` (LLM-as-judge)
- `docs/ROADMAP.md` — plan & tracks · `docs/COST.md` — per-run cost · `docs/DECK_SPEC.md` — the HTML dashboard spec

## Notes

All client data is **fictional** and for demo only — **not financial advice**.
