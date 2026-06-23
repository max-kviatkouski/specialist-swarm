// dashboard/cases.js
// window.CASES is an array of case objects consumed by index.html.
// Shape: { id, ...all financial_plan.json fields..., internal: { dialog, riskFlags, talkingPoints, complianceReasoning } }
// This file contains 3 synthetic demo cases.  Real cases can be appended via build_cases.py.

window.CASES = [
  // ── Case 1: Sharma household ────────────────────────────────────────────────
  // Plan fields are VERBATIM from synthetic-data/sample-plan.json.
  // internal section is authored to be consistent with the plan.
  {
    id: "sharma",
    generatedFor: "Anand & Priya Sharma",
    asOf: "2026-06-23",
    advisor: "Senior Wealth Advisor — AI Wealth Advisory Swarm",
    ticketType: "NEW_CLIENT_PLAN",
    routedSpecialists: [
      "Portfolio Analyst",
      "Risk Profiler",
      "Market Strategist",
      "Goals & Wellbeing Planner",
      "Tax & Estate Specialist",
      "Compliance Reviewer"
    ],
    executiveSummary: [
      "Strong savers with a healthy $1.25M base, but 34% of the portfolio sits in a single employer stock — the dominant risk to the whole plan.",
      "Retirement at 60 is reachable but currently ~$1.1M short on the median path; closing the gap needs a higher pre-tax savings rate, not more risk.",
      "$125K (10%) in cash is a drag; redeploying most of it and trimming the concentrated position funds both diversification and the college/vacation-home goals.",
      "Recommended path keeps the household at a Moderate Growth risk band — suitable for their 14-year horizon and stated comfort level."
    ],
    financialWellbeing: {
      score: 72,
      band: "On Track — with funding gaps",
      drivers: [
        "+ High, stable dual income and a 24% savings rate",
        "+ Fully funded 6-month emergency reserve",
        "− Single-stock concentration (34%) and cash drag (10%)",
        "− Retirement and college goals under-funded on the current path"
      ]
    },
    riskProfile: {
      capacityScore: 75,
      toleranceScore: 58,
      band: "Moderate Growth",
      rationale: "High capacity (long horizon, secure dual income, large reserve) but only moderate stated tolerance after a prior market scare. We anchor the plan to the lower of the two — Moderate Growth — and reduce risk via diversification rather than de-risking the equity weight."
    },
    allocation: {
      current: [
        { assetClass: "US Equity", percent: 30, value: 375000 },
        { assetClass: "Employer Stock (concentrated)", percent: 34, value: 425000 },
        { assetClass: "International Equity", percent: 8, value: 100000 },
        { assetClass: "Bonds", percent: 14, value: 175000 },
        { assetClass: "Cash", percent: 10, value: 125000 },
        { assetClass: "Alternatives / Other", percent: 4, value: 50000 }
      ],
      target: [
        { assetClass: "US Equity", percent: 33 },
        { assetClass: "Employer Stock (concentrated)", percent: 10 },
        { assetClass: "International Equity", percent: 17 },
        { assetClass: "Bonds", percent: 25 },
        { assetClass: "Cash", percent: 5 },
        { assetClass: "Alternatives / Other", percent: 10 }
      ],
      keyChanges: [
        "Reduce employer stock from 34% to 10% over 4 quarters using tax-aware lot selection to limit capital-gains drag.",
        "Lift international equity 8% → 17% and bonds 14% → 25% to diversify the de-concentrated proceeds.",
        "Cut cash 10% → 5%, redeploying ~$60K into the target mix."
      ]
    },
    goals: [
      {
        name: "Retirement at age 60",
        targetYear: 2040,
        targetAmount: 4500000,
        fundedPercent: 68,
        onTrack: false,
        gap: "~$1.1M projected shortfall on the median path at the current savings rate.",
        recommendation: "Max both 401(k)s pre-tax and add a backdoor Roth; raises the funded path to ~90% without increasing portfolio risk."
      },
      {
        name: "College — elder child",
        targetYear: 2032,
        targetAmount: 250000,
        fundedPercent: 42,
        onTrack: false,
        gap: "529 balance covers ~2 of 4 years at current contributions.",
        recommendation: "Increase 529 funding by $1,200/mo; front-load using part of the cash drag."
      },
      {
        name: "Vacation home down payment",
        targetYear: 2034,
        targetAmount: 200000,
        fundedPercent: 25,
        onTrack: true,
        gap: "On track if employer-stock proceeds are partly earmarked here.",
        recommendation: "Hold this bucket in short-duration bonds, not equities, given the fixed 8-year horizon."
      }
    ],
    marketContext: {
      summary: "Mid-2026 backdrop: rate-cut expectations have steadied bond yields, large-cap US valuations remain elevated and concentrated in mega-cap tech, and international equities trade at a meaningful valuation discount. This reinforces (not drives) the plan's tilt away from a single US tech name and toward international and bonds.",
      asOf: "2026-06-23",
      sources: [
        "[populated live by the Market Strategist's web_search — example placeholders]",
        "https://www.federalreserve.gov/",
        "https://www.spglobal.com/spdji/"
      ],
      tacticalTilts: [
        "Modest overweight to international developed equity within the target band.",
        "Extend bond duration slightly to lock current yields ahead of expected cuts.",
        "Do NOT time the exit of the employer stock on a market view — exit on a fixed, tax-aware schedule."
      ]
    },
    projections: {
      assumptions: "6.2% nominal expected return at the target allocation, 2.4% inflation, $90K/yr combined contributions rising 3%/yr, retirement spend $180K/yr from 2040. Bands show 10th / 50th / 90th percentile outcomes.",
      series: [
        { year: 2026, age: 46, low: 1250000, mid: 1250000, high: 1250000 },
        { year: 2028, age: 48, low: 1360000, mid: 1455000, high: 1560000 },
        { year: 2030, age: 50, low: 1510000, mid: 1720000, high: 1960000 },
        { year: 2032, age: 52, low: 1650000, mid: 2010000, high: 2460000 },
        { year: 2035, age: 55, low: 1900000, mid: 2520000, high: 3250000 },
        { year: 2040, age: 60, low: 2600000, mid: 3580000, high: 5050000 },
        { year: 2050, age: 70, low: 2380000, mid: 4180000, high: 7050000 },
        { year: 2060, age: 80, low: 1780000, mid: 3820000, high: 8100000 }
      ]
    },
    recommendations: [
      { id: "R1", title: "De-risk the concentrated employer stock", detail: "Sell down 34% → 10% across 4 quarters with tax-aware lot selection; this is the single highest-impact action in the plan.", priority: "high", owner: "Portfolio Analyst" },
      { id: "R2", title: "Put the cash to work", detail: "Redeploy ~$60K of the $125K cash into international equity and bonds per the target mix; keep ~$65K as the emergency reserve.", priority: "high", owner: "Portfolio Analyst" },
      { id: "R3", title: "Close the retirement gap with pre-tax savings", detail: "Max both 401(k)s and add a backdoor Roth; lifts the median retirement path from 68% to ~90% funded without raising risk.", priority: "high", owner: "Goals & Wellbeing Planner" },
      { id: "R4", title: "Front-load the 529", detail: "+$1,200/mo to the elder child's 529, partly funded from the cash drag, to close the 2-year coverage gap.", priority: "medium", owner: "Goals & Wellbeing Planner" },
      { id: "R5", title: "Tax-aware sequencing", detail: "Place bonds in tax-deferred accounts and the de-concentrated equity in taxable to improve after-tax return; harvest losses opportunistically.", priority: "medium", owner: "Tax & Estate Specialist" }
    ],
    compliance: {
      verdict: "APPROVED",
      reviewer: "Compliance / Suitability Reviewer",
      notes: [
        "Recommended allocation is consistent with the household's Moderate Growth profile and 14-year horizon.",
        "No product recommendation exceeds the client's stated risk tolerance.",
        "Concentration-reduction plan is tax-aware and time-phased, not market-timed.",
        "All projections are presented as ranges, not guarantees."
      ]
    },
    disclaimers: "FICTIONAL DEMO — NOT FINANCIAL ADVICE. Generated by an AI multi-agent demo on synthetic data for a hackathon. No real persons, securities, or accounts are referenced. Not a recommendation, solicitation, or offer. Consult a licensed fiduciary advisor before making any financial decision.",
    internal: {
      dialog: [
        {
          specialist: "Portfolio Analyst",
          role: "Portfolio construction & concentration risk",
          message: "The 34% employer-stock position is the dominant risk factor. Using tax-lot analysis, I've identified a phased 4-quarter exit strategy that minimizes cap-gains drag. Proceeds redeploy into international equity (8% → 17%) and bonds (14% → 25%). The $60K cash overhang above the 6-month reserve should also redeploy into the target mix immediately. Proposed target allocation: 33% US Equity, 10% Employer Stock, 17% International, 25% Bonds, 5% Cash, 10% Alts. All percent totals confirm to 100."
        },
        {
          specialist: "Risk Profiler",
          role: "Risk capacity & tolerance assessment",
          message: "Capacity score 75/100: 14-year horizon, dual high income, 6-month reserve are all strong positives. Tolerance score 58/100: self-reported moderate comfort; notably, the household pulled to cash once during a prior selloff and expressed emotional attachment to the employer-stock position — both are tolerance-compressing signals. Appropriate band: Moderate Growth. I recommend anchoring the plan to tolerance (58), not capacity (75), to avoid behavioral risk of a second panic exit."
        },
        {
          specialist: "Market Strategist",
          role: "Macro context & tactical tilts",
          message: "As of June 2026, Fed expectations have stabilized; bond yields have stopped rising. US large-cap (mega-cap tech) valuations are elevated — the S&P 500 P/E is near 22x trailing. International developed equities trade at ~14x — a 35%+ valuation discount. This macro context reinforces the structural case for the de-concentration and international tilt. I explicitly advise against market-timing the employer-stock exit; the schedule should be mechanical and tax-driven."
        },
        {
          specialist: "Goals & Wellbeing Planner",
          role: "Goal gap analysis & wellbeing scoring",
          message: "Retirement at 60: $4.5M target, currently 68% funded on median path — ~$1.1M shortfall. Maxing both 401(k)s pre-tax plus a backdoor Roth raises this to ~90% funded without adding equity risk. College (elder): 529 covers ~2 of 4 years; +$1,200/mo funded from cash drag closes the gap. Vacation home: on track if employer-stock proceeds partially earmarked. Financial wellbeing score: 72 — 'On Track with funding gaps.' Drivers: high income + savings rate positive; concentration + underfunded retirement negative."
        },
        {
          specialist: "Tax & Estate Specialist",
          role: "Tax efficiency & estate considerations",
          message: "The Sharmas are in the 37% federal bracket and California's 13.3% top state rate — combined marginal of ~50%. The employer stock has large embedded gains; selling all at once would trigger a significant one-year tax bill. The phased 4-quarter exit plan optimizes this. For asset location: bonds should sit in 401(k)/IRA (tax-deferred); employer stock exit should occur in the taxable account with strategic lot harvesting. Backdoor Roth is warranted given income level; no direct Roth IRA contributions are permitted."
        },
        {
          specialist: "Compliance Reviewer",
          role: "Suitability review & regulatory sign-off",
          message: "Review complete. The plan recommends a Moderate Growth allocation consistent with the household's lower of capacity/tolerance (58/100). No product pitch is present — the recommendations are diversification, savings-rate increases, and tax-optimization. All projections are presented as probabilistic ranges (10th/50th/90th percentile) with explicit assumptions disclosed. No Reg BI concern. VERDICT: APPROVED. The plan is suitable and may be presented to the client."
        }
      ],
      riskFlags: [
        {
          label: "Single-stock concentration",
          severity: "high",
          detail: "34% of the entire household portfolio is in one employer name. A 50% drawdown in that position — historically common for single tech stocks — would destroy ~17% of total household wealth in a single event. Phased exit is the highest-priority action."
        },
        {
          label: "Cash drag",
          severity: "medium",
          detail: "$125K (10%) sits in money market. After the 6-month emergency reserve (~$65K), approximately $60K is uninvested against a ~6.2% expected target return. Opportunity cost is ~$3,700/year and growing."
        },
        {
          label: "Capacity/tolerance gap",
          severity: "medium",
          detail: "Capacity score 75 vs. tolerance score 58 — a 17-point gap. The prior panic-sell episode and emotional attachment to the employer stock are behavioral indicators that the plan must be tolerance-anchored, not capacity-anchored, to survive volatility."
        }
      ],
      talkingPoints: [
        "Lead with the good news: their savings rate is exceptional and the 14-year runway gives us real flexibility.",
        "Frame the employer-stock reduction as 'protecting what you've built' rather than 'selling what's working' — the emotional anchor is strong.",
        "Use the allocation donut side-by-side to show the red slice (employer stock) shrinking to green — make the visual case.",
        "Be specific about the retirement gap: 'You're 68% of the way there — maxing the 401(k)s gets you to 90% without adding a penny more of risk.'",
        "Acknowledge the tax cost of de-concentration upfront; show that the phased plan keeps the annual tax bill manageable.",
        "On the 529, frame urgency: the elder child starts college in 6 years and every dollar saved now has 6 years of compounding."
      ],
      complianceReasoning: "The plan passes suitability on all five Reg BI axes: (1) Reasonable basis — the Moderate Growth band is supported by the dual-score assessment. (2) Customer specific — allocation anchored to the lower tolerance score (58), not the higher capacity score. (3) Quantitative suitability — no excessive trading; the phased de-concentration is scheduled, not reactive. (4) Conflicts — no proprietary products, no commissions, no incentive conflicts. (5) Disclosure — all projections labeled probabilistic; disclaimers visible. APPROVED."
    }
  },

  // ── Case 2: Maya Chen — young accumulator ───────────────────────────────────
  // PORTFOLIO_REVIEW, 3-specialist subset (board shrinks), APPROVED.
  {
    id: "young-accumulator",
    generatedFor: "Maya Chen",
    asOf: "2026-06-23",
    advisor: "Wealth Advisor — AI Wealth Advisory Swarm",
    ticketType: "PORTFOLIO_REVIEW",
    routedSpecialists: [
      "Portfolio Analyst",
      "Goals & Wellbeing Planner",
      "Compliance / Suitability Reviewer"
    ],
    executiveSummary: [
      "Maya is 28 with $40K invested and a stable $135K income — the fundamentals for long-term wealth-building are in place.",
      "Top priority: build the emergency fund from $6K to $18K before adding investment risk elsewhere.",
      "A simple 3-fund index portfolio (80% equity / 20% bonds) auto-pilot is the right fit — no complex allocation or tax maneuvering needed.",
      "Capturing the full 401(k) employer match (4%) is the highest guaranteed return available; confirm it is being fully utilized."
    ],
    financialWellbeing: {
      score: 64,
      band: "Building — strong foundation, some gaps",
      drivers: [
        "+ Long time horizon (37 years to retirement) and high risk capacity",
        "+ Stable W-2 income, no dependents, tax-advantaged state",
        "− Emergency reserve below target ($6K vs $18K needed)",
        "− Cash sitting idle rather than invested systematically"
      ]
    },
    riskProfile: {
      capacityScore: 88,
      toleranceScore: 82,
      band: "Growth",
      rationale: "High capacity: 37-year horizon, stable income, no dependents, no debt beyond manageable student loans. High tolerance: self-described aggressive, comfortable with full market cycles, no prior loss trauma. Both scores align — Growth band is appropriate. No tension between capacity and willingness here."
    },
    allocation: {
      current: [
        { assetClass: "US Equity", percent: 35, value: 14000 },
        { assetClass: "Bonds", percent: 10, value: 4000 },
        { assetClass: "Cash", percent: 27, value: 11000 },
        { assetClass: "401k / Target Date", percent: 28, value: 11000 }
      ],
      target: [
        { assetClass: "US Equity", percent: 50 },
        { assetClass: "International Equity", percent: 20 },
        { assetClass: "Bonds", percent: 15 },
        { assetClass: "Cash", percent: 5 },
        { assetClass: "401k / Target Date", percent: 10 }
      ],
      keyChanges: [
        "Redirect $500/mo from checking into a high-yield savings account until the emergency fund reaches $18K (~24 months).",
        "After emergency fund is full, systematically invest the $500/mo into a 3-fund index mix (50% US equity, 20% international, 30% bonds/cash).",
        "Confirm 401(k) contribution is at exactly 4% to capture the full employer match — not more, not less, until the emergency fund is funded."
      ]
    },
    goals: [
      {
        name: "Emergency fund ($18K target)",
        targetYear: 2028,
        targetAmount: 18000,
        fundedPercent: 33,
        onTrack: false,
        gap: "$12K below the 3-month minimum target; exposed to unexpected expenses.",
        recommendation: "Redirect $500/mo from the current cash flow to a HYSA until the target is reached (~24 months at current savings pace)."
      },
      {
        name: "Retirement (age 65)",
        targetYear: 2063,
        targetAmount: 2500000,
        fundedPercent: 2,
        onTrack: true,
        gap: "On track given 37-year horizon; compounding does the heavy lifting with consistent contributions.",
        recommendation: "After emergency fund is complete, increase 401(k) contribution toward the annual limit. Add Roth IRA contributions at the max annually."
      }
    ],
    marketContext: {
      summary: "Not applicable for this portfolio review — no Market Strategist was engaged for this simple single-account review. The focus is on savings discipline and account structure, not tactical market positioning.",
      asOf: "2026-06-23",
      sources: [],
      tacticalTilts: []
    },
    projections: {
      assumptions: "7.0% nominal return (Growth allocation), 2.4% inflation, $12K/yr contributions growing 3%/yr. Retirement at 65 in 2063. Bands show 10th/50th/90th percentile over 37-year horizon.",
      series: [
        { year: 2026, age: 28, low: 40000, mid: 40000, high: 40000 },
        { year: 2030, age: 32, low: 58000, mid: 70000, high: 84000 },
        { year: 2035, age: 37, low: 95000, mid: 130000, high: 175000 },
        { year: 2040, age: 42, low: 155000, mid: 230000, high: 330000 },
        { year: 2045, age: 47, low: 235000, mid: 380000, high: 580000 },
        { year: 2050, age: 52, low: 340000, mid: 590000, high: 960000 },
        { year: 2055, age: 57, low: 470000, mid: 890000, high: 1550000 },
        { year: 2063, age: 65, low: 750000, mid: 1680000, high: 3200000 }
      ]
    },
    recommendations: [
      { id: "R1", title: "Build the emergency fund first", detail: "Redirect $500/mo to a HYSA until the $18K target is reached. This is the non-negotiable first step — investing while underinsured against job loss is the wrong order.", priority: "high", owner: "Goals & Wellbeing Planner" },
      { id: "R2", title: "Capture the full 401(k) match", detail: "Confirm contribution is at exactly 4% — the employer match is a guaranteed 100% return on those dollars. Prioritize this over all other investing until the match is fully captured.", priority: "high", owner: "Portfolio Analyst" },
      { id: "R3", title: "Max the Roth IRA annually", detail: "At $135K income (WA, no state tax), there is no barrier to direct Roth IRA contributions. Max the $7K annual limit — tax-free growth over 37 years is the most powerful tool available.", priority: "medium", owner: "Portfolio Analyst" },
      { id: "R4", title: "Adopt a 3-fund index plan", detail: "Replace any active holdings with a 3-fund index approach: 50% US equity (VTI), 20% international (VXUS), 30% bonds/stable (BND). Low fees, broad diversification, no management required.", priority: "medium", owner: "Portfolio Analyst" }
    ],
    compliance: {
      verdict: "APPROVED",
      reviewer: "Compliance / Suitability Reviewer",
      notes: [
        "Recommendations are conservative, index-focused, and fully aligned with the client's Growth risk profile.",
        "No products are pitched — only low-cost index funds and standard account types.",
        "No complex strategies, no tax risk, no suitability concerns.",
        "Plan is simple, proportional, and in the client's best interest."
      ]
    },
    disclaimers: "FICTIONAL DEMO — NOT FINANCIAL ADVICE. Generated by an AI multi-agent demo on synthetic data for a hackathon. No real persons, securities, or accounts are referenced. Not a recommendation, solicitation, or offer. Consult a licensed fiduciary advisor before making any financial decision.",
    internal: {
      dialog: [
        {
          specialist: "Portfolio Analyst",
          role: "Portfolio construction & fund selection",
          message: "Maya's situation is simple and the right answer is simple: a 3-fund index portfolio. Current allocation is fragmented across a target-date fund, an S&P 500 fund, and idle cash — the target-date fund in the 401(k) is fine; the taxable account and Roth IRA should consolidate to VTI + VXUS + BND (or equivalent). The key action is increasing systematic investment after the emergency fund is funded. 401(k) match must be fully captured first — it's the highest guaranteed return in the plan."
        },
        {
          specialist: "Goals & Wellbeing Planner",
          role: "Goal gap analysis & wellbeing scoring",
          message: "Two goals identified: emergency fund and retirement. Emergency fund is 33% funded — the gap ($12K) represents genuine risk; a job loss before this is resolved would force liquidating investments at potentially poor timing. Retirement is on track given the 37-year runway, but contributions need to increase systematically after emergency fund completion. Wellbeing score: 64 — 'Building.' The score is lower due to the reserve gap, not structural problems. This household is on a good trajectory."
        },
        {
          specialist: "Compliance / Suitability Reviewer",
          role: "Suitability & regulatory sign-off",
          message: "Clean review. No product recommendation, no complex strategy, no suitability tension. Recommendations are entirely standard: fund the emergency reserve, capture the employer match, max a Roth IRA, use index funds. Growth band is supported by both capacity (88) and tolerance (82) scores. No Reg BI concerns. VERDICT: APPROVED."
        }
      ],
      riskFlags: [
        {
          label: "Thin emergency reserve",
          severity: "medium",
          detail: "Only $6K cash against a $18K target (3-6 months of ~$3,500/mo expenses). An unexpected expense or job disruption could force unplanned liquidation of investments, potentially at a loss."
        },
        {
          label: "Idle cash / uninvested deposits",
          severity: "low",
          detail: "Cash is sitting in a standard checking account earning near-zero rather than being invested systematically. Opportunity cost is modest at this portfolio size but the habit of non-investment is the real risk."
        }
      ],
      talkingPoints: [
        "Start with what's going well: she's 28, investing, has a Roth IRA, and earns well — she's ahead of the majority of her peers.",
        "Frame the emergency fund as 'unlocking' more investment, not 'delaying' it — once it's funded, she can invest the $500/mo without hesitation.",
        "The 401(k) match story is simple: 'Your employer is offering you a 100% return on part of your money — we should definitely take all of that.'",
        "Keep the investment plan simple and repeatable — three funds, auto-invest, forget it for 37 years. The complexity can come later if she wants it."
      ],
      complianceReasoning: "Simple, standard portfolio review with no products recommended. The plan is composed entirely of low-cost index funds and standard tax-advantaged accounts. Capacity (88) and tolerance (82) are both high and aligned — no tension. Growth band is well-supported. No Reg BI concerns whatsoever. APPROVED without reservation."
    }
  },

  // ── Case 3: Robert Halloran — pre-retiree STOP ──────────────────────────────
  // RETIREMENT_READINESS, full roster, compliance.verdict = STOP.
  {
    id: "preretiree-stop",
    generatedFor: "Robert & Susan Halloran",
    asOf: "2026-06-23",
    advisor: "Senior Wealth Advisor — AI Wealth Advisory Swarm",
    ticketType: "RETIREMENT_READINESS",
    routedSpecialists: [
      "Portfolio Analyst",
      "Risk Profiler",
      "Market Strategist",
      "Goals & Wellbeing Planner",
      "Tax & Estate Specialist",
      "Compliance / Suitability Reviewer"
    ],
    executiveSummary: [
      "COMPLIANCE STOP: The recommended 'Halloran Concentrated Growth Sleeve' is unsuitable and the swarm refuses to present it — it directly contradicts the Hallorans' documented capital-preservation mandate and fails Reg BI best-interest obligations.",
      "The Hallorans have $1.6M in investable assets and are 2 years from retirement — their income need (~$110K/yr) is fully fundable WITHOUT the aggressive product; growth-chasing is not required.",
      "The pitched product combines a 7-year surrender schedule (outlasting their retirement date), a 5% up-front load, 1.75%/yr in ongoing fees, ~80% equity exposure, and ~56% single-strategy concentration — each element alone is problematic; together they represent a textbook suitability failure.",
      "The swarm proposes an alternative: a conservative income-oriented ladder (30% equity / 65% bonds-cash / 5% alts) aligned with a Conservative risk band, low fees, and full liquidity by the 2028 retirement date."
    ],
    financialWellbeing: {
      score: 71,
      band: "Retirement-Ready — with income risk if unsuitable product adopted",
      drivers: [
        "+ $1.6M investable assets, mortgage paid off, no debt",
        "+ Susan's pension + two Social Security benefits provide a reliable income base",
        "− Proposed product would raise sequence-of-returns risk to critical levels two years before withdrawals begin",
        "− 7-year surrender schedule would lock capital past retirement date, eliminating liquidity when income is needed"
      ]
    },
    riskProfile: {
      capacityScore: 22,
      toleranceScore: 15,
      band: "Conservative",
      rationale: "Capacity score 22/100: 2-year horizon to first withdrawals, no earned income after retirement, full dependency on portfolio for ~$70K/yr drawdowns — effectively zero capacity to absorb a significant drawdown and recover before withdrawals begin. Tolerance score 15/100: self-described capital-preservation, deeply loss-averse, sold near the bottom in a prior crash and never re-entered, explicitly stated 'nothing aggressive, no single stocks, no products we can't get out of.' Both scores are far below what an 80% aggressive equity strategy requires. Conservative band is the only appropriate classification."
    },
    allocation: {
      current: [
        { assetClass: "US Equity", percent: 35, value: 560000 },
        { assetClass: "International Equity", percent: 8, value: 128000 },
        { assetClass: "Bonds", percent: 38, value: 608000 },
        { assetClass: "Cash / CDs", percent: 12, value: 192000 },
        { assetClass: "Alternatives / Other", percent: 7, value: 112000 }
      ],
      target: [
        { assetClass: "US Equity", percent: 20 },
        { assetClass: "International Equity", percent: 10 },
        { assetClass: "Bonds", percent: 45 },
        { assetClass: "Cash / CDs", percent: 20 },
        { assetClass: "Alternatives / Other", percent: 5 }
      ],
      keyChanges: [
        "REJECT the pitched product — the proposed 56% shift into an aggressive concentrated sleeve is refused as unsuitable.",
        "Reduce total equity from 43% to 30% to match the Conservative risk band required for a 2-year horizon.",
        "Build a 2-year income ladder in CDs/short-duration bonds to fund the $70K/yr portfolio drawdown from day one of retirement.",
        "Hold the bond allocation in diversified investment-grade securities with staggered maturities — no single-strategy concentration."
      ]
    },
    goals: [
      {
        name: "Retirement income ($110K/yr for 30+ years)",
        targetYear: 2028,
        targetAmount: 2200000,
        fundedPercent: 73,
        onTrack: true,
        gap: "On track with a conservative allocation; the income target is achievable without aggressive growth.",
        recommendation: "Build a floor income stream from Social Security + pension; cover the $70K/yr portfolio gap with a conservative bond/equity ladder. Do not chase growth — the plan is fundable as-is."
      },
      {
        name: "Legacy / inheritance",
        targetYear: 2045,
        targetAmount: 500000,
        fundedPercent: 85,
        onTrack: true,
        gap: "Modest legacy goal is achievable on conservative returns without any product changes.",
        recommendation: "Leave the growth equity allocation at 30% — this provides sufficient long-term appreciation to support the legacy goal while preserving capital."
      }
    ],
    marketContext: {
      summary: "Mid-2026: bond yields have stabilized following Fed rate expectations. For near-retirees, the current yield environment is constructive — investment-grade bonds at 4.5–5% yields provide the income floor this household needs without chasing equity risk. The Market Strategist explicitly advises against using macro optimism to justify the pitched aggressive product; the Hallorans' horizon and tolerance disqualify them from equity overweights regardless of market conditions.",
      asOf: "2026-06-23",
      sources: [
        "https://www.federalreserve.gov/",
        "https://www.treasurydirect.gov/",
        "https://www.sec.gov/investor/pubs/regreview.htm"
      ],
      tacticalTilts: [
        "For this household: income-ladder positioning, NOT tactical equity exposure.",
        "Current bond yields (4.5–5%) support locking in the income floor for 2028 retirement — act now while yields are favorable.",
        "No tactical market calls should be used to justify the pitched growth product; the household's documented tolerance overrides any macro view."
      ]
    },
    projections: {
      assumptions: "4.2% nominal return (Conservative allocation), 2.4% inflation, $48K/yr contributions in 2026–2028, then $70K/yr portfolio withdrawals from 2028 onward. Susan's pension $28K/yr + combined Social Security ~$48K/yr from 2029 assumed. Bands show 10th/50th/90th percentile. NOTE: projections shown are for the SUITABLE conservative alternative — not the unsuitable pitched product.",
      series: [
        { year: 2026, age: 63, low: 1600000, mid: 1600000, high: 1600000 },
        { year: 2027, age: 64, low: 1630000, mid: 1660000, high: 1695000 },
        { year: 2028, age: 65, low: 1620000, mid: 1680000, high: 1745000 },
        { year: 2030, age: 67, low: 1560000, mid: 1660000, high: 1775000 },
        { year: 2035, age: 72, low: 1380000, mid: 1580000, high: 1820000 },
        { year: 2040, age: 77, low: 1180000, mid: 1480000, high: 1840000 },
        { year: 2050, age: 87, low: 780000, mid: 1240000, high: 1800000 },
        { year: 2056, age: 93, low: 540000, mid: 1040000, high: 1700000 }
      ]
    },
    recommendations: [
      { id: "R1", title: "REFUSE the pitched concentrated growth product", detail: "The 'Halloran Concentrated Growth Sleeve' is unsuitable on every axis: tolerance (LOW vs 80% equity), capacity (2-yr horizon vs 7-yr surrender), concentration (56% single-strategy), and cost (5% load + 1.75%/yr + surrender charges). This recommendation is withheld.", priority: "high", owner: "Compliance / Suitability Reviewer" },
      { id: "R2", title: "Build a 2-year income ladder immediately", detail: "Lock in current 4.5–5% yields: construct a CD/short-duration bond ladder covering $140K (2 years of the $70K/yr drawdown need) before retirement date. This eliminates sequence-of-returns risk for the critical early years.", priority: "high", owner: "Portfolio Analyst" },
      { id: "R3", title: "Reduce total equity to 30% (Conservative band)", detail: "Current 43% equity allocation slightly exceeds Conservative band for a 2-year horizon. Shift 13 percentage points from equity into bonds/CDs over the next 18 months — not all at once, to avoid disrupting the existing bond portfolio structure.", priority: "high", owner: "Portfolio Analyst" },
      { id: "R4", title: "Optimize Social Security timing", detail: "Delaying Robert's Social Security to age 70 (2033) increases the benefit by ~32% and strengthens the inflation-adjusted income floor. Model the breakeven against the 2028 option; for a 30-year plan, delay almost certainly wins.", priority: "medium", owner: "Goals & Wellbeing Planner" },
      { id: "R5", title: "Tax-efficient withdrawal sequencing", detail: "Draw down the taxable brokerage first (2028–2032), then the IRA/rollover IRA (2032+), allowing the tax-deferred accounts to compound longer. Roth conversions in 2026–2027 may reduce future RMDs — model the bracket window with the estate attorney.", priority: "medium", owner: "Tax & Estate Specialist" }
    ],
    compliance: {
      verdict: "STOP",
      reviewer: "Compliance / Suitability Reviewer",
      notes: [
        "STOP — UNSUITABLE UNDER REG BI: The recommended 'Halloran Concentrated Growth Sleeve' fails the best-interest standard on all five suitability axes.",
        "Tolerance breach: client documents a capital-preservation, LOW-tolerance mandate; the product requires bearing 80% equity risk — a direct and documented contradiction.",
        "Time-horizon / liquidity mismatch: the 7-year surrender schedule extends past the client's 2028 retirement date; withdrawals cannot begin on schedule without triggering surrender charges.",
        "Concentration risk: 56% of investable assets into a single strategy (itself ~60% in 5 names) creates exactly the single-name / single-strategy concentration the client explicitly ruled out.",
        "Cost impairment: a 5% up-front load plus 1.75%/yr ongoing fees plus surrender charges represent material value destruction in a withdrawal-stage portfolio — not in the client's best interest.",
        "Sequence-of-returns risk: maximizing equity volatility 2 years before withdrawals begin is the highest-probability path to permanent capital impairment for this household.",
        "This plan will NOT be presented to the client in its current form. A suitable conservative income-oriented alternative has been prepared instead."
      ]
    },
    disclaimers: "FICTIONAL DEMO — NOT FINANCIAL ADVICE. Generated by an AI multi-agent demo on synthetic data for a hackathon. No real persons, securities, or accounts are referenced. Not a recommendation, solicitation, or offer. Consult a licensed fiduciary advisor before making any financial decision.",
    internal: {
      dialog: [
        {
          specialist: "Portfolio Analyst",
          role: "Portfolio construction & product evaluation",
          message: "I've reviewed the pitched 'Halloran Concentrated Growth Sleeve.' The proposal asks us to move $900K (~56% of investable assets) into a strategy that is ~85% equity, top-5 names account for ~60% of the sleeve, carries a 7-year surrender schedule, a 5% up-front load, and 1.75%/yr ongoing fees. This is disqualifying on portfolio grounds alone: concentration risk, illiquidity past the retirement date, and fee drag that materially impairs withdrawal-stage returns. I recommend a conservative income ladder as the alternative: 30% equity (diversified index), 45% bonds (staggered investment-grade), 20% cash/CDs (income ladder for 2028 drawdowns), 5% alternatives."
        },
        {
          specialist: "Risk Profiler",
          role: "Risk capacity & tolerance assessment",
          message: "Capacity score: 22/100. With first withdrawals in 24 months, there is virtually no time to recover from a drawdown before income must be taken. A 30% market decline (fully possible in 2 years) would reduce the portfolio by ~$460K at the proposed 80% equity weight — that loss is unrecoverable before retirement. Tolerance score: 15/100. The client has documented their tolerance explicitly: 'capital preservation first, nothing aggressive, no products we can't get out of.' The proposed product requires a tolerance score of at least 75. The gap is 60 points. Both scores independently mandate a Conservative band. I am flagging this for a mandatory Compliance STOP."
        },
        {
          specialist: "Market Strategist",
          role: "Macro context — income positioning",
          message: "Mid-2026 bond yields (4.5–5% on investment-grade) provide the income floor the Hallorans need without requiring equity risk. I want to be explicit: the current macro environment does NOT justify recommending an aggressive concentrated equity product to a capital-preservation near-retiree. The argument that 'they need growth to fund a 30-year retirement' is mathematically false — their income floor is covered by Social Security + pension + a 4–4.5% withdrawal rate on a conservative allocation. This plan does not require the pitched product under any reasonable market scenario."
        },
        {
          specialist: "Goals & Wellbeing Planner",
          role: "Goal viability & wellbeing assessment",
          message: "The income goal ($110K/yr for 30+ years) is fundable WITHOUT the pitched product. Susan's pension ($28K/yr) + combined Social Security (~$48K/yr from age 67) provides ~$76K of the floor. The remaining $34K–$70K annual gap (before Social Security starts) is covered by conservative portfolio withdrawals of ~4–4.5% on a $1.6M base. The portfolio does not need to grow aggressively to meet this need — it needs to survive. Wellbeing score: 71. The main risk to wellbeing is not insufficient returns; it is the adoption of an unsuitable product that introduces the sequence-of-returns catastrophe the client explicitly wanted to avoid."
        },
        {
          specialist: "Tax & Estate Specialist",
          role: "Tax analysis & estate planning",
          message: "The 5% up-front load on $900K = $45,000 of immediate, irrecoverable value destruction. At a 4.5% net return, it takes over a year of investment returns just to recover the load — before counting the 1.75%/yr ongoing drag. The surrender schedule (7 years) runs to 2033 — the withdrawal strategy requires portfolio access from 2028. Early surrenders in 2028–2032 would trigger surrender charges of 3–6% depending on schedule terms. I recommend the RIA-based, fee-transparent conservative alternative, with a Roth conversion strategy in 2026–2027 to reduce future RMDs from the rollover IRA. There is no tax argument that justifies the pitched product."
        },
        {
          specialist: "Compliance / Suitability Reviewer",
          role: "Suitability review & regulatory compliance",
          message: "VERDICT: STOP. The recommended 'Halloran Concentrated Growth Sleeve' is unsuitable and may not be presented to the client. Grounds: (1) Tolerance breach — LOW/capital-preservation mandate vs. 80% aggressive equity; (2) Illiquidity mismatch — 7-year surrender schedule past 2-year retirement date; (3) Concentration — 56% single-strategy, ~60% top-5 names; (4) Cost — 5% load + 1.75%/yr + surrender charges not in client's best interest under Reg BI; (5) Sequence-of-returns risk — maximum equity volatility 2 years before drawdowns. I am withholding this plan. A suitable conservative alternative has been prepared and may be presented instead."
        }
      ],
      riskFlags: [
        {
          label: "Unsuitable product — compliance STOP",
          severity: "high",
          detail: "The 'Halloran Concentrated Growth Sleeve' fails suitability on all five Reg BI axes. The plan as pitched will NOT be presented to the client. See compliance notes for full breakdown."
        },
        {
          label: "Sequence-of-returns risk (critical)",
          severity: "high",
          detail: "Maximizing equity volatility 2 years before mandatory withdrawals begin is the primary path to permanent capital impairment for a 30-year income plan. A 30% drawdown at 80% equity = $384K loss at the proposed allocation — unrecoverable before withdrawals start."
        },
        {
          label: "Illiquidity trap — 7-year surrender schedule",
          severity: "high",
          detail: "The proposed product locks capital until 2033. Retirement withdrawals must begin 2028. Early surrender triggers charges of 3–7% that reduce the portfolio value available for income precisely when income is most needed."
        },
        {
          label: "Fee impairment",
          severity: "medium",
          detail: "5% up-front load ($45,000 immediate loss) + 1.75%/yr ongoing. At a net 4.5% return, the household spends 1+ year of returns just recovering the load, then pays 1.75%/yr perpetually — approximately $15,000/yr on a $900K allocation. Alternatives with 0.05%/yr expense ratios exist."
        },
        {
          label: "Potential Reg BI conflict of interest",
          severity: "medium",
          detail: "The compensation structure (5% sales load) creates an incentive for the recommending broker that is misaligned with the client's best interest. Reg BI requires disclosing and mitigating this conflict. This flag requires review by the compliance team before any further client interaction on this case."
        }
      ],
      talkingPoints: [
        "Open by affirming their caution: 'You told us your first priority is to protect what you've built — and that's exactly what this review did.'",
        "Be direct about the STOP: 'The product that was proposed to you failed our suitability review. We are not recommending it, and here is why.' Then walk through the five reasons calmly.",
        "Show the capacity/tolerance bar chart — both bars are low and red. 'The proposed product would require someone comfortable with an 80 on this scale. You're at 15 and 22 — and that's completely appropriate for where you are.'",
        "Pivot to the suitable alternative immediately: 'Here is what we DO recommend — a conservative income ladder that gets you to $110K/yr reliably, keeps your money liquid when you need it, and costs a fraction of what was proposed.'",
        "On Social Security timing: 'Delaying Robert's benefit to 70 is one of the best risk-free return moves available to you. Let us model the numbers.'",
        "Close on the swarm's role: 'Six specialists reviewed this simultaneously and independently reached the same conclusion. This is not one advisor's opinion — this is the whole board saying no to that product.'"
      ],
      complianceReasoning: "The pitched product is refused on all five Reg BI care-obligation axes: (1) Reasonable basis — no basis to recommend an 80% aggressive equity product to a documented capital-preservation client; (2) Customer-specific — tolerance 15/100, capacity 22/100 both mandate Conservative band; no path to Aggressive or Growth; (3) Quantitative suitability — the proposal would concentrate 56% of assets in one strategy with a 7-year lockup, the opposite of the diversification required; (4) Conflicts — 5% sales load creates a clear broker incentive that is misaligned with the client's best interest and must be flagged; (5) Disclosure — the surrender schedule and fee structure were not prominently disclosed in the pitch. VERDICT: STOP. Suitable conservative alternative approved in its place."
    }
  }
];
