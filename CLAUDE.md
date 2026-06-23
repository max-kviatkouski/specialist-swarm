# CLAUDE.md

Guidance for Claude Code (and any AI agents) working in this repository.

## Shared backlog — GitHub Issues

This repo uses **GitHub Issues as the shared backlog** so multiple developers and
Claude Code agents don't duplicate work. Use the `gh` CLI. Follow this protocol
every session:

1. **Before starting**, see what's open and who's on it:
   ```bash
   gh issue list --state open --json number,title,assignees,labels
   ```
   Skip anything already assigned or labeled `in-progress` — someone has it.

2. **Claim an unassigned issue before working on it** (the anti-collision step):
   ```bash
   gh issue edit <number> --add-assignee @me --add-label "in-progress"
   ```
   If a race is possible, claim FIRST, then re-list to confirm you got it; if it's
   now assigned to someone else, back off and pick another.

3. **While working**, leave a short status comment so others see progress:
   ```bash
   gh issue comment <number> --body "Started: <what you're doing>"
   ```

4. **When done**, link the PR and close it:
   ```bash
   gh issue edit <number> --add-label "done" --remove-label "in-progress"
   gh issue close <number> --comment "Done in #<PR>"
   ```

5. **New work you discover** → file it so it's visible to everyone, don't keep it
   in chat:
   ```bash
   gh issue create --title "<task>" --body "<context>" --label "todo"
   ```

Re-run `gh issue list` at the start of each session and before picking up a new
task so you never start something already claimed.

## What this project is

An **AI Wealth Advisory Swarm** (hackathon MVP) built on Anthropic's Managed Agents
multi-agent beta API (`managed-agents-2026-04-01`). A **Senior Wealth Advisor** coordinator
classifies a client ticket and delegates to a **subset** of six specialists, a **Compliance /
Suitability Reviewer** gates the result (`APPROVED` / `REVISE` / `STOP`), and the swarm emits
`financial_plan.json` + a branded `financial_plan.pptx`. See `README.md` and `docs/ROADMAP.md`.

Pivoted from the upstream "Deal Desk" starter — the stale Deal Desk scenario files were removed
(recoverable from git history); the same coordinator+specialists+skills plumbing is reused.

## How to run it

```bash
cp .env.sample .env     # add a workspace ANTHROPIC_API_KEY with the managed-agents beta grant
./run_demo.sh           # full pipeline → outputs/ (or pass a client .md path)
```

Manual chain (what `run_demo.sh` does, in order): `create_specialists.py` → `upload_skills.py`
→ `create_coordinator.py` → `setup_environment.py` → `run_advisory.py`. Each step caches state
to git-ignored dotfiles (`.specialist_ids.json`, `.coordinator_id`, `.environment_id`, …), so
re-runs are cheap. Inspect output: `open outputs/financial_plan.pptx`; validate the plan:
`python evals/validate_plan.py outputs/financial_plan.json`.

## Architecture facts worth knowing (verified against the docs)

- **No runtime "recruiting."** A coordinator's `multiagent.agents` roster is snapshotted at
  create/update time. "Dynamic team" = the coordinator **delegates to a subset** of the pinned
  superset roster per ticket (≤20 agents, ≤25 threads, depth 1). The board grow/shrink you see
  is subset-selection, not in-session spawning.
- **The event stream is the message bus** (`session.thread_created`, `agent.thread_message_sent/
  received`, …). No NATS in the MVP. The run loop's terminal signal is per-thread
  `session.thread_status_idle` — **not** a `session.status_idle` event (that doesn't exist).
- **Pre-built skills** (`pptx`/`docx`/`xlsx`/`pdf`) attach via `skills=[{"type":"anthropic",
  "skill_id":"pptx"}]`. The coordinator must carry the skill that produces the deliverable.
- **Models:** coordinator + Compliance Reviewer use `claude-opus-4-8`; analysis specialists
  `claude-sonnet-4-6`; the Tax lane `claude-haiku-4-5-20251001`.

## The data contract

`schemas/financial_plan.schema.json` is the single contract the coordinator emits and that the
HTML dashboard, the pptx deck, and `evals/validate_plan.py` all consume. `synthetic-data/
sample-plan.json` is a valid fixture (passes the validator 9/9) — render UI against it.

## Conventions

- **Secrets:** the test key lives only in `.env` (git-ignored). Never print or commit values;
  scripts load it via `python-dotenv`, shell wrappers via `set -a; . .env; set +a`.
- **Branching:** feature branch → PR to `main`; keep the branch rebased on `origin/main`.
