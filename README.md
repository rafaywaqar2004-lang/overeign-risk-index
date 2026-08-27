# Sovereign Risk Scorecard

A composite sovereign risk score for 15 MENA & South Asia economies (Pakistan,
Egypt, Morocco, Tunisia, Algeria, Jordan, Saudi Arabia, UAE, Iran, Bangladesh,
Sri Lanka, Iraq, Lebanon, Kuwait, Qatar), built on public IMF/World Bank data.

**Live app:** https://overeign-risk-index-ql7q7cx9xkcherlpesydmn.streamlit.app

## Features

- **Regional Overview** — ranked risk scores across all 15 countries, with
  regional (Gulf / South Asia / Levant) averages and a multi-country
  historical trend comparison (2015-2024)
- **Country Deep Dive** — per-country radar chart across all 7 risk factors,
  a historical trend line, an auto-generated narrative identifying each
  country's key risk drivers vs. relative strengths, and the underlying raw
  indicator values
- **Methodology & Data** — full transparency on weights, normalization
  method, and known data limitations

## Methodology

Each country is scored 0-100 (100 = highest risk) on a weighted composite of
7 factors across two pillars:

| Factor | Pillar | Weight | Source |
|---|---|---|---|
| Debt (% of GDP) | Economic | 20% | World Bank WDI |
| Current account (% of GDP) | Economic | 15% | World Bank WDI |
| Reserves (months of imports) | Economic | 15% | World Bank WDI |
| GDP growth | Economic | 10% | World Bank WDI |
| Inflation | Economic | 10% | World Bank WDI |
| Political stability | Governance | 20% | World Bank WGI |
| Government effectiveness | Governance | 10% | World Bank WGI |

Each factor is min-max normalized to 0-100 relative to the other countries in
the sample. If a country is missing a factor, that factor is dropped and the
remaining weights are rescaled proportionally — missing data is never
silently treated as "safe."

## Known limitations (v2)

- **Debt-to-GDP coverage is sparse** for Gulf states and Iran — only 6 of 15
  countries report it consistently to the World Bank. A v3 improvement would
  add IMF World Economic Outlook debt data as a fallback source.
- **Iran's score is lower-confidence** — only 4 of 7 factors are available,
  likely due to sanctions limiting fiscal data reporting.
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
