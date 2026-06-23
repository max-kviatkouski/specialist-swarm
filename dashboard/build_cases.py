#!/usr/bin/env python3
"""
build_cases.py — Convert a real swarm-run output into a dashboard case object.

USAGE
-----
After running the AI Wealth Advisory swarm, you will have (relative to the repo root):
    outputs/financial_plan.json        — the plan produced by the coordinator
    outputs/coordinator-transcript.txt — the raw coordinator transcript (optional)

Run from anywhere inside the repo:

    python dashboard/build_cases.py

This script reads those two files, wraps the plan in the dashboard case shape
(adding a synthetic `internal` section), and prints the resulting JSON to stdout.

To add the new case to the console, paste the printed JSON into dashboard/cases.js
and append it to the window.CASES array, giving it a unique `id`.

OPTIONAL FLAGS
--------------
    --plan  PATH    Override the default path to financial_plan.json
    --transcript PATH  Override the default path to coordinator-transcript.txt
    --out   PATH    Write the JSON to a file instead of stdout

CASE OBJECT SHAPE
-----------------
{
  "id":               "<str — set this yourself to something like 'client-2026-07'>",
  "<all financial_plan.json fields...>": ...,
  "internal": {
    "dialog":          [{"specialist": str, "role": str, "message": str}],
    "riskFlags":       [{"label": str, "severity": "high"|"medium"|"low", "detail": str}],
    "talkingPoints":   [str],
    "complianceReasoning": str
  }
}

The `internal` section is built from the coordinator transcript where possible.
If the transcript is not available or cannot be parsed, placeholder values are
inserted and labeled clearly for the advisor to fill in manually.

Dependencies: Python stdlib only (json, pathlib, re, textwrap, sys, argparse).
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ── default paths (relative to the repo root, one level up from dashboard/) ───
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PLAN_PATH = REPO_ROOT / "outputs" / "financial_plan.json"
DEFAULT_TRANSCRIPT_PATH = REPO_ROOT / "outputs" / "coordinator-transcript.txt"

VALID_VERDICTS = {"APPROVED", "REVISE", "STOP"}
SEVERITY_KEYWORDS = {
    "high":   ["stop", "unsuitable", "concentration", "breach", "fail", "critical",
               "illiquid", "surrender", "loss", "exceed"],
    "medium": ["drag", "gap", "shortfall", "below", "lag", "under-fund", "partial",
               "moderate", "watch", "caution"],
}


def load_plan(path: Path) -> dict:
    """Load and parse the financial_plan.json file."""
    if not path.is_file():
        sys.stderr.write(
            f"ERROR: plan file not found: {path}\n"
            f"Run the swarm first (python run_advisory.py ...) to generate outputs/financial_plan.json\n"
        )
        sys.exit(1)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"ERROR: {path} is not valid JSON: {exc}\n")
        sys.exit(1)


def load_transcript(path: Path) -> str | None:
    """Load the coordinator transcript, returning None if not found."""
    if not path.is_file():
        sys.stderr.write(
            f"WARNING: transcript not found at {path} — internal.dialog will use placeholders.\n"
        )
        return None
    return path.read_text(encoding="utf-8")


def extract_specialist_turns(transcript: str, routed: list[str]) -> list[dict]:
    """
    Heuristically parse specialist contributions from the coordinator transcript.

    Looks for patterns like:
        [Specialist Name] ...message...
        SPECIALIST: <name> — ...
    Falls back to placeholder entries for any specialist not found.
    """
    turns = []
    for specialist in routed:
        # Try to find a section attributed to this specialist (case-insensitive)
        pattern = rf"(?i)(?:\[{re.escape(specialist)}\]|{re.escape(specialist)}\s*[:\-—])([^\[]*)"
        match = re.search(pattern, transcript)
        message = match.group(1).strip()[:1200] if match else (
            f"[Placeholder — no matching transcript section found for '{specialist}'. "
            f"Paste the specialist's contribution here.]"
        )
        # Clean up extra whitespace
        message = re.sub(r"\s{2,}", " ", message)
        turns.append({
            "specialist": specialist,
            "role": _guess_role(specialist),
            "message": message,
        })
    return turns


def _guess_role(specialist: str) -> str:
    """Map a specialist name to a short role description."""
    name_lower = specialist.lower()
    if "portfolio" in name_lower:    return "Portfolio construction & analysis"
    if "risk" in name_lower:         return "Risk capacity & tolerance assessment"
    if "market" in name_lower:       return "Market context & tactical positioning"
    if "goal" in name_lower:         return "Goal gap analysis & wellbeing scoring"
    if "tax" in name_lower or "estate" in name_lower: return "Tax efficiency & estate planning"
    if "compliance" in name_lower or "suitability" in name_lower: return "Suitability review & regulatory sign-off"
    return "Specialist contribution"


def infer_risk_flags(plan: dict) -> list[dict]:
    """
    Build a best-effort list of risk flags from the plan data.

    Checks for: concentration, cash drag, capacity/tolerance gap, compliance STOP.
    """
    flags = []
    alloc = plan.get("allocation", {})
    current = alloc.get("current", [])

    # Concentrated positions (any single class > 25%)
    for item in current:
        pct = item.get("percent", 0)
        cls = item.get("assetClass", "Unknown")
        if pct >= 25 and cls.lower() not in ("us equity", "bonds"):
            flags.append({
                "label": f"Concentration — {cls}",
                "severity": "high" if pct >= 30 else "medium",
                "detail": (
                    f"{cls} represents {pct}% of the portfolio. "
                    f"A concentrated single-name or single-strategy position of this size "
                    f"creates asymmetric downside risk."
                ),
            })

    # Cash drag
    cash_items = [i for i in current if "cash" in i.get("assetClass", "").lower()]
    cash_pct = sum(i.get("percent", 0) for i in cash_items)
    if cash_pct > 8:
        flags.append({
            "label": "Cash drag",
            "severity": "medium",
            "detail": (
                f"{cash_pct:.0f}% of the portfolio is in cash — above the emergency-reserve "
                f"threshold. Excess cash earns below the target allocation's expected return."
            ),
        })

    # Capacity / tolerance gap
    rp = plan.get("riskProfile", {})
    cap = rp.get("capacityScore", 0)
    tol = rp.get("toleranceScore", 0)
    gap = abs(cap - tol)
    if gap >= 15:
        flags.append({
            "label": "Capacity / tolerance gap",
            "severity": "medium" if gap < 40 else "high",
            "detail": (
                f"Risk capacity ({cap}/100) and tolerance ({tol}/100) diverge by {gap} points. "
                f"The plan is anchored to the lower of the two; behavioral risk "
                f"(e.g., panic selling) is elevated if allocations are closer to capacity."
            ),
        })

    # Compliance STOP
    verdict = (plan.get("compliance") or {}).get("verdict", "")
    if verdict == "STOP":
        flags.insert(0, {
            "label": "Compliance STOP — unsuitable recommendation",
            "severity": "high",
            "detail": (
                "The compliance reviewer has issued a STOP verdict. "
                "The plan as originally proposed may NOT be presented to the client. "
                "See compliance notes and internal complianceReasoning for the full rationale."
            ),
        })

    if not flags:
        flags.append({
            "label": "No material risk flags identified",
            "severity": "low",
            "detail": "The plan passed all automated flag checks. Manual review still recommended.",
        })

    return flags


def build_talking_points(plan: dict) -> list[str]:
    """Generate generic advisor talking points from the plan data."""
    pts = []
    wb = plan.get("financialWellbeing", {})
    score = wb.get("score", 0)
    pts.append(
        f"Open with the wellbeing score ({score}/100 — '{wb.get('band', '')}') "
        f"to anchor the conversation positively before discussing gaps."
    )
    verdict = (plan.get("compliance") or {}).get("verdict", "")
    if verdict == "STOP":
        pts.append(
            "Be direct about the STOP: explain why the proposed recommendation was refused "
            "and immediately present the suitable alternative. Do not dwell — pivot quickly."
        )
    goals = plan.get("goals", [])
    off_track = [g["name"] for g in goals if not g.get("onTrack")]
    if off_track:
        pts.append(
            f"Address off-track goals ({', '.join(off_track)}) with specific, actionable steps "
            f"— clients respond better to 'here is what we do' than to 'you have a gap.'"
        )
    recs = [r for r in plan.get("recommendations", []) if r.get("priority") == "high"]
    if recs:
        pts.append(
            f"Lead with the highest-priority recommendation: '{recs[0].get('title', '')}' — "
            f"establish this as the single most important action before covering secondary items."
        )
    pts.append(
        "[Placeholder] Add any client-specific talking points based on advisor notes "
        "or the coordinator transcript before the client meeting."
    )
    return pts


def build_compliance_reasoning(plan: dict, transcript: str | None) -> str:
    """
    Extract or synthesize the compliance reasoning.

    Tries to pull the relevant section from the transcript; falls back to a
    structured placeholder built from the plan's compliance fields.
    """
    if transcript:
        # Try to extract a compliance reasoning section
        pattern = r"(?i)(?:compliance\s*reason|suitability\s*reason|reg\s*bi|verdict\s*reason)[:\s]+(.*?)(?=\n\n|\Z)"
        match = re.search(pattern, transcript, re.DOTALL)
        if match:
            text = match.group(1).strip()[:2000]
            if len(text) > 80:
                return re.sub(r"\s{2,}", " ", text)

    # Build from plan fields
    compliance = plan.get("compliance", {})
    verdict = compliance.get("verdict", "UNKNOWN")
    reviewer = compliance.get("reviewer", "Compliance Reviewer")
    notes = compliance.get("notes", [])
    notes_text = " ".join(f"({i+1}) {n}" for i, n in enumerate(notes))
    return (
        f"Verdict: {verdict}. Reviewer: {reviewer}. "
        f"Summary: {notes_text} "
        f"[Populate with the full Reg BI five-axis analysis from the coordinator transcript "
        f"before filing this case.]"
    )


def build_case(plan: dict, transcript: str | None) -> dict:
    """Assemble the full case object for the dashboard."""
    routed = plan.get("routedSpecialists", [])
    dialog = extract_specialist_turns(transcript, routed) if transcript else [
        {
            "specialist": s,
            "role": _guess_role(s),
            "message": (
                f"[Placeholder — transcript not available for '{s}'. "
                f"Paste the specialist's contribution here.]"
            ),
        }
        for s in routed
    ]

    internal = {
        "dialog": dialog,
        "riskFlags": infer_risk_flags(plan),
        "talkingPoints": build_talking_points(plan),
        "complianceReasoning": build_compliance_reasoning(plan, transcript),
    }

    case = {"id": "new-case-CHANGEME"}
    case.update(plan)        # all plan fields verbatim
    case["internal"] = internal
    return case


def validate_basic(plan: dict) -> list[str]:
    """Return a list of warning strings for common schema violations."""
    warnings = []
    alloc = plan.get("allocation", {})
    cur = alloc.get("current", [])
    tgt = alloc.get("target", [])
    cur_sum = sum(x.get("percent", 0) for x in cur)
    tgt_sum = sum(x.get("percent", 0) for x in tgt)
    if abs(cur_sum - 100) > 1:
        warnings.append(f"allocation.current percents sum to {cur_sum:.1f} (should be ~100)")
    if abs(tgt_sum - 100) > 1:
        warnings.append(f"allocation.target percents sum to {tgt_sum:.1f} (should be ~100)")
    goals = plan.get("goals", [])
    for g in goals:
        fp = g.get("fundedPercent", -1)
        if not (0 <= fp <= 100):
            warnings.append(f"goal '{g.get('name')}' fundedPercent={fp} is out of range [0,100]")
    series = (plan.get("projections") or {}).get("series", [])
    for i, pt in enumerate(series):
        lo, mi, hi = pt.get("low"), pt.get("mid"), pt.get("high")
        if None not in (lo, mi, hi) and not (lo <= mi <= hi):
            warnings.append(f"projection cone ordering violation at point #{i} (year {pt.get('year')}): {lo}/{mi}/{hi}")
    verdict = (plan.get("compliance") or {}).get("verdict")
    if verdict not in VALID_VERDICTS:
        warnings.append(f"compliance.verdict='{verdict}' is not one of {VALID_VERDICTS}")
    routed = plan.get("routedSpecialists", [])
    if not routed:
        warnings.append("routedSpecialists is empty")
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a dashboard case object from a swarm run's outputs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--plan", type=Path, default=DEFAULT_PLAN_PATH,
        help=f"Path to financial_plan.json (default: {DEFAULT_PLAN_PATH})"
    )
    parser.add_argument(
        "--transcript", type=Path, default=DEFAULT_TRANSCRIPT_PATH,
        help=f"Path to coordinator-transcript.txt (default: {DEFAULT_TRANSCRIPT_PATH})"
    )
    parser.add_argument(
        "--out", type=Path, default=None,
        help="Write JSON to this file instead of stdout"
    )
    args = parser.parse_args()

    plan = load_plan(args.plan)
    transcript = load_transcript(args.transcript)

    warnings = validate_basic(plan)
    if warnings:
        sys.stderr.write("VALIDATION WARNINGS (fix before adding to dashboard):\n")
        for w in warnings:
            sys.stderr.write(f"  ⚠  {w}\n")
        sys.stderr.write("\n")

    case = build_case(plan, transcript)
    output = json.dumps(case, indent=2, ensure_ascii=False)

    if args.out:
        args.out.write_text(output, encoding="utf-8")
        sys.stderr.write(f"Case written to: {args.out}\n")
        sys.stderr.write(
            f"Next: open dashboard/cases.js, append the object to window.CASES, "
            f"and set a unique 'id' value.\n"
        )
    else:
        print(output)
        sys.stderr.write(
            "\nNext steps:\n"
            "  1. Copy the JSON above.\n"
            "  2. Open dashboard/cases.js.\n"
            "  3. Append the object to the window.CASES array.\n"
            "  4. Set a unique 'id' field (e.g. 'sharma-2026-07').\n"
            "  5. Fill in any [Placeholder] strings in the internal section.\n"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
