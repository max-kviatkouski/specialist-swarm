---
name: asset-allocation-playbook
description: Synthetic wealth-management asset-allocation rules. Use whenever recommending a target portfolio, analyzing a current portfolio, or flagging concentration/cash drag. Covers model portfolios by risk band, concentration limits, rebalancing, and cash policy. Trigger on any request to propose or review an investment allocation.
---

# Asset Allocation Playbook

> FICTIONAL demo content for a hackathon. Not investment advice.

## Model portfolios (target weights by risk band)

| Asset class | Conservative | Moderate | Moderate Growth | Growth | Aggressive |
| --- | --- | --- | --- | --- | --- |
| US Equity | 20% | 28% | 33% | 40% | 50% |
| International Equity | 10% | 14% | 17% | 20% | 25% |
| Bonds | 50% | 38% | 25% | 15% | 5% |
| Alternatives / Real assets | 5% | 8% | 10% | 12% | 12% |
| Cash | 15% | 12% | 5% | 3% | 3% |
| (single-stock / concentrated) | 0% | ≤10% | ≤10% | ≤15% | ≤15% |

Pick the band from the Risk Profiler's output. When capacity and tolerance disagree,
anchor to the **lower** band and reduce risk via diversification, not by going to cash.

## Concentration limits (hard rules)

- **No single stock above 10%** of total investable assets for any band ≤ Growth.
- A position above the limit is the **#1 risk to flag** — name it explicitly.
- Reduce concentrated positions on a **fixed, tax-aware schedule** (e.g. 25% per quarter),
  never by market-timing. Use specific-lot selection to manage capital gains.

## Cash policy

- Target cash = emergency reserve (3–6 months of spend) + near-term goal funding only.
- Anything above that is **cash drag** — flag it and redeploy into the target mix.

## Rebalancing

- Rebalance when any asset class drifts > 5 percentage points from target, or annually.
- Prefer rebalancing with new contributions and dividends before selling (tax efficiency).

## Output expectations

When you analyze a portfolio, return: (1) current allocation with $ and %, (2) the recommended
target by band, (3) the 2–4 highest-impact changes (concentration, cash drag, missing diversifiers),
each with a concrete action. Be specific about numbers.
