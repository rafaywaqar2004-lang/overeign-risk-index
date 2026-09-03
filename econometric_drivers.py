"""
Data assembly and panel-regression engine behind the "Drivers Analysis" tab.

Pure logic module (fetching + pandas/linearmodels statistics) — no Streamlit
rendering here, matching how compute_scores.py / fetch_data.py stay separate
from app.py's UI code. Only `st.cache_data` is used, for the same reason
app.py's own load_data() is cached: this pulls from live external APIs and
shouldn't re-fetch on every widget interaction.

Six of the eight variables used here (political_stability, debt_to_gdp,
gdp_growth, inflation, current_account_pct_gdp, reserves_months_imports)
are already fetched by fetch_data.py into raw_data_long.csv — reused as-is,
not re-fetched, to avoid hitting the World Bank API twice for the same data.
Two are new (trade_openness, gov_expenditure), fetched here directly via the
same World Bank indicator API fetch_data.py already uses.

Coverage note (checked directly against the World Bank API): GC.XPN.TOTL.GD.ZS
(government expenditure) has real but uneven reporting -- e.g. Egypt reports
2010-2015 then stops, Pakistan has none in 2010-2024 at all. This is not a
bug in the fetch; it reflects genuinely sparse Government Finance Statistics
reporting for several of these 34 economies. The IMF DataMapper fallback
series named for reserves (FI_RES_MOM) does not exist as a real IMF
DataMapper indicator as of this writing (the endpoint returns no "values"
key for it) -- the fetch code still attempts it and fails gracefully (empty
fallback, exactly like a missing World Bank figure), rather than silently
substituting something else. Both gaps are surfaced to the user via the
per-variable coverage table rather than hidden.
"""
import subprocess
import json
import time
from collections import OrderedDict

import numpy as np
import pandas as pd
import streamlit as st
from scipy import stats as scipy_stats

from fetch_data import COUNTRIES, fetch_indicator_series, fetch_imf_datamapper_fallback, fetch_acled_events

MIN_YEAR = 2010
MAX_YEAR = 2024

DV_COL = "political_stability"
DV_LABEL = "Political Stability (WGI)"

# Order matches the task spec's regression formula.
IV_LABELS = OrderedDict([
    ("debt_to_gdp", "Debt (% GDP)"),
    ("gdp_growth", "GDP Growth (%)"),
    ("inflation", "Inflation (%)"),
    ("current_account_pct_gdp", "Current Account (% GDP)"),
    ("reserves_months_imports", "Reserves Cover (months)"),
    ("trade_openness", "Trade Openness (% GDP)"),
    ("gov_expenditure", "Govt. Expenditure (% GDP)"),
])

# The two indicators NOT already in raw_data_long.csv.
NEW_WB_INDICATORS = {
    "NE.TRD.GNFS.ZS": "trade_openness",
    "GC.XPN.TOTL.GD.ZS": "gov_expenditure",
}

# IMF DataMapper fallback series named in the task spec, attempted for real —
# see module docstring: FI_RES_MOM does not actually exist in IMF DataMapper,
# so that fallback silently contributes nothing, exactly like a genuinely
# missing World Bank figure would.
IMF_PANEL_FALLBACK_SERIES = {
    "debt_to_gdp": "GG_DEBT_GDP",
    "reserves_months_imports": "FI_RES_MOM",
}

ALL_COLS = [DV_COL] + list(IV_LABELS.keys())


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_new_indicators_long():
    """Fetches trade_openness and gov_expenditure for all 34 countries,
    2010-2024, from the World Bank API — the same fetch_indicator_series
    fetch_data.py's own pipeline already uses for every other indicator.
    Returns a long-format DataFrame: country_code, country, indicator, year, value."""
    rows = []
    for code, name in COUNTRIES.items():
        for wb_code, col_name in NEW_WB_INDICATORS.items():
            series = fetch_indicator_series(code, wb_code)
            for year, value in series.items():
                if MIN_YEAR <= year <= MAX_YEAR:
                    rows.append({"country_code": code, "country": name, "indicator": col_name, "year": year, "value": value})
            time.sleep(0.1)
    return pd.DataFrame(rows, columns=["country_code", "country", "indicator", "year", "value"])


def _fetch_imf_datamapper_full_series(series_code, country_codes, retries=3):
    """Like fetch_data.fetch_imf_datamapper_fallback, but returns every
    available year (2010-2024) per country rather than only the latest —
    needed here because this is a per-year PANEL fallback, not a single
    current-snapshot fallback. Same real API call, same graceful empty
    return on failure or a non-existent series (see IMF_PANEL_FALLBACK_SERIES)."""
    url = f"https://www.imf.org/external/datamapper/api/v1/{series_code}"
    result = None
    for _ in range(retries):
        result = subprocess.run(["curl", "-s", "-m", "20", url], capture_output=True, text=True, timeout=25)
        if result.returncode == 0 and result.stdout:
            break
        time.sleep(1)

    if result is None or result.returncode != 0 or not result.stdout:
        return {}
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}

    values = data.get("values", {}).get(series_code, {})
    out = {}
    for code in country_codes:
        series = values.get(code)
        if not series:
            continue
        for year_str, value in series.items():
            year = int(year_str)
            if MIN_YEAR <= year <= MAX_YEAR and value is not None:
                out[(code, year)] = value
    return out


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_imf_panel_fallback():
    """Returns {factor: {(country_code, year): value}} for each series in
    IMF_PANEL_FALLBACK_SERIES. A real, working call against IMF's own public
    API for both series named in the task spec; an entry silently contributes
    nothing if that series has no data for a country-year (see module
    docstring re: FI_RES_MOM)."""
    return {
        factor: _fetch_imf_datamapper_full_series(series_code, list(COUNTRIES.keys()))
        for factor, series_code in IMF_PANEL_FALLBACK_SERIES.items()
    }


def build_panel(long_df):
    """Assembles the country-year panel used for regression, merging:
      - the 6 indicators already in raw_data_long.csv (political_stability,
        debt_to_gdp, gdp_growth, inflation, current_account_pct_gdp,
        reserves_months_imports),
      - the 2 freshly-fetched indicators (trade_openness, gov_expenditure),
      - the IMF DataMapper panel fallback, applied ONLY where the World Bank
        figure is missing (never overriding a real World Bank value) and
        tagged in `<factor>_source` so a filled-in cell is never silently
        indistinguishable from a directly-reported one.
    Returns (panel_df, fallback_counts) where fallback_counts maps factor ->
    number of country-year cells filled by the IMF fallback."""
    existing = long_df[long_df["indicator"].isin(ALL_COLS) & long_df["year"].between(MIN_YEAR, MAX_YEAR)]
    wide = existing.pivot_table(index=["country_code", "country", "year"], columns="indicator", values="value", aggfunc="first").reset_index()

    new_long = fetch_new_indicators_long()
    if not new_long.empty:
        new_wide = new_long.pivot_table(index=["country_code", "country", "year"], columns="indicator", values="value", aggfunc="first").reset_index()
        wide = wide.merge(new_wide, on=["country_code", "country", "year"], how="outer")

    for col in ALL_COLS:
        if col not in wide.columns:
            wide[col] = np.nan

    # Ensure every country x year combination in [MIN_YEAR, MAX_YEAR] exists,
    # even if every indicator is NaN for it — otherwise a country missing
    # entirely from one of the merged sources would just vanish from the
    # panel instead of showing up as missing data.
    full_index = pd.MultiIndex.from_product(
        [list(COUNTRIES.keys()), range(MIN_YEAR, MAX_YEAR + 1)], names=["country_code", "year"]
    )
    wide = wide.set_index(["country_code", "year"]).reindex(full_index).reset_index()
    wide["country"] = wide["country_code"].map(COUNTRIES)

    fallback_counts = {factor: 0 for factor in IMF_PANEL_FALLBACK_SERIES}
    imf_fallback = fetch_imf_panel_fallback()
    for factor, lookup in imf_fallback.items():
        if not lookup:
            continue
        for i, row in wide.iterrows():
            if pd.isna(row[factor]):
                key = (row["country_code"], int(row["year"]))
                if key in lookup:
                    wide.at[i, factor] = lookup[key]
                    fallback_counts[factor] += 1

    return wide, fallback_counts


def variable_coverage(panel_df, cols):
    """Returns {col: (non_null_count, total, pct)} — used to show the user
    exactly how complete each series is before they pick a regression
    specification, rather than only surfacing sparseness after the fact."""
    total = len(panel_df)
    out = {}
    for col in cols:
        non_null = int(panel_df[col].notna().sum())
        out[col] = (non_null, total, (non_null / total * 100) if total else 0.0)
    return out


def prepare_regression_frame(panel_df, dv, ivs):
    """Listwise deletion on [dv] + ivs, then sets the (entity, time) MultiIndex
    linearmodels requires. Returns (clean_df, n_total, n_dropped)."""
    cols = [dv] + list(ivs)
    n_total = len(panel_df)
    clean = panel_df.dropna(subset=cols).copy()
    n_dropped = n_total - len(clean)
    clean = clean.set_index(["country_code", "year"])
    return clean, n_total, n_dropped


def standardize_frame(df, cols):
    """Z-scores the given columns (for standardized-coefficient interpretation)."""
    z = df.copy()
    for col in cols:
        std = z[col].std()
        z[col] = (z[col] - z[col].mean()) / std if std and std > 0 else 0.0
    return z


def _exog(df, ivs, add_const):
    from statsmodels.tools import add_constant
    X = df[list(ivs)]
    return add_constant(X) if add_const else X


def fit_pooled(df, dv, ivs):
    from linearmodels.panel import PooledOLS
    try:
        mod = PooledOLS(df[dv], _exog(df, ivs, add_const=True))
        return mod.fit(cov_type="clustered", cluster_entity=True), None
    except Exception as e:
        return None, str(e)


def fit_fe(df, dv, ivs, time_effects=True):
    from linearmodels.panel import PanelOLS
    try:
        mod = PanelOLS(df[dv], _exog(df, ivs, add_const=False), entity_effects=True, time_effects=time_effects, drop_absorbed=True)
        return mod.fit(cov_type="clustered", cluster_entity=True), None
    except Exception as e:
        return None, str(e)


def fit_re(df, dv, ivs):
    from linearmodels.panel import RandomEffects
    try:
        mod = RandomEffects(df[dv], _exog(df, ivs, add_const=True))
        return mod.fit(cov_type="clustered", cluster_entity=True), None
    except Exception as e:
        return None, str(e)


def hausman_test(fe_res, re_res):
    """Manual Hausman specification test comparing FE vs RE on their common,
    non-effects-absorbed coefficients. NOTE (disclosed to the user in the
    Methodology section): this is computed against an entity-only FE model
    (time_effects=False), since the classic Hausman test doesn't extend
    cleanly to a two-way FE specification — the main results table above
    still reports the full entity+time FE model as the "Fixed Effects"
    column; this test is a separate, narrower check.
    Uses a pseudo-inverse (rather than a plain inverse) for the variance
    difference, since that matrix is very commonly close to singular in
    small panels — a known practical limitation of the classic Hausman test,
    not a bug here."""
    common = [p for p in fe_res.params.index if p in re_res.params.index]
    if not common:
        return None
    b_diff = (fe_res.params[common] - re_res.params[common]).values
    v_diff = fe_res.cov.loc[common, common].values - re_res.cov.loc[common, common].values
    stat = float(b_diff.T @ np.linalg.pinv(v_diff) @ b_diff)
    df_ = len(common)
    pvalue = float(1 - scipy_stats.chi2.cdf(stat, df_))
    return {"statistic": stat, "df": df_, "pvalue": pvalue, "vars": common}


def _stars(p):
    if p is None or pd.isna(p):
        return ""
    if p < 0.01:
        return "***"
    if p < 0.05:
        return "**"
    if p < 0.10:
        return "*"
    return ""


def results_table_rows(results, ivs, n_entities):
    """results: dict of {model_label: (fitted_result_or_None, error_or_None)}.
    n_entities: number of distinct countries in the (shared) regression
    sample -- passed in directly rather than introspected per-model, since
    RandomEffects results don't expose the same entity_info Pooled/FE do,
    and all three models are fit on the identical `clean` frame anyway.
    Returns rows for custom_table: one row per IV (+ const where present),
    each cell 'coef (se) stars'."""
    labels = [IV_LABELS.get(v, v) for v in ivs]
    param_names = list(ivs)
    rows = []
    has_const = any(res is not None and "const" in res.params.index for res, _ in results.values())
    display_params = (["const"] if has_const else []) + param_names
    display_labels = (["Intercept"] if has_const else []) + labels
    for pname, label in zip(display_params, display_labels):
        row = [label]
        for model_label, (res, err) in results.items():
            if res is None or pname not in res.params.index:
                row.append("—")
                continue
            coef = res.params[pname]
            se = res.std_errors[pname]
            p = res.pvalues[pname]
            row.append(f"{coef:+.3f} ({se:.3f}){_stars(p)}")
        rows.append(row)

    for lbl in ["N (obs)", "N (countries)", "R²"]:
        row = [lbl]
        for model_label, (res, err) in results.items():
            if res is None:
                row.append("—")
            elif lbl == "N (obs)":
                row.append(f"{int(res.nobs)}")
            elif lbl == "N (countries)":
                row.append(f"{n_entities}")
            else:
                row.append(f"{res.rsquared:.3f}")
        rows.append(row)
    return rows, list(results.keys())


def standardized_coefficients(df, dv, ivs):
    """Refits the entity+time FE model on standardized (z-scored) data, for
    a relative-importance coefficient plot. FE is used here (rather than
    pooled OLS) so the plotted magnitudes match the same "preferred" model
    used for the residual plot below."""
    z = standardize_frame(df.reset_index(), [dv] + list(ivs)).set_index(["country_code", "year"])
    res, err = fit_fe(z, dv, ivs, time_effects=True)
    if res is None:
        return None, err
    return res.params[list(ivs)].sort_values(key=lambda s: s.abs(), ascending=True), None


def leave_one_out(df, dv, ivs):
    """Re-fits the entity+time FE model once per country, excluding that
    country each time. Returns a DataFrame indexed by excluded country_code
    with one column per IV — lets the user see whether any single country is
    silently driving a coefficient's sign or size."""
    entities = df.index.get_level_values("country_code").unique()
    rows = []
    for code in entities:
        sub = df[df.index.get_level_values("country_code") != code]
        if sub.index.get_level_values("country_code").nunique() < 3:
            continue
        res, err = fit_fe(sub, dv, ivs, time_effects=True)
        if res is None:
            continue
        row = {"excluded_country": code}
        for iv in ivs:
            row[iv] = res.params.get(iv, np.nan)
        rows.append(row)
    return pd.DataFrame(rows).set_index("excluded_country") if rows else pd.DataFrame()


def lag_predictors(panel_df, ivs):
    """Shifts every IV back by one year within each country (t-1 predicting
    the DV at t), keeping the DV at its original year. Countries/years with
    no t-1 observation become NaN, handled by the normal listwise deletion
    in prepare_regression_frame."""
    lagged = panel_df.sort_values(["country_code", "year"]).copy()
    for iv in ivs:
        lagged[iv] = lagged.groupby("country_code")[iv].shift(1)
    return lagged


def conflict_onset_from_acled(acled_events, panel_df, threshold=5):
    """Builds a binary conflict-onset DV (1 if a country-year's ACLED event
    count exceeds `threshold`, else 0) from REAL ACLED events only. Returns
    None if no events were supplied — this path is never fabricated; it
    activates only when fetch_data.fetch_acled_events() actually returned
    live data (i.e. ACLED_API_KEY/ACLED_EMAIL are configured), exactly like
    every other ACLED-dependent feature in this codebase."""
    if not acled_events:
        return None
    ev = pd.DataFrame(acled_events)
    if ev.empty or "event_date" not in ev.columns:
        return None
    ev["year"] = pd.to_datetime(ev["event_date"], errors="coerce").dt.year
    name_to_code = {name: code for code, name in COUNTRIES.items()}
    ev["country_code"] = ev["country"].map(name_to_code)
    counts = ev.groupby(["country_code", "year"]).size().rename("event_count").reset_index()
    merged = panel_df.merge(counts, on=["country_code", "year"], how="left")
    merged["event_count"] = merged["event_count"].fillna(0)
    merged["conflict_onset"] = (merged["event_count"] > threshold).astype(int)
    return merged


def generate_r_code(dv, ivs, panel_csv_name="drivers_panel.csv"):
    formula = f"{dv} ~ " + " + ".join(ivs)
    return f'''# Reproduces the "Drivers Analysis" panel regression (MENASA Risk Monitor)
# in R, using the plm package. Export the panel first from the app's
# "Download Panel Data (CSV)" button and place it alongside this script.
#
# install.packages(c("plm", "lmtest", "sandwich"))
library(plm)
library(lmtest)
library(sandwich)

df <- read.csv("{panel_csv_name}")
pdata <- pdata.frame(df, index = c("country_code", "year"))

formula <- {formula}

# ---- Pooled OLS ----
pooled <- plm(formula, data = pdata, model = "pooling")
cat("\\n=== Pooled OLS (clustered SE by country) ===\\n")
print(coeftest(pooled, vcov = vcovHC(pooled, type = "HC1", cluster = "group")))

# ---- Fixed Effects (entity + time / "twoways") ----
fe <- plm(formula, data = pdata, model = "within", effect = "twoways")
cat("\\n=== Fixed Effects, entity + time (clustered SE by country) ===\\n")
print(coeftest(fe, vcov = vcovHC(fe, type = "HC1", cluster = "group")))

# ---- Random Effects ----
re <- plm(formula, data = pdata, model = "random")
cat("\\n=== Random Effects (clustered SE by country) ===\\n")
print(coeftest(re, vcov = vcovHC(re, type = "HC1", cluster = "group")))

# ---- Hausman test: FE vs RE ----
# NOTE: computed against entity-only FE (effect = "individual") to match the
# classic two-model Hausman setup — the twoways FE above is the app's main
# "Fixed Effects" result, not what this specific test is run against.
fe_entity <- plm(formula, data = pdata, model = "within", effect = "individual")
cat("\\n=== Hausman test (entity-only FE vs RE) ===\\n")
print(phtest(fe_entity, re))
'''


def generate_stata_code(dv, ivs, panel_dta_name="drivers_panel.csv"):
    ivs_str = " ".join(ivs)
    return f'''* Reproduces the "Drivers Analysis" panel regression (MENASA Risk Monitor)
* in Stata. Export the panel first from the app's "Download Panel Data (CSV)"
* button and place it alongside this .do file.

import delimited "{panel_dta_name}", clear
encode country_code, generate(country_id)
xtset country_id year

* ---- Pooled OLS (clustered SE by country) ----
display "=== Pooled OLS ==="
regress {dv} {ivs_str}, vce(cluster country_id)

* ---- Fixed Effects, entity + time (clustered SE by country) ----
display "=== Fixed Effects (entity + time) ==="
xtreg {dv} {ivs_str} i.year, fe vce(cluster country_id)
estimates store fe_twoways

* ---- Random Effects (clustered SE by country) ----
display "=== Random Effects ==="
xtreg {dv} {ivs_str}, re vce(cluster country_id)
estimates store re_model

* ---- Hausman test: entity-only FE vs RE ----
* NOTE: run against entity-only FE (no i.year) to match the classic
* two-model Hausman setup -- the twoways FE above is the app's main
* "Fixed Effects" result, not what this specific test is run against.
quietly xtreg {dv} {ivs_str}, fe
estimates store fe_entity
display "=== Hausman test (entity-only FE vs RE) ==="
hausman fe_entity re_model
'''


METHODOLOGY_MD = """
**Model specification.** The dependent variable is the World Bank's WGI
Political Stability estimate (`political_stability`) — a continuous,
cross-nationally comparable governance score, not a binary "crisis" flag.
Three panel specifications are run on the same regressors: **Pooled OLS**
(ignores country structure entirely — a naive baseline), **Fixed Effects**
(entity + time — absorbs every time-invariant country characteristic, so
coefficients are identified only from within-country variation over time),
and **Random Effects** (assumes the country-level effect is uncorrelated
with the regressors — a stronger, often unrealistic assumption, useful here
mainly as the Hausman test's comparison point). Fixed Effects is the
econometrically preferred specification for this panel: political stability
plausibly correlates with time-invariant country traits (colonial history,
geography, regime type) that also correlate with debt and trade patterns —
exactly the confound Random Effects assumes away.

**Why standard errors are clustered by country.** Observations within the
same country across years are not independent — a debt crisis in year *t*
is highly predictive of debt levels in *t+1*. Ordinary (non-clustered)
standard errors would treat 15 years of the same country's data as 15
independent draws, understating uncertainty and overstating significance.
Clustering by entity (country) is the standard correction and is applied to
every model reported here, pooled OLS included.

**Known limitations — read before treating any coefficient as causal:**
- **Endogeneity / reverse causality.** Debt-to-GDP plausibly *causes*
  instability, but instability (coups, civil conflict, capital flight) also
  plausibly *causes* debt to rise. Nothing here identifies a causal
  direction — an instrumental-variables or dynamic-panel (Arellano-Bond)
  design would be needed for that, and isn't attempted.
- **Omitted variable bias.** Seven regressors cannot capture every driver of
  political stability (external shocks, leadership transitions, conflict
  spillover). Fixed effects absorb *time-invariant* omitted factors only —
  a time-varying omitted shock (e.g. a regional war) is not controlled for.
- **Small T.** With at most 15 years per country and several years typically
  dropped to missing data, the effective within-country time dimension is
  short — fixed-effects estimates are noisier and small-sample bias (the
  Nickell bias, relevant when lagged DVs are involved) is a live concern for
  the lagged-predictor robustness check below.
- **WGI itself is annual and backward-looking**, exactly like this app's own
  composite score (see the main Methodology tab) — it will not reflect an
  event from the last few months, and it is an *estimate* with its own
  published margin of error, not a precise measurement.

**This is illustrative, academic-style analysis for a research/screening
tool — not a publication-quality paper, and not a claim of a validated
causal model.** It exists to make the underlying panel data and a
transparent, reproducible statistical method inspectable, the same way the
rest of this app makes its composite-score methodology inspectable.
"""
