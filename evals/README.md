# Evals — `financial_plan.json` quality gate

Two evals for the plan the Wealth Advisory swarm coordinator emits. Both take the
path to a `financial_plan.json` as their single argument.

## 1. `validate_plan.py` — deterministic gate (required)

Schema-validates the plan against [`schemas/financial_plan.schema.json`](../schemas/financial_plan.schema.json)
(JSON Schema, draft 2020-12) and adds structural sanity checks the schema can't express:

- `allocation.current` percents sum to ~100 (±1)
- `allocation.target` percents sum to ~100 (±1)
- `allocation.current` values sum > 0
- every `goal.fundedPercent` in `[0, 100]`
- `projections.series` ordered: `low <= mid <= high` per point, `year` strictly increasing
- `compliance.verdict` in `{APPROVED, REVISE, STOP}`
- `routedSpecialists` non-empty

Prints a `PASS`/`FAIL` report with one line per check and **exits non-zero on any failure**
— so it drops straight into CI or a pre-commit gate.

```bash
# install the one extra dependency (see note below)
pip install jsonschema

# validate the committed fixture (should PASS)
python evals/validate_plan.py synthetic-data/sample-plan.json

# validate a freshly generated plan from a swarm run
python evals/validate_plan.py outputs/financial_plan.json
echo $?   # 0 = PASS, 1 = check failure, 2 = bad input / missing dep
```

Pure Python stdlib + `jsonschema`. No network, no API key.

## 2. `judge_plan.py` — LLM-as-judge (optional)

Uses the Anthropic SDK (`claude-sonnet-4-6`) to score the plan **1–5** on:

- **coverage** — are all routed specialist lanes reflected, no gaps?
- **personalization** — tailored to this household vs generic boilerplate?
- **actionability** — specific, prioritized, owned recommendations?
- **suitability_consistency** — does the target allocation match `riskProfile.band`,
  and is `compliance.verdict` consistent with it (an over-aggressive plan should not be `APPROVED`)?

Prints the scores as JSON. Reads the key from the environment.

```bash
export ANTHROPIC_API_KEY=sk-ant-...        # or: set -a; . .env; set +a
python evals/judge_plan.py synthetic-data/sample-plan.json
```

Example output:

```json
{
  "coverage": 5,
  "personalization": 5,
  "actionability": 5,
  "suitability_consistency": 5,
  "rationale": "Target mix and APPROVED verdict are consistent with the Moderate Growth band."
}
```

## Dependency note

`validate_plan.py` needs **`jsonschema`**, which is not yet in the repo's
[`requirements.txt`](../requirements.txt). Add it:

```
jsonschema>=4.0.0
```

`judge_plan.py` uses `anthropic`, already pinned in `requirements.txt`.
