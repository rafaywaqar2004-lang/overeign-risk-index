"""
Computes:
  1. scored_data.csv       - current composite risk score per country (wide format)
  2. scored_history.csv    - composite risk score per country PER YEAR (for trend charts)
  3. driver_data.csv       - each country's normalized 0-100 risk sub-score per
                             factor (for radar charts + "what's driving this score")
  4. driver_history.csv    - the same per-factor normalized sub-scores, but PER YEAR
                             (for the YoY point-attribution breakdown -- exactly which
                             factors drove a score change, and by how much)

Methodology (v4):
- 11 factors across two pillars:
    Economic (6, 1/12 weight each -- 50% of the composite):
        debt, current account, reserves, GDP growth, inflation,
        currency depreciation (YoY % change in the official USD exchange rate --
        added to close a gap this project's own historical backtest surfaced:
        Egypt's 2022-23 currency crisis didn't move the score at all under the
        prior 10-factor version, since no tracked factor was an FX indicator)
    Governance (5, 1/10 weight each -- 50% of the composite):
        political stability, government effectiveness, rule of law,
        regulatory quality, control of corruption
- Each factor is min-max normalized to 0-100 (100 = riskiest) CROSS-SECTIONALLY
  (i.e. relative to the other countries in the sample, for that same year).
- Missing factors are dropped per-country and remaining weights rescaled
  proportionally, so missing data never silently reads as "safe."
- FDI (net inflows, % GDP) is tracked separately as descriptive investment
  context — it is NOT part of the risk score, since investment direction
  isn't unambiguously "risk," it's a related but distinct signal.
- Economic Risk Index / Political Risk Index (v9): the same two pillars,
  reported as their own 0-100 sub-scores (not a separate model) in both
  scored_data.csv and scored_history.csv. Since each pillar carries exactly
  50% of the composite's weight, risk_score == 0.5*economic + 0.5*political
  whenever both pillars have full coverage -- letting the app show, e.g., a
  Gulf state's low economic risk against its comparatively higher political
  risk, or the reverse, rather than only the blended number.
"""
import pandas as pd
from datetime import datetime, timezone

WEIGHTS = {
    "debt_to_gdp": 1 / 12,
    "current_account_pct_gdp": 1 / 12,
    "reserves_months_imports": 1 / 12,
    "gdp_growth": 1 / 12,
    "inflation": 1 / 12,
    "currency_depreciation_pct": 1 / 12,
    "political_stability": 0.10,
    "government_effectiveness": 0.10,
    "rule_of_law": 0.10,
    "regulatory_quality": 0.10,
    "control_of_corruption": 0.10,
}

HIGHER_IS_RISKIER = {
    "debt_to_gdp": True,
    "current_account_pct_gdp": False,
    "reserves_months_imports": False,
    "gdp_growth": False,
    "inflation": True,
    "currency_depreciation_pct": True,
    "political_stability": False,
    "government_effectiveness": False,
    "rule_of_law": False,
    "regulatory_quality": False,
    "control_of_corruption": False,
}

FACTOR_LABELS = {
    "debt_to_gdp": "Debt (% GDP)",
    "current_account_pct_gdp": "Current Account",
    "reserves_months_imports": "Reserves Cover",
    "gdp_growth": "GDP Growth",
    "inflation": "Inflation",
    "currency_depreciation_pct": "Currency Depreciation",
    "political_stability": "Political Stability",
    "government_effectiveness": "Govt. Effectiveness",
    "rule_of_law": "Rule of Law",
    "regulatory_quality": "Regulatory Quality",
    "control_of_corruption": "Control of Corruption",
}

# The composite's two pillars, each exactly 50% of the total weight (6 econ
# factors x 1/12 = 0.5; 5 governance factors x 0.10 = 0.5). Split out here so
# the same two lists drive both the historical pillar-coverage gate below AND
# the Economic/Political Risk Index sub-scores -- a separate reading of "is
# this a fragile-but-well-governed economy, or a stable economy with acute
# governance/political risk" that a single blended composite hides.
ECON_FACTORS = ["debt_to_gdp", "current_account_pct_gdp", "reserves_months_imports", "gdp_growth", "inflation", "currency_depreciation_pct"]
GOV_FACTORS = ["political_stability", "government_effectiveness", "rule_of_law", "regulatory_quality", "control_of_corruption"]


def normalize_to_risk_0_100(series, higher_is_riskier):
    valid = series.dropna()
    if valid.empty or valid.min() == valid.max():
        return pd.Series([None] * len(series), index=series.index)
    if higher_is_riskier:
        norm = (series - valid.min()) / (valid.max() - valid.min()) * 100
    else:
        norm = (valid.max() - series) / (valid.max() - valid.min()) * 100
    return norm


def compute_weighted_score(risk_df):
    """Given a dataframe of per-factor 0-100 risk sub-scores (rows=countries),
    returns a Series of composite scores with rescaled weights for missing data."""
    scores = []
    for i, row in risk_df.iterrows():
        available = row.dropna()
        if available.empty:
            scores.append(None)
            continue
        available_weights = {k: WEIGHTS[k] for k in available.index}
        total_weight = sum(available_weights.values())
        rescaled = {k: w / total_weight for k, w in available_weights.items()}
        score = sum(available[k] * rescaled[k] for k in available.index)
        scores.append(round(score, 1))
    return pd.Series(scores, index=risk_df.index)


_LIVE_EXPORT_RENAME = {
    "country": "Country", "country_code": "Country Code",
    "debt_to_gdp": "Debt To GDP (%)", "current_account_pct_gdp": "Current Account (% GDP)",
    "reserves_months_imports": "Reserves (Months Of Imports)", "gdp_growth": "GDP Growth (%)",
    "inflation": "Inflation (%)", "currency_depreciation_pct": "Currency Depreciation YoY (%)",
    "political_stability": "Political Stability (WGI)",
    "government_effectiveness": "Government Effectiveness (WGI)", "rule_of_law": "Rule Of Law (WGI)",
    "regulatory_quality": "Regulatory Quality (WGI)", "control_of_corruption": "Control Of Corruption (WGI)",
    "fdi_net_inflows_pct_gdp": "FDI Net Inflows (% GDP)", "exports_pct_gdp": "Exports (% GDP)",
    "imports_pct_gdp": "Imports (% GDP)", "official_exchange_rate_lcu_usd": "Official Exchange Rate (LCU per USD)",
    "risk_score": "Composite Risk Score", "risk_score_factors_used": "Factors Used",
    "economic_risk_score": "Economic Risk Index", "economic_risk_factors_used": "Economic Factors Used",
    "political_risk_score": "Political Risk Index", "political_risk_factors_used": "Political Factors Used",
    "risk_tier": "Risk Tier", "risk_rank": "Regional Rank",
    "yoy_change": "YoY Change", "yoy_latest_year": "YoY Latest Year", "yoy_prior_year": "YoY Prior Year",
}


def build_live_export(df_sorted):
    """Builds live_sovereign_risk_data.csv: a single, human-readable,
    Title-Case/underscore-free consolidated snapshot for anyone consuming this
    data OUTSIDE the app itself (e.g. in a spreadsheet). This is an ADDITIONAL
    convenience export layered on top of scored_data.csv / driver_data.csv /
    scored_history.csv, which remain the actual files the Streamlit app and
    its tested per-year methodology are built on — nothing here replaces
    those, since re-architecting a working, validated pipeline around a new
    filename would risk the exact per-year normalization and missing-data
    handling this project has already fixed real bugs in."""
    export_df = df_sorted.copy()
    new_columns = []
    for col in export_df.columns:
        if col in _LIVE_EXPORT_RENAME:
            new_columns.append(_LIVE_EXPORT_RENAME[col])
        elif col.endswith("_year") and col[: -len("_year")] in _LIVE_EXPORT_RENAME:
            new_columns.append(_LIVE_EXPORT_RENAME[col[: -len("_year")]] + " — As Of Year")
        elif col.endswith("_source") and col[: -len("_source")] in _LIVE_EXPORT_RENAME:
            new_columns.append(_LIVE_EXPORT_RENAME[col[: -len("_source")]] + " — Source")
        else:
            new_columns.append(col.replace("_", " ").title())
    export_df.columns = new_columns
    export_df.insert(0, "Data As Of", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    export_df.to_csv("live_sovereign_risk_data.csv", index=False)
    return export_df


def risk_tier(score):
    if score is None or pd.isna(score):
        return "Insufficient data"
    if score < 33:
        return "Lower Risk"
    elif score < 66:
        return "Moderate Risk"
    return "Higher Risk"


def main():
    df = pd.read_csv("raw_data.csv")
    long_df = pd.read_csv("raw_data_long.csv")

    # ---------- 1. CURRENT COMPOSITE SCORE (latest available value per factor) ----------
    risk_cols = {}
    for factor in WEIGHTS:
        risk_cols[factor] = normalize_to_risk_0_100(df[factor], HIGHER_IS_RISKIER[factor])
    risk_df = pd.DataFrame(risk_cols)

    df["risk_score"] = compute_weighted_score(risk_df)
    df["risk_score_factors_used"] = risk_df.notna().sum(axis=1)
    df["risk_tier"] = df["risk_score"].apply(risk_tier)
    df["risk_rank"] = df["risk_score"].rank(ascending=False, method="min")

    # ---------- Economic Risk Index / Political Risk Index (pillar sub-scores) ----------
    # Same normalized sub-scores, same missing-data rescaling, restricted to one
    # pillar's factors -- NOT a new model, just the existing composite's two
    # halves reported separately. Because each pillar is exactly 50% of the
    # composite by construction, risk_score == 0.5*economic + 0.5*political
    # whenever both pillars have full coverage.
    df["economic_risk_score"] = compute_weighted_score(risk_df[ECON_FACTORS])
    df["economic_risk_factors_used"] = risk_df[ECON_FACTORS].notna().sum(axis=1)
    df["political_risk_score"] = compute_weighted_score(risk_df[GOV_FACTORS])
    df["political_risk_factors_used"] = risk_df[GOV_FACTORS].notna().sum(axis=1)

    df_sorted = df.sort_values("risk_score", ascending=False, na_position="last")
    df_sorted.to_csv("scored_data.csv", index=False)

    # ---------- 2. PER-FACTOR RISK SUB-SCORES (for radar chart + driver analysis) ----------
    driver_df = risk_df.copy()
    driver_df.insert(0, "country", df["country"])
    driver_df.insert(0, "country_code", df["country_code"])
    driver_df.to_csv("driver_data.csv", index=False)

    # ---------- 3. HISTORICAL SCORE PER YEAR (cross-sectional normalization each year) ----------
    # A year only qualifies as a valid trend/YoY point for a country if BOTH pillars
    # have at least one reporting factor that year. Without this guard, a year where
    # only fast-moving economic indicators have been published yet (governance
    # indicators like WGI lag ~1-2 years behind) would silently produce a composite
    # built from a completely different, much narrower factor set than neighboring
    # years — creating a fake-looking swing in the trend/YoY that reflects a change
    # in what's being measured, not real-world risk.
    history_rows = []
    driver_history_rows = []
    years = sorted(long_df["year"].unique())
    for year in years:
        year_slice = long_df[long_df["year"] == year]
        pivot = year_slice.pivot_table(index="country_code", columns="indicator", values="value", aggfunc="first")
        if pivot.empty:
            continue
        for factor in WEIGHTS:
            if factor not in pivot.columns:
                pivot[factor] = None

        year_risk_cols = {}
        for factor in WEIGHTS:
            year_risk_cols[factor] = normalize_to_risk_0_100(pivot[factor], HIGHER_IS_RISKIER[factor])
        year_risk_df = pd.DataFrame(year_risk_cols, index=pivot.index)

        year_scores = compute_weighted_score(year_risk_df)
        econ_coverage = year_risk_df[ECON_FACTORS].notna().sum(axis=1)
        gov_coverage = year_risk_df[GOV_FACTORS].notna().sum(axis=1)
        for country_code, score in year_scores.items():
            if score is None or pd.isna(score):
                continue
            if econ_coverage.get(country_code, 0) == 0 or gov_coverage.get(country_code, 0) == 0:
                continue  # one whole pillar missing this year — not a comparable composite
            history_rows.append({
                "country_code": country_code, "year": year, "risk_score": score,
                "economic_risk_score": compute_weighted_score(year_risk_df.loc[[country_code], ECON_FACTORS]).iloc[0],
                "political_risk_score": compute_weighted_score(year_risk_df.loc[[country_code], GOV_FACTORS]).iloc[0],
            })
            # Same-gated per-factor normalized sub-scores for this country-year --
            # lets the app decompose a YoY score change into each factor's exact
            # point contribution (weight x change in sub-score, rescaled weights
            # recomputed from whichever factors are non-null that year), rather
            # than only naming the top driver without quantifying it.
            driver_history_rows.append({
                "country_code": country_code, "year": year,
                **{f: year_risk_df.loc[country_code, f] for f in WEIGHTS},
            })

    history_df = pd.DataFrame(history_rows)
    country_lookup = df[["country_code", "country"]].drop_duplicates()
    history_df = history_df.merge(country_lookup, on="country_code", how="left")
    history_df.to_csv("scored_history.csv", index=False)

    driver_history_df = pd.DataFrame(driver_history_rows)
    driver_history_df.to_csv("driver_history.csv", index=False)

    # ---------- 4. YEAR-OVER-YEAR CHANGE (latest year in history vs. prior year) ----------
    yoy_rows = []
    for code in df["country_code"]:
        c_hist = history_df[history_df["country_code"] == code].sort_values("year")
        if len(c_hist) >= 2:
            latest = c_hist.iloc[-1]
            prior = c_hist.iloc[-2]
            yoy_rows.append({
                "country_code": code,
                "yoy_change": round(latest["risk_score"] - prior["risk_score"], 1),
                "yoy_latest_year": int(latest["year"]),
                "yoy_prior_year": int(prior["year"]),
            })
        else:
            yoy_rows.append({"country_code": code, "yoy_change": None, "yoy_latest_year": None, "yoy_prior_year": None})

    yoy_df = pd.DataFrame(yoy_rows)
    df_sorted = df_sorted.merge(yoy_df, on="country_code", how="left")
    df_sorted.to_csv("scored_data.csv", index=False)

    # ---------- 5. CONSOLIDATED, HUMAN-READABLE LIVE EXPORT ----------
    build_live_export(df_sorted)

    # ---------- Console summary ----------
    print(df_sorted[["country", "risk_score", "risk_tier", "risk_rank", "yoy_change"]].to_string(index=False))
    print(f"\nSaved scored_data.csv, driver_data.csv, scored_history.csv ({len(history_df)} country-year rows), "
          f"driver_history.csv ({len(driver_history_df)} country-year rows), live_sovereign_risk_data.csv")


if __name__ == "__main__":
    main()
