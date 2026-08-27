# Sovereign Risk Scorecard

A composite sovereign risk score for 11 MENA & South Asia economies (Pakistan,
Egypt, Morocco, Tunisia, Algeria, Jordan, Saudi Arabia, UAE, Iran, Bangladesh,
Sri Lanka), built on public IMF/World Bank data.

**Live app:** https://overeign-risk-index-ql7q7cx9xkcherlpesydmn.streamlit.app

## Methodology

Each country is scored 0-100 (100 = highest risk) on a weighted composite of:

| Factor | Weight | Source |
|---|---|---|
| Central government debt (% of GDP) | 30% | World Bank WDI |
| Current account balance (% of GDP) | 20% | World Bank WDI |
| Reserves (months of import cover) | 20% | World Bank WDI |
| Political stability estimate | 30% | World Bank Worldwide Governance Indicators |

Each factor is min-max normalized across the country sample, then combined
using the weights above. If a country is missing a factor (this happens —
see "Known limitations" below), that factor is dropped and the remaining
weights are rescaled proportionally, rather than silently treating missing
data as "safe."

## Known limitations (v1)

- **Debt-to-GDP coverage is sparse** for Gulf states and Iran in the World
  Bank's WDI dataset — several either don't report centrally or report with
  a multi-year lag. A v2 improvement would pull IMF World Economic Outlook
  debt data as a fallback source for better coverage.
- **Iran's score is low-confidence** — only 1 of 4 factors (political
  stability) is available, likely due to sanctions limiting what fiscal data
  gets reported to the World Bank.
- This is a v1 methodology built to be transparent and explainable, not a
  finished risk model — weights are a reasonable starting point, not a
  backtested or validated formula.

## Running it locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python fetch_data.py       # pulls live data from the World Bank API
python compute_scores.py   # computes the composite risk score
streamlit run app.py       # launches the dashboard
```

## Stack

Python, pandas, Streamlit, Plotly. Data via the World Bank's public API
(no key required).
