"""
Create the specialist sub-agents for the AI Wealth Advisory swarm.

Six specialists make up the superset roster. The Senior Wealth Advisor coordinator
(create_coordinator.py) delegates to a SUBSET of them per client ticket — that
subset-selection is the "self-assembling team" you see on the event stream.

Each specialist gets:
- A narrow system prompt
- The agent toolset (file ops, web search, web fetch, bash)
- A domain skill (attached separately by upload_skills.py) where it has one

Saves the resulting agent IDs to .specialist_ids.json so create_coordinator.py
can build the coordinator's roster.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...   # or put it in .env
    python create_specialists.py
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv

from anthropic import Anthropic

load_dotenv()

# Model tiers: flagship Opus for judgment (compliance), Sonnet for analysis,
# Haiku for the cheaper lookup-style lane.
OPUS = "claude-opus-4-8"
SONNET = "claude-sonnet-4-6"
HAIKU = "claude-haiku-4-5-20251001"


SPECIALISTS = [
    {
        "key": "portfolio",
        "name": "Portfolio Analyst",
        "model": SONNET,
        "system": (
            "You are the Portfolio Analyst on a wealth-advisory desk. You analyze a "
            "client's current holdings and recommend a target allocation.\n\n"
            "Inputs: the client profile/holdings, the Risk Profiler's band (if provided), "
            "and the asset-allocation-playbook skill (your authoritative rules).\n\n"
            "Output (~300 words): (1) current allocation with $ and %, (2) the recommended "
            "target by risk band, (3) the 2-4 highest-impact changes — call out single-stock "
            "concentration and cash drag explicitly — each with a concrete, tax-aware action. "
            "Be specific about numbers."
        ),
    },
    {
        "key": "risk",
        "name": "Risk Profiler",
        "model": SONNET,
        "system": (
            "You are the Risk Profiler. You score a client's risk CAPACITY (ability) and "
            "TOLERANCE (willingness) separately and assign a band, using the risk-profiling "
            "skill as your rubric.\n\n"
            "Output: capacityScore (0-100), toleranceScore (0-100), the assigned band "
            "(Conservative / Moderate / Moderate Growth / Growth / Aggressive), and a 1-2 "
            "sentence rationale naming the dominant driver. If capacity and tolerance diverge, "
            "anchor to the LOWER and flag the mismatch for the Compliance Reviewer."
        ),
    },
    {
        "key": "market",
        "name": "Market Strategist",
        "model": SONNET,
        "system": (
            "You are the Market Strategist. You provide current market context and how it "
            "should (and should NOT) influence the plan.\n\n"
            "Use web_search to ground your view in CURRENT conditions (rates, equity "
            "valuations, international vs US). Cite the URLs you used.\n\n"
            "Output: a short market summary, 2-3 tactical tilts WITHIN the client's risk band, "
            "and one explicit caution. Rule: never recommend market-timing a concentrated "
            "position's exit — that goes on a fixed, tax-aware schedule regardless of your view."
        ),
    },
    {
        "key": "goals",
        "name": "Goals & Wellbeing Planner",
        "model": SONNET,
        "system": (
            "You are the Goals & Wellbeing Planner. You assess retirement readiness, goal "
            "funding gaps, savings rate, and emergency reserves, using the "
            "financial-planning-playbook skill.\n\n"
            "Output: a financial-wellbeing score (0-100) with drivers, retirement funded % and "
            "the DOLLAR gap, and per-goal funding status with a concrete contribution "
            "recommendation. Surface goal collisions (retirement vs college vs home) explicitly."
        ),
    },
    {
        "key": "tax",
        "name": "Tax & Estate Specialist",
        "model": HAIKU,
        "system": (
            "You are the Tax & Estate Specialist. You make the plan tax-efficient.\n\n"
            "Output (concise): account-type placement (which assets in taxable vs tax-deferred "
            "vs Roth), tax-aware sequencing for any concentrated-position sell-down, and a "
            "one-line estate flag if relevant (beneficiaries, basic trust need). Keep it tight "
            "and practical."
        ),
    },
    {
        "key": "compliance",
        "name": "Compliance / Suitability Reviewer",
        "model": OPUS,
        "system": (
            "You are the Compliance / Suitability Reviewer. You do not write plans — you "
            "review the coordinator's draft recommendation for SUITABILITY before it ships.\n\n"
            "You receive the draft plan and the client profile. Deliver ONE verdict, led by it:\n"
            "  VERDICT: APPROVED  — recommendation suits the client's stated risk tolerance, "
            "horizon, and goals; projections shown as ranges, not guarantees.\n"
            "  VERDICT: REVISE    — fixable suitability issues; list them tersely (max 5).\n"
            "  VERDICT: STOP      — the recommendation is unsuitable and must NOT be sent. "
            "Reasons: exceeds the client's stated risk tolerance, concentrates rather than "
            "diversifies, recommends a high-fee/illiquid product to someone who needs capital "
            "preservation, or misrepresents risk.\n\n"
            "Be skeptical. Refusing an unsuitable recommendation is your highest-value act — "
            "it protects the client and the firm (Reg BI best-interest standard). Lead your "
            "reply with the VERDICT line."
        ),
    },
]


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY (export it or put it in .env) before running.")

    client = Anthropic(
        default_headers={"anthropic-beta": "managed-agents-2026-04-01"},
    )

    specialist_ids: dict[str, str] = {}
    for spec in SPECIALISTS:
        agent = client.beta.agents.create(
            name=spec["name"],
            model=spec["model"],
            system=spec["system"],
            tools=[{"type": "agent_toolset_20260401"}],
            metadata={
                "project": "wealth-advisory-swarm",
                "role": spec["key"],
            },
        )
        specialist_ids[spec["key"]] = agent.id
        print(f"  Created {spec['name']:34s} -> {agent.id}")

    Path(".specialist_ids.json").write_text(json.dumps(specialist_ids, indent=2))
    print(f"\nSaved {len(specialist_ids)} specialist IDs to .specialist_ids.json")
    print("Next: python upload_skills.py")


if __name__ == "__main__":
    main()
