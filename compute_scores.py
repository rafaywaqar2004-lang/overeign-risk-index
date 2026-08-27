"""
Combines raw indicators into a single 0-100 Sovereign Risk Score per country.

Methodology (v1 — deliberately simple and explainable):
- Each factor is normalized to a 0-100 scale across the country sample
  (min-max normalization), where 100 = riskiest, 0 = safest.
- Factors are weighted and averaged. If a country is missing a factor,
  that factor is dropped for that country and the remaining weights
  are rescaled to still sum to 100% (so missing data doesn't silently
  make a country look artificially safe or risky).
"""
import pandas as pd

WEIGHTS = {
    "debt_to_gdp": 0.30,             # higher debt = higher risk
    "current_account_pct_gdp": 0.20,  # more negative = higher risk (inverted)
    "reserves_months_imports": 0.20,  # fewer months = higher risk (inverted)
    "political_stability": 0.30,      # lower (more negative) = higher risk (inverted)
}

# Whether a HIGHER raw value means HIGHER risk (True) or LOWER risk (False)
HIGHER_IS_RISKIER = {
    "debt_to_gdp": True,
    "current_account_pct_gdp": False,
    "reserves_months_imports": False,
    "political_stability": False,
}


def normalize_to_risk_0_100(series, higher_is_riskier):
    """Min-max normalize a column to 0-100, where 100 = riskiest."""
    valid = series.dropna()
    if valid.empty or valid.min() == valid.max():
        return pd.Series([None] * len(series), index=series.index)

    if higher_is_riskier:
        norm = (series - valid.min()) / (valid.max() - valid.min()) * 100
    else:
        norm = (valid.max() - series) / (valid.max() - valid.min()) * 100
    return norm


def main():
    df = pd.read_csv("raw_data.csv")

    risk_cols = {}
    for factor in WEIGHTS:
        risk_cols[factor] = normalize_to_risk_0_100(df[factor], HIGHER_IS_RISKIER[factor])

    risk_df = pd.DataFrame(risk_cols)

    scores = []
    for i, row in risk_df.iterrows():
        available = row.dropna()
        if available.empty:
            scores.append(None)
            continue
        available_weights = {k: WEIGHTS[k] for k in available.index}
        total_weight = sum(available_weights.values())
        rescaled_weights = {k: w / total_weight for k, w in available_weights.items()}
        score = sum(available[k] * rescaled_weights[k] for k in available.index)
        scores.append(round(score, 1))

    df["risk_score"] = scores
    df["risk_score_factors_used"] = risk_df.notna().sum(axis=1)

    def risk_tier(score):
        if score is None:
            return "Insufficient data"
        if score < 33:
            return "Lower Risk"
        elif score < 66:
            return "Moderate Risk"
        else:
            return "Higher Risk"

    df["risk_tier"] = df["risk_score"].apply(risk_tier)

    df_sorted = df.sort_values("risk_score", ascending=False, na_position="last")
    df_sorted.to_csv("scored_data.csv", index=False)

    print(df_sorted[["country", "risk_score", "risk_tier", "risk_score_factors_used"]].to_string(index=False))
    print("\nSaved scored_data.csv")


if __name__ == "__main__":
    main()
