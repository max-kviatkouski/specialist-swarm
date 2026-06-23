#!/usr/bin/env python3
"""Optional LLM-as-judge for a financial_plan.json (claude-sonnet-4-6).

Scores 1-5 on coverage, personalization, actionability, and
suitability-consistency (does the recommended allocation match
riskProfile.band AND compliance.verdict?). Prints JSON scores to stdout.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python evals/judge_plan.py path/to/financial_plan.json

Dependencies: anthropic SDK (already in requirements.txt).
"""

import json
import os
import sys

from anthropic import Anthropic

MODEL = "claude-sonnet-4-6"

RUBRIC = (
    "You are a meticulous wealth-management QA reviewer. Score the financial plan "
    "JSON 1-5 (5=excellent) on each dimension:\n"
    "- coverage: are all routedSpecialists' lanes reflected (risk, allocation, "
    "goals, market, tax, compliance) with no gaps?\n"
    "- personalization: is it tailored to THIS household (name, ages, goals, "
    "concentration, tax bracket) vs generic boilerplate?\n"
    "- actionability: are recommendations specific, prioritized, and owned?\n"
    "- suitability_consistency: does the TARGET allocation and the recommendations "
    "match riskProfile.band, and is compliance.verdict consistent with them "
    "(e.g. an over-aggressive plan should NOT be APPROVED)?\n"
    "Reply with ONLY a JSON object: {\"coverage\":N,\"personalization\":N,"
    "\"actionability\":N,\"suitability_consistency\":N,\"rationale\":\"one sentence\"}."
)


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("Usage: python evals/judge_plan.py <financial_plan.json>\n")
        return 2
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.stderr.write("ERROR: set ANTHROPIC_API_KEY (optional judge needs it).\n")
        return 2

    plan = json.loads(open(argv[1], encoding="utf-8").read())
    client = Anthropic(api_key=api_key)
    resp = client.messages.create(
        model=MODEL,
        max_tokens=400,
        system=RUBRIC,
        messages=[{
            "role": "user",
            "content": "Plan to score:\n" + json.dumps(plan, ensure_ascii=False),
        }],
    )
    text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
    # Strip markdown fences if the model wraps the JSON.
    if text.startswith("```"):
        text = text.strip("`").lstrip("json").strip()
    try:
        scores = json.loads(text)
    except json.JSONDecodeError:
        scores = {"error": "judge did not return JSON", "raw": text}
    print(json.dumps(scores, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
