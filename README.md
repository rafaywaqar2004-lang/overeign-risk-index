# Sovereign Risk Scorecard

A composite sovereign risk score for 15 MENA & South Asia economies (Pakistan,
Egypt, Morocco, Tunisia, Algeria, Jordan, Saudi Arabia, UAE, Iran, Bangladesh,
Sri Lanka, Iraq, Lebanon, Kuwait, Qatar), built on public World Bank data.

**Live app:** https://overeign-risk-index-ql7q7cx9xkcherlpesydmn.streamlit.app

## Features

- **Regional Overview** — a choropleth risk map, ranked bar chart across all
  15 countries, regional (Gulf / South Asia / Levant) averages, and a
  multi-country historical trend comparison (2015-2024)
- **Country Deep Dive** — composite score with regional rank and year-over-year
  change, a 10-factor radar chart, historical trend line, auto-generated
  narrative on key risk drivers, curated historical context (major
  fact-checked economic/political events by year), an FDI investment-context
  chart, and the country's primary stock exchange/benchmark index
- **Scenario Explorer** — live sliders to reweight all 10 factors and see the
  regional ranking recompute in real time (e.g. model a bank's debt-focused
  view vs. a consultancy's governance-weighted view)
- **Methodology & Data** — full transparency on weights, normalization
  method, and known data limitations

## Methodology

Each country is scored 0-100 (100 = highest risk) on a weighted composite of
10 factors across two pillars, weighted equally at 10% by default (adjustable
live in the Scenario Explorer):

| Factor | Pillar | Source |
|---|---|---|
| Debt (% of GDP) | Economic | World Bank WDI |
| Current account (% of GDP) | Economic | World Bank WDI |
| Reserves (months of imports) | Economic | World Bank WDI |
| GDP growth | Economic | World Bank WDI |
| Inflation | Economic | World Bank WDI |
| Political stability | Governance | World Bank WGI |
| Government effectiveness | Governance | World Bank WGI |
| Rule of law | Governance | World Bank WGI |
| Regulatory quality | Governance | World Bank WGI |
| Control of corruption | Governance | World Bank WGI |

Each factor is min-max normalized to 0-100 relative to the other countries in
the sample. If a country is missing a factor, that factor is dropped and the
remaining weights are rescaled proportionally — missing data is never
silently treated as "safe." FDI (net inflows, % GDP) is tracked separately as
descriptive investment context and is intentionally **not** part of the risk
score.

## Historical context data

`context_data.py` contains curated historical highlights (major IMF programs,
defaults, political transitions, natural disasters) and each country's
primary stock exchange, hand-researched and fact-checked against IMF press
releases and major news sources as of August 2026. This is a curated
snapshot, not a live news feed.

## Known limitations (v3)

- **Debt-to-GDP coverage is sparse** for Gulf states and Iran — only 6 of 15
  countries report it consistently to the World Bank. A future improvement
  would add IMF World Economic Outlook debt data as a fallback source.
- **Iran's score is lower-confidence** — only 7 of 10 factors are available,
  likely due to sanctions limiting fiscal data reporting.
- Historical context entries are curated highlights, not exhaustive, and are
  not live-updated.
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
