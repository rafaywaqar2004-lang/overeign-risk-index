# Sovereign Risk Scorecard

A composite sovereign risk score for **all 26 MENA & South Asia economies**
(Algeria, Bahrain, Egypt, Iran, Iraq, Israel, Jordan, Kuwait, Lebanon, Libya,
Morocco, Oman, Qatar, Saudi Arabia, Syria, Tunisia, UAE, Yemen, Afghanistan,
Bangladesh, Bhutan, India, Maldives, Nepal, Pakistan, Sri Lanka), built on
public World Bank data.

**Live app:** https://overeign-risk-index-ql7q7cx9xkcherlpesydmn.streamlit.app

## Features

- **Regional Overview** — a choropleth risk map, ranked bar chart across all
  26 countries, 5 sub-regional averages (Gulf, North Africa, Levant & Iraq,
  Iran & Yemen, South Asia), and a multi-country historical trend comparison
  (2010-2024)
- **Country Deep Dive** — an auto-generated analyst-style Country Brief
  synthesizing score, top risk drivers, recent history, and live-conflict
  exposure into flowing prose; composite score with regional rank and
  year-over-year change; a 10-factor radar chart; historical trend line;
  sourced Key Historical Context (conflicts, protests, IMF programs,
  defaults — each fact-checked and linked to its source); FDI and
  exports/imports trade-context charts; primary stock exchange reference;
  verified IMF Financing Arrangements (amount, approval date, program
  length); and, where verified, a Key Economic Partners summary (major
  creditors/investors)
- **Live Conflicts** — the region's most consequential live flashpoints (the
  2026 Iran-Israel-US war, the Red Sea shipping crisis and Houthi blockade of
  Saudi Arabia, the fragile Gaza ceasefire, Syria's post-Assad transition,
  and Sudan's civil war spillover), each mapped to affected countries with
  sourced summary and market/trade impact — the qualitative complement to
  the necessarily backward-looking annual composite score
- **Scenario Explorer** — live sliders to reweight all 10 factors and see the
  regional ranking recompute in real time
- **Methodology & Data** — full transparency on weights, normalization
  method, direct World Bank indicator source links, and known data
  limitations

## Methodology

Each country is scored 0-100 (100 = highest risk) on a weighted composite of
10 factors across two pillars, weighted equally at 10% by default (adjustable
live in the Scenario Explorer):

| Factor | Pillar | Source |
|---|---|---|
| Debt (% of GDP) | Economic | World Bank WDI (GC.DOD.TOTL.GD.ZS) |
| Current account (% of GDP) | Economic | World Bank WDI (BN.CAB.XOKA.GD.ZS) |
| Reserves (months of imports) | Economic | World Bank WDI (FI.RES.TOTL.MO) |
| GDP growth | Economic | World Bank WDI (NY.GDP.MKTP.KD.ZG) |
| Inflation | Economic | World Bank WDI (FP.CPI.TOTL.ZG) |
| Political stability | Governance | World Bank WGI (PV.EST) |
| Government effectiveness | Governance | World Bank WGI (GE.EST) |
| Rule of law | Governance | World Bank WGI (RL.EST) |
| Regulatory quality | Governance | World Bank WGI (RQ.EST) |
| Control of corruption | Governance | World Bank WGI (CC.EST) |

Each factor is min-max normalized to 0-100 relative to the other countries in
the sample. If a country is missing a factor, that factor is dropped and the
remaining weights are rescaled proportionally — missing data is never
silently treated as "safe." FDI, exports, and imports (all % of GDP) are
tracked separately as descriptive investment/trade context and are
intentionally **not** part of the risk score.

## Historical & conflict data

`context_data.py` contains:
- `HISTORICAL_CONTEXT` — curated historical highlights (IMF programs,
  defaults, political transitions, natural disasters, conflicts) per
  country, each fact-checked via web search and linked to its source
- `FINANCING_ARRANGEMENTS` — verified IMF financing arrangement details
  (amount, approval date, program length) for the 7 countries where this
  was independently confirmed
- `KEY_ECONOMIC_PARTNERS` — sourced summaries of major creditor/investor
  relationships for the 5 countries with the clearest, best-documented cases
  (Pakistan, Sri Lanka, Maldives, Egypt, Qatar)
- `STOCK_EXCHANGES` — each country's primary exchange and benchmark index
  (reference only, not live pricing)
- `LIVE_CONFLICTS` — the 5 most consequential live regional flashpoints,
  each with affected-country mapping, a sourced summary, and market/trade
  impact analysis

All of the above is a curated snapshot fact-checked as of **August 2026**,
not a live feed. Coverage is intentionally partial where sourcing wasn't
solid — see the Methodology tab for the explicit scope note. Instrument-level
bond/loan maturity schedules (a true debt "rollover wall") are out of scope
entirely; that needs a specialized debt database (Bloomberg, the IMF's
sovereign debt investor relations portal, or national debt management
offices), not a web research pass.

## Known limitations (v4)

- **Debt-to-GDP coverage is sparse** — only 11 of 26 countries report it
  consistently to the World Bank. A future improvement would add IMF World
  Economic Outlook debt data as a fallback source.
- **Iran's score is lower-confidence** — only 7 of 10 factors are available,
  likely due to sanctions limiting fiscal data reporting.
- **The composite score is annual and backward-looking** — see the Live
  Conflicts tab for the qualitative, currently-relevant complement.
- Weights are a transparent, reasonable starting point — not a backtested or
  econometrically validated model. Research/screening tool, not investment
  advice.

## Running it locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python fetch_data.py       # pulls live historical data from the World Bank API
python compute_scores.py   # computes composite scores, history, and driver breakdowns
streamlit run app.py       # launches the dashboard
```

## Stack

Python, pandas, Streamlit, Plotly. Data via the World Bank's public API (no
key required).
