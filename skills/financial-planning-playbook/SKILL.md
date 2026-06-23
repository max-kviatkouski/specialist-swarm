---
name: financial-planning-playbook
description: Synthetic goal-based financial planning rules. Use whenever assessing retirement readiness, goal funding gaps, savings rate, emergency reserves, or a financial-wellbeing score. Covers the planning math and the wellbeing rubric. Trigger on any request to plan for goals, check retirement readiness, or score financial health.
---

# Financial Planning Playbook

> FICTIONAL demo content for a hackathon. Not financial advice.

## Emergency reserve

3 months of spend if dual stable income; 6 months if single income or variable pay.
Above that = investable, not "cash buffer."

## Savings rate

| Combined savings rate | Reading |
| --- | --- |
| < 10% | Off track |
| 10–19% | Adequate |
| ≥ 20% | Strong |

Closing a retirement gap: **raise the savings rate before raising portfolio risk.** Max
tax-advantaged space first (401(k) to match, then max; HSA; backdoor Roth if eligible).

## Retirement readiness

- Sustainable withdrawal ≈ **4%/yr** of the balance at retirement (inflation-adjusted).
- Required nest egg ≈ **annual retirement spend ÷ 0.04** (i.e. × 25).
- "Funded %" = projected median balance at the target year ÷ required nest egg.
- onTrack = funded ≥ 90%. Report the dollar gap, not just a flag.

## Goal funding

For each goal: targetAmount, targetYear, current funding, and contribution needed.
- Goals **< 5 years out** belong in short-duration bonds/cash, NOT equities.
- When goals collide (retirement + college + home draw the same pool), sequence by
  hard deadline and tax treatment; surface the collision explicitly.

## Financial wellbeing score (0–100)

Start at 60. Adjust:
- Savings rate ≥ 20%: **+15** · 10–19%: **+5** · < 10%: **−15**
- Emergency reserve funded: **+10** (else **−10**)
- All goals on track: **+15** · some gaps: **0** · major gaps: **−10**
- Single-stock concentration > 10%: **−10** · cash drag > 8%: **−5**
Clamp to [0,100]. Band: <40 At Risk · 40–69 On Track — with gaps · 70–100 Healthy.

## Output expectations

Return: the wellbeing score + drivers, retirement funded % + dollar gap, and per-goal
funding status with a concrete contribution recommendation.
