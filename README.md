# MENASA Risk Monitor

*(formerly "Sovereign Risk Scorecard" — renamed to reflect the broader scope: risk scoring, live conflicts, country comparison, and the Geo-Economic Interdependence Dashboard)*

A composite sovereign risk score for **all 34 MENA, South Asia & Horn of Africa economies**
(Algeria, Bahrain, Egypt, Iran, Iraq, Israel, Jordan, Kuwait, Lebanon, Libya,
Morocco, Oman, Palestine, Qatar, Saudi Arabia, Syria, Tunisia, Turkey, UAE, Yemen,
Afghanistan, Bangladesh, Bhutan, India, Maldives, Nepal, Pakistan, Sri Lanka,
Sudan, South Sudan, Ethiopia, Somalia, Djibouti, Eritrea),
built on public World Bank data, with deep sourced qualitative context
designed to be useful as a genuine research reference, not just a scorecard.

**Live app:** https://menasa-risk-monitor.onrender.com

## Written analytic briefs

`briefs/` holds two standalone written analytic pieces built on this tool's own data -- the analytical
narrative half to this dashboard's quantitative half:

- [`sovereign-debt-and-political-instability.md`](briefs/sovereign-debt-and-political-instability.md) --
  three case studies (Pakistan, Sri Lanka, Bangladesh) in fiscal-political feedback loops, grounded in
  `scored_data.csv`/`driver_data.csv` and this repo's curated historical-context/credit-rating/
  current-government records. Published: https://claude.ai/code/artifact/8908bad9-96cc-48e4-8aa1-752d37f7968d
- [`mena-geopolitical-risk-brief-issue-01.md`](briefs/mena-geopolitical-risk-brief-issue-01.md) -- Issue
  No. 1 of a monthly regional-digest series, grounded in the regional snapshot data and the curated
  `LIVE_CONFLICTS` dataset. Published: https://claude.ai/code/artifact/9203fd21-1872-464b-94cb-b72b3b9143a7

Both were originally written and committed in the companion Gulf AI & Tech-Bloc Alignment Tracker repo
(`rafaywaqar2004-lang/oaqjp-final-project-emb-ai`) -- the one a session had write access to at the time --
then moved here once a session had push access to this repo directly, since both are grounded in this
project's data and belong with it, not with the Gulf tracker.

## Features

- **Regional Overview** — a choropleth risk map, ranked bar chart across all
  34 countries, 5 sub-regional averages, and a multi-country historical trend
  comparison (2010-2024)
- **Country Deep Dive**, for every one of the 34 countries:
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
    summaries for all 34 countries
  - FDI and exports/imports trade-context charts
  - Primary stock exchange reference
- **Live Conflicts** — 13 major current MENASA flashpoints (the 2026
  Iran-Israel-US war, the Red Sea/Houthi-Saudi blockade, the Gaza ceasefire,
  the Israel-Hezbollah/Lebanon front, Syria's post-Assad transition, Sudan's
  spillover, Libya's rival-government standoff, the 2026 Pakistan-Afghanistan
  war, the 2025 India-Pakistan Kashmir crisis, the Balochistan/CPEC
  insurgency, Iran-aligned militia attacks on US forces in Iraq, the
  Egypt-Ethiopia Nile dam dispute, and the Western Sahara/Algeria-Morocco
  rupture) — each with the armed/political groups involved, affected
  countries, a sourced summary, and market/trade impact
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
where sourcing wasn't equally strong across all 34 countries — see the
Methodology tab for the explicit scope note. Instrument-level bond/loan
maturity schedules (a true debt "rollover wall") are out of scope entirely;
that needs a specialized debt database (Bloomberg, the IMF's sovereign debt
investor relations portal, or national debt management offices), not a web
research pass.

## Known limitations (v5)

- **Debt-to-GDP coverage is sparse** — only 31 of 34 countries report it
  consistently to the World Bank (the IMF WEO fallback fills some gaps).
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

## v7 additions

- **Fixed a stale date cutoff** in the World Bank fetch that was silently
  discarding already-published 2025 data for fast-moving indicators (GDP
  growth, inflation, current account, reserves, FDI, trade); the cutoff now
  tracks the current year automatically instead of a hardcoded year.
- **Fixed a year-over-year methodology bug**: once 2025-partial data existed,
  the trend/YoY calculation was briefly comparing a 4-factor "2025" (before
  governance indicators had published) against a full 10-factor "2024,"
  producing misleading swings. A year now only counts toward the trend/YoY
  series if both the economic and governance pillars have data for it.
- **Rewrote the Country Brief generator** to do real synthesis instead of
  template-filling: it now states risk trajectory (worsening/easing/stable,
  using real year-over-year data) and explicitly links the top risk driver
  to the historical event still driving it.
- **Deep-research expansion across all 26 countries**: Key Historical
  Context entries rewritten from one-line headlines into 6-9 sourced,
  2-4-sentence analytical events per country (cause → consequence → why it
  matters); Trade Profiles expanded from single phrases into detailed,
  figure-backed descriptions; Key Economic Partners rewritten into 5-8
  sentence summaries covering creditors, major foreign investors, debt
  rollover support, key allies/rivals, and recent deals, each backed by
  4-6 named sources. Financing Arrangements now explicitly cover all 26
  countries (a verified program, or a sourced explanation of why none
  exists), and the per-country tab copy was trimmed to cut repetitive
  disclaimer text.
- **Added a 13th Live Conflict**: the Western Sahara / Algeria-Morocco
  rupture, a major MENASA conflict that had been missing entirely — with
  full actor breakdown, the 2021 diplomatic break, and the Maghreb-Europe
  gas pipeline shutdown's cost to Morocco.
- **Deep-expanded all 13 Live Conflicts** to full analytical depth (6-10
  sentence summaries and market-impact sections with specific dollar/
  percentage figures, 5-8 stats and 5-7 sources each), catching that the
  "2026 Iran-Israel-US War" entry was itself out of date — a second, larger
  war phase (Feb 2026 onward) was still active and unresolved, not the
  earlier, already-concluded phase the entry previously described.
- **Added a data-driven Regional Snapshot** to the Overview tab: a synthesis
  paragraph (avg score, spread, biggest YoY movers, share of the region
  exposed to a live conflict) computed from the actual data each run,
  rather than the tab being pure charts with no narrative.

## v8 additions — Scenario Explorer presets & visual transparency

Two proposed modules (a real-time market-sentiment overlay, and Bayesian/EM
imputation of missing data) were evaluated and deliberately **not** built:
reliable free market data doesn't exist for most of these 26 economies
(several have no tradable sovereign debt instrument at all), and imputing
missing values would reverse this project's core "never silently fill a
gap" design principle. Building either as originally specified risked
misrepresenting coverage or quietly blurring real data with modeled
guesses. What *was* built:

- **Scenario Explorer shock presets**: three one-click stress-test
  scenarios (Red Sea / Shipping Shock, Commodity Price Cycle, Capital
  Flight / Sudden Stop) that reweight all 10 factors to a documented,
  analyst-reasoned configuration, with the rationale shown inline.
- **Radar chart transparency**: a country's missing factors now render as
  a visible amber "not reported" marker on their own axis, rather than
  silently shrinking the shape — no value is ever invented to fill a gap.
- **Conflict map**: all 13 Live Conflicts plotted on an interactive map
  (color-coded by status, hoverable for actors and market impact) using
  Plotly to stay visually consistent with the rest of the app, rather than
  a separate mapping library that would look like a different product.
- **Two-column PDF layout**: the country brief's score summary and credit
  ratings now render side by side on the page, matching the denser,
  structured look of an actual analyst one-pager.

## v9 additions — Economic/Political Risk split & Upcoming Catalysts

Inspired by comparing this tool's approach against a commercial country-risk
product (Fitch Solutions' BMI Country Risk Service): two features adapted to
what a public-data, non-fabricating tool can responsibly do.

- **Economic Risk Index / Political Risk Index**: the composite score's two
  existing pillars (economic fundamentals and governance/political risk),
  now reported as their own 0-100 sub-scores rather than only a single
  blended number. Not a new model — since each pillar is exactly 50% of the
  composite's weight, `composite = 0.5×economic + 0.5×political` whenever
  both have full coverage. Shown on every Country Deep Dive page, plus a
  region-wide Economic Risk vs. Political Risk quadrant chart on the
  Overview tab, surfacing profiles a single blended score hides (e.g. a
  Gulf state with low economic risk but comparatively higher political
  risk, or a fiscally strained but comparatively stable-governed state).
- **Upcoming Catalysts**: a deliberately small, non-exhaustive calendar of
  concrete, dated, sourced forward-looking events — scheduled elections,
  IMF program review windows, similar institutional milestones — verified
  against official/primary sources (IMF press releases and program
  documents, national election authorities, major wire services), not
  estimated or projected. Consistent with this project's "never silently
  fill a gap" principle: a country with nothing verified shows an explicit
  "no confirmed near-term catalyst identified" message rather than a
  manufactured placeholder. See `catalysts_data.py`.
