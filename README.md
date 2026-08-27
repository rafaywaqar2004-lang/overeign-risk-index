# Sovereign Risk Scorecard

A composite sovereign risk score for **all 26 MENA & South Asia economies**
(Algeria, Bahrain, Egypt, Iran, Iraq, Israel, Jordan, Kuwait, Lebanon, Libya,
Morocco, Oman, Qatar, Saudi Arabia, Syria, Tunisia, UAE, Yemen, Afghanistan,
Bangladesh, Bhutan, India, Maldives, Nepal, Pakistan, Sri Lanka), built on
public World Bank data, with deep sourced qualitative context designed to be
useful as a genuine research reference, not just a scorecard.

**Live app:** https://overeign-risk-index-ql7q7cx9xkcherlpesydmn.streamlit.app

## Features

- **Regional Overview** — a choropleth risk map, ranked bar chart across all
  26 countries, 5 sub-regional averages, and a multi-country historical trend
  comparison (2010-2024)
- **Country Deep Dive**, for every one of the 26 countries:
  - An auto-generated analyst-style Country Brief
  - Composite score with regional rank and year-over-year change
  - A 10-factor radar chart and historical trend line
  - **Key Sectors & Trade Profile** — main economic sectors, biggest exports,
    biggest imports, and leading trade partners
  - Sourced **Key Historical Context** — conflicts, protests, IMF programs,
    defaults, disasters — every entry linked to its source
  - **Financing Arrangements** — verified IMF program details where
    confirmed, or an explicit "net creditor" note for Gulf surplus states
  - **Key Economic Partners** — sourced creditor/investor/trade relationship
    summaries for all 26 countries
  - FDI and exports/imports trade-context charts
  - Primary stock exchange reference
- **Live Conflicts** — 12 major current MENASA flashpoints (the 2026
  Iran-Israel-US war, the Red Sea/Houthi-Saudi blockade, the Gaza ceasefire,
  the Israel-Hezbollah/Lebanon front, Syria's post-Assad transition, Sudan's
  spillover, Libya's rival-government standoff, the 2026 Pakistan-Afghanistan
  war, the 2025 India-Pakistan Kashmir crisis, the Balochistan/CPEC
  insurgency, Iran-aligned militia attacks on US forces in Iraq, and the
  Egypt-Ethiopia Nile dam dispute) — each with the armed/political groups
  involved, affected countries, a sourced summary, and market/trade impact
- **Scenario Explorer** — live sliders to reweight all 10 factors and watch
  the ranking recompute in real time
- **Methodology & Data** — full transparency on weights, normalization,
  direct World Bank indicator source links, and an explicit list of the
  broader source ecosystem used for qualitative content

## Methodology

Each country is scored 0-100 (100 = highest risk) on a weighted composite of
10 factors across two pillars, weighted equally at 10% by default (adjustable
live in the Scenario Explorer). See the in-app Methodology tab for the full
factor/weight/source table.

## Data sources

The **quantitative risk score** is built entirely on the **World Bank's**
public API (WDI + WGI) for consistency and reproducibility.

The **qualitative layers** (historical context, live conflicts, key economic
partners, trade profiles) draw on a much broader source ecosystem, reflecting
how political risk research actually works:

- **News & wire services**: Reuters, Bloomberg, Al Jazeera, Associated Press,
  Times of Israel, France24, Middle East Eye
- **Think tanks & policy research**: Brookings Institution, Council on
  Foreign Relations (CFR) Global Conflict Tracker, CSIS, Carnegie Endowment,
  Atlantic Council, International Crisis Group, Belfer Center (Harvard),
  Chatham House, Stimson Center, Washington Institute, Soufan Center
- **Government & multilateral bodies**: IMF press releases, US Congress.gov
  (CRS reports), UK House of Commons Library, UN Security Council Report
- **Economic/trade data**: CIA World Factbook, Observatory of Economic
  Complexity (OEC), UN Comtrade, EIA (energy)

All of this is a curated snapshot fact-checked via web search as of
**August 2026**, not a live feed. Coverage is intentionally uneven in depth
where sourcing wasn't equally strong across all 26 countries — see the
Methodology tab for the explicit scope note. Instrument-level bond/loan
maturity schedules (a true debt "rollover wall") are out of scope entirely;
that needs a specialized debt database (Bloomberg, the IMF's sovereign debt
investor relations portal, or national debt management offices), not a web
research pass.

## Known limitations (v5)

- **Debt-to-GDP coverage is sparse** — only 11 of 26 countries report it
  consistently to the World Bank.
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

Python, pandas, Streamlit, Plotly. Quantitative data via the World Bank's
public API (no key required).

## v6 additions

- **Credit rating comparison**: actual S&P/Moody's/Fitch sovereign ratings
  for all 26 countries, shown next to this tool's own composite score as a
  sanity check against real-world agency assessments
- **IMF WEO debt fallback**: automatically fills in debt-to-GDP for 13
  countries the World Bank doesn't cover, using the IMF's public World
  Economic Outlook API (raised debt coverage from 11/26 to 24/26 countries)
- **Downloadable PDF country brief**: a "Download Brief (PDF)" button on
  every Country Deep Dive page, generating a formatted one-pager with the
  score, ratings, brief, trade profile, financing, partners, and sourced
  historical context
- **Key statistics on every conflict**: each of the 12 Live Conflicts entries
  now has a row of specific, sourced figures (casualties, attack counts,
  financial costs, displacement numbers) rather than narrative alone
- **Data validation script** (`validate_data.py`): checks every data
  structure for consistency (valid country codes, required fields,
  well-formed source URLs) before deployment
- **Automated weekly data refresh** (`.github/workflows/refresh-data.yml`):
  a GitHub Actions workflow that re-pulls World Bank/IMF data every Monday,
  recomputes all scores, validates them, and commits automatically —
  Streamlit Cloud then auto-redeploys. This keeps the *quantitative* score
  genuinely live. The qualitative content (conflicts, historical context,
  credit ratings) remains a periodically-refreshed curated snapshot by
  design — a true real-time feed for that would require a paid/authenticated
  news API, which is out of scope here.
