#!/usr/bin/env python3
"""Validate a financial_plan.json against the schema + structural sanity checks.

Usage:
    python evals/validate_plan.py path/to/financial_plan.json

Validates against schemas/financial_plan.schema.json (JSON Schema, draft 2020-12)
and then runs structural checks that the schema alone cannot express. Prints a
PASS/FAIL report with one line per check and exits non-zero if anything fails.

Dependencies: Python stdlib + `jsonschema` only.
"""

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.stderr.write(
        "ERROR: the 'jsonschema' package is required. "
        "Install it with:  pip install jsonschema  "
        "(also listed in requirements.txt).\n"
    )
    sys.exit(2)

# Repo root is the parent of evals/ ; schema lives at schemas/financial_plan.schema.json
REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "financial_plan.schema.json"

SUM_TOLERANCE = 1.0  # percent points; allocation sums must be within ~100 +/- 1
VALID_VERDICTS = {"APPROVED", "REVISE", "STOP"}


class Report:
    """Collects per-check results and renders a PASS/FAIL report."""

    def __init__(self):
        self.lines = []
        self.failed = 0

    def check(self, ok, name, detail=""):
        status = "PASS" if ok else "FAIL"
        if not ok:
            self.failed += 1
        suffix = f" — {detail}" if detail else ""
        self.lines.append(f"  [{status}] {name}{suffix}")
        return ok

    def render(self):
        out = "\n".join(self.lines)
        total = len(self.lines)
        passed = total - self.failed
        verdict = "PASS" if self.failed == 0 else "FAIL"
        out += (
            f"\n\n{'=' * 60}\n"
            f"RESULT: {verdict}  ({passed}/{total} checks passed)\n"
            f"{'=' * 60}"
        )
        return out


def _percent_sum(items):
    return sum(float(x.get("percent", 0)) for x in items if isinstance(x, dict))


def _value_sum(items):
    return sum(float(x.get("value", 0)) for x in items if isinstance(x, dict))


def schema_validate(plan, schema, report):
    """Run JSON Schema validation; record one line per error (or one PASS)."""
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(plan), key=lambda e: list(e.path))
    if not errors:
        report.check(True, "JSON Schema validation (financial_plan.schema.json)")
        return True
    for err in errors:
        loc = "/".join(str(p) for p in err.path) or "(root)"
        report.check(False, "JSON Schema validation", f"{loc}: {err.message}")
    return False


def structural_checks(plan, report):
    """Checks beyond what the schema can express."""
    # --- routedSpecialists non-empty ---
    routed = plan.get("routedSpecialists")
    report.check(
        isinstance(routed, list) and len(routed) > 0,
        "routedSpecialists is non-empty",
        f"got {routed!r}" if not (isinstance(routed, list) and routed) else "",
    )

    alloc = plan.get("allocation") or {}
    current = alloc.get("current") or []
    target = alloc.get("target") or []

    # --- allocation.current percents sum ~100 ---
    cur_pct = _percent_sum(current)
    report.check(
        abs(cur_pct - 100.0) <= SUM_TOLERANCE,
        "allocation.current percents sum to ~100 (+/-1)",
        f"sum = {cur_pct:g}",
    )

    # --- allocation.target percents sum ~100 ---
    tgt_pct = _percent_sum(target)
    report.check(
        abs(tgt_pct - 100.0) <= SUM_TOLERANCE,
        "allocation.target percents sum to ~100 (+/-1)",
        f"sum = {tgt_pct:g}",
    )

    # --- allocation.current values sum > 0 ---
    cur_val = _value_sum(current)
    report.check(
        cur_val > 0,
        "allocation.current values sum > 0",
        f"sum = {cur_val:g}",
    )

    # --- every goal.fundedPercent in [0,100] ---
    goals = plan.get("goals") or []
    bad_funded = [
        (g.get("name", f"#{i}"), g.get("fundedPercent"))
        for i, g in enumerate(goals)
        if not (isinstance(g, dict)
                and isinstance(g.get("fundedPercent"), (int, float))
                and 0 <= g["fundedPercent"] <= 100)
    ]
    report.check(
        not bad_funded,
        "every goal.fundedPercent in [0,100]",
        f"out of range: {bad_funded}" if bad_funded else "",
    )

    # --- projections.series ordered: low<=mid<=high per point, year strictly increasing ---
    series = (plan.get("projections") or {}).get("series") or []
    cone_bad = []
    year_bad = []
    prev_year = None
    for i, pt in enumerate(series):
        if not isinstance(pt, dict):
            cone_bad.append(f"#{i} not an object")
            continue
        low, mid, high = pt.get("low"), pt.get("mid"), pt.get("high")
        if None in (low, mid, high) or not (low <= mid <= high):
            cone_bad.append(f"#{i} (year {pt.get('year')}): {low}/{mid}/{high}")
        yr = pt.get("year")
        if prev_year is not None and not (isinstance(yr, int) and yr > prev_year):
            year_bad.append(f"#{i}: {prev_year} -> {yr}")
        if isinstance(yr, int):
            prev_year = yr
    report.check(
        not cone_bad,
        "projections.series cone ordered low<=mid<=high",
        f"violations: {cone_bad}" if cone_bad else "",
    )
    report.check(
        not year_bad,
        "projections.series year strictly increasing",
        f"violations: {year_bad}" if year_bad else "",
    )

    # --- compliance.verdict in {APPROVED, REVISE, STOP} ---
    verdict = (plan.get("compliance") or {}).get("verdict")
    report.check(
        verdict in VALID_VERDICTS,
        "compliance.verdict in {APPROVED, REVISE, STOP}",
        f"got {verdict!r}" if verdict not in VALID_VERDICTS else "",
    )


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("Usage: python evals/validate_plan.py <financial_plan.json>\n")
        return 2

    plan_path = Path(argv[1])
    if not plan_path.is_file():
        sys.stderr.write(f"ERROR: plan file not found: {plan_path}\n")
        return 2
    if not SCHEMA_PATH.is_file():
        sys.stderr.write(f"ERROR: schema not found: {SCHEMA_PATH}\n")
        return 2

    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"ERROR: {plan_path} is not valid JSON: {exc}\n")
        return 2
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    report = Report()
    print(f"Validating: {plan_path}")
    print(f"Against schema: {SCHEMA_PATH.relative_to(REPO_ROOT)}\n")

    schema_validate(plan, schema, report)
    structural_checks(plan, report)

    print(report.render())
    return 0 if report.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
