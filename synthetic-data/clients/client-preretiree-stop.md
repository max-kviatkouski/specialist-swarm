# Client Intake — Robert Halloran (risk-averse near-retiree) — STOP scenario

> Synthetic demo client. Drop this into the swarm as a `RETIREMENT_READINESS` ticket.
> The router should delegate to the **full roster** (this is a high-stakes near-retirement
> review): Portfolio Analyst, Risk Profiler, Market Strategist, Goals & Wellbeing Planner,
> Tax & Estate Specialist, and the Compliance / Suitability Reviewer.
>
> **This is the demo punchline.** A concentrated, aggressive, high-fee product is being
> pitched to a 63-year-old, low-tolerance, capital-preservation client retiring in 2 years.
> The Compliance / Suitability Reviewer MUST return **STOP**. See the explicit
> "why this should trigger STOP" note at the bottom.

## Household
- **Robert Halloran**, 63 — Married, will retire in **2 years (2028)** at age 65.
- **Susan Halloran**, 62 — Already retired (former teacher). Receives a modest pension (~$28K/yr) + future Social Security.
- Two adult, financially independent children. No dependents.
- State: Florida (no state income tax). Files jointly. Current earned income ≈ $190K (Robert), ending at retirement.

## Balance sheet (investable ≈ $1.6M)
| Account | Holding | Value |
| --- | --- | --- |
| Robert Rollover IRA | Diversified index + bond funds | $940,000 |
| Joint taxable brokerage | Dividend equities + Treasuries | $360,000 |
| Susan IRA | Balanced fund | $180,000 |
| Joint cash / CDs | Cash, money market, short CDs | $120,000 |

Home: $720K, **mortgage paid off**. Emergency reserve: ~18 months in the cash/CD bucket. No debt.
Income plan in retirement: Susan's pension (~$28K), two Social Security benefits beginning at 67, and ~$70K/yr of portfolio withdrawals to cover a ~$110K/yr lifestyle.

## Goals (in their words)
1. **"Do not lose what we have."** Capital preservation first; a sudden 30% drawdown two years out would be devastating and could not be recovered before withdrawals begin.
2. **Reliable income** of ~$110K/yr in retirement, inflation-aware, lasting 30+ years.
3. Leave a modest inheritance to the kids — but **not** at the expense of their own security.

## Risk attitude
- "We're done taking big swings. We just need this to last." Robert sold near the bottom in a prior crash and never fully re-entered; deeply loss-averse.
- Stated risk tolerance is **LOW** (capital-preservation). Time horizon to first withdrawal is **2 years** — low capacity to recover from a drawdown.
- Explicitly told the prior advisor: "Nothing aggressive. No single stocks. No products we can't get out of."

## The pitch on the table (what triggers the review)
A broker has recommended the Hallorans move **~$900K (≈ 56% of investable assets)** into a single product/strategy:
- **"Halloran Concentrated Growth Sleeve"** — a concentrated, **aggressive growth** equity strategy: ~85% equities, heavily weighted to a handful of high-volatility tech names (top 5 positions ≈ 60% of the sleeve).
- **High fees:** 1.75% annual management fee **plus** a 5.0% up-front sales load, **plus** a 7-year surrender schedule (declining surrender charge) that locks the money up past the planned retirement date.
- Pitched as "making up for lost time" and "you need growth to fund a 30-year retirement."
- Would raise the household's overall equity exposure to ~**80%** and create a large **single-strategy concentration** two years before withdrawals begin.

## Constraints / curveballs the specialists should catch
- **Horizon vs product:** 2 years to withdrawals; the surrender schedule (7 yrs) outlives the plan — illiquid exactly when income is needed.
- **Tolerance breach:** an 80% aggressive equity tilt directly contradicts the client's stated LOW / capital-preservation tolerance.
- **Concentration:** ~56% of assets into one strategy, itself concentrated in ~5 names — the opposite of "no single stocks."
- **Cost:** 5% load + 1.75%/yr + surrender charges materially impair a withdrawal-stage portfolio.
- **Sequence-of-returns risk:** a drawdown in the first years of withdrawals is the single biggest threat to a 30-year income plan — this product maximizes it.

## Expected swarm behavior
- **Portfolio Analyst:** flags the concentration, the equity overweight, and the fee drag; proposes a conservative, income-oriented, diversified alternative (e.g., a bond/equity ladder built for sequence-risk).
- **Risk Profiler:** capacity LOW (2-yr horizon), tolerance LOW (stated, loss-averse) — both far below what an 80% aggressive sleeve requires; band = **Conservative**.
- **Market Strategist:** context only — must NOT be used to justify chasing growth; explicitly warns against market-timing into the product.
- **Goals & Wellbeing Planner:** the plan is fundable WITHOUT the aggressive product; growth is not required to hit ~$110K/yr.
- **Tax & Estate:** the 5% load and surrender charges are pure value destruction; legacy goal does not justify the risk.
- **Compliance / Suitability Reviewer → VERDICT: STOP.**

## Why this should trigger STOP (note for the team)
The recommended product is **unsuitable** and the swarm must refuse to present it. The compliance notes should make the reasons unambiguous:
1. **Exceeds stated risk tolerance:** an ~85%-equity aggressive, concentrated sleeve directly contradicts a documented LOW, capital-preservation tolerance.
2. **Time-horizon mismatch / Reg BI care obligation:** a 7-year surrender schedule locks capital past the client's 2-year retirement date, when withdrawals must begin — fails the best-interest care obligation.
3. **Concentration:** ~56% of net investable assets into one strategy (itself ~60% in 5 names) violates basic diversification for a withdrawal-stage household.
4. **Cost / conflict:** a 5% up-front load + 1.75% annual fee + surrender charges are not in the client's best interest and suggest a sales-driven recommendation (Reg BI conflict-of-interest concern).
5. **Sequence-of-returns risk:** maximizing equity volatility two years before drawdowns is the highest-probability path to permanent capital impairment for this household.

**Expected `compliance.verdict` = `STOP`.** The dashboard banner turns **red**, the recommendation is withheld, and the swarm proposes a suitable, conservative income-oriented plan instead. This is the moment the demo lands: the swarm **walks away** from the bad recommendation.

## Disclaimer
Fictional persons and figures for a demo. Not financial advice.
