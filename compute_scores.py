"""
Computes:
  1. scored_data.csv       - current composite risk score per country (wide format)
  2. scored_history.csv    - composite risk score per country PER YEAR (for trend charts)
  3. driver_data.csv       - each country's normalized 0-100 risk sub-score per
                             factor (for radar charts + "what's driving this score")

Methodology (v3):
- 10 factors across two pillars, 5 each:
    Economic:   debt, current account, reserves, GDP growth, inflation
    Governance: political stability, government effectiveness, rule of
                law, regulatory quality, control of corruption
- Each factor is min-max normalized to 0-100 (100 = riskiest) CROSS-SECTIONALLY
  (i.e. relative to the other countries in the sample, for that same year).
- Missing factors are dropped per-country and remaining weights rescaled
  proportionally, so missing data never silently reads as "safe."
- FDI (net inflows, % GDP) is tracked separately as descriptive investment
  context — it is NOT part of the risk score, since investment direction
  isn't unambiguously "risk," it's a related but distinct signal.
"""
import pandas as pd

WEIGHTS = {
    "debt_to_gdp": 0.10,
    "current_account_pct_gdp": 0.10,
    "reserves_months_imports": 0.10,
    "gdp_growth": 0.10,
    "inflation": 0.10,
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
    "political_stability": "Political Stability",
    "government_effectiveness": "Govt. Effectiveness",
    "rule_of_law": "Rule of Law",
    "regulatory_quality": "Regulatory Quality",
    "control_of_corruption": "Control of Corruption",
}


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

    df_sorted = df.sort_values("risk_score", ascending=False, na_position="last")
    df_sorted.to_csv("scored_data.csv", index=False)

    # ---------- 2. PER-FACTOR RISK SUB-SCORES (for radar chart + driver analysis) ----------
    driver_df = risk_df.copy()
    driver_df.insert(0, "country", df["country"])
    driver_df.insert(0, "country_code", df["country_code"])
    driver_df.to_csv("driver_data.csv", index=False)

    # ---------- 3. HISTORICAL SCORE PER YEAR (cross-sectional normalization each year) ----------
    history_rows = []
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
        for country_code, score in year_scores.items():
            if score is not None and not pd.isna(score):
                history_rows.append({"country_code": country_code, "year": year, "risk_score": score})

    history_df = pd.DataFrame(history_rows)
    country_lookup = df[["country_code", "country"]].drop_duplicates()
    history_df = history_df.merge(country_lookup, on="country_code", how="left")
    history_df.to_csv("scored_history.csv", index=False)

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

    # ---------- Console summary ----------
    print(df_sorted[["country", "risk_score", "risk_tier", "risk_rank", "yoy_change"]].to_string(index=False))
    print(f"\nSaved scored_data.csv, driver_data.csv, scored_history.csv ({len(history_df)} country-year rows)")


if __name__ == "__main__":
    main()
