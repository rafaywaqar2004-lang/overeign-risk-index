"""
Pulls sovereign risk indicators (full historical series, 2010-2024) from the
World Bank's public API for a set of MENA / South Asia economies.
"""
import subprocess
import json
import pandas as pd
import time

COUNTRIES = {
    "PAK": "Pakistan",
    "EGY": "Egypt",
    "MAR": "Morocco",
    "TUN": "Tunisia",
    "DZA": "Algeria",
    "JOR": "Jordan",
    "SAU": "Saudi Arabia",
    "ARE": "UAE",
    "IRN": "Iran",
    "BGD": "Bangladesh",
    "LKA": "Sri Lanka",
    "IRQ": "Iraq",
    "LBN": "Lebanon",
    "KWT": "Kuwait",
    "QAT": "Qatar",
}

# Economic pillar
ECON_INDICATORS = {
    "GC.DOD.TOTL.GD.ZS": "debt_to_gdp",
    "BN.CAB.XOKA.GD.ZS": "current_account_pct_gdp",
    "FI.RES.TOTL.MO": "reserves_months_imports",
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",
    "FP.CPI.TOTL.ZG": "inflation",
}

# Governance pillar (World Bank Worldwide Governance Indicators)
GOV_INDICATORS = {
    "GOV_WGI_PV.EST": "political_stability",
    "GOV_WGI_GE.EST": "government_effectiveness",
}

INDICATORS = {**ECON_INDICATORS, **GOV_INDICATORS}

BASE_URL = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"


def fetch_indicator_series(country_code, indicator_code, retries=3):
    """Returns a dict of {year: value} for all available years 2010-2024."""
    url = BASE_URL.format(country=country_code, indicator=indicator_code)
    full_url = f"{url}?format=json&date=2010:2024&per_page=100"

    result = None
    for attempt in range(retries):
        result = subprocess.run(
            ["curl", "-s", "-m", "15", full_url],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode == 0 and result.stdout:
            break
        time.sleep(1)

    if result is None or result.returncode != 0 or not result.stdout:
        return {}

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}

    if len(data) < 2 or data[1] is None:
        return {}

    series = {}
    for entry in data[1]:
        if entry["value"] is not None:
            series[int(entry["date"])] = entry["value"]
    return series


def main():
    all_rows = []
    for code, name in COUNTRIES.items():
        for indicator_code, col_name in INDICATORS.items():
            series = fetch_indicator_series(code, indicator_code)
            for year, value in series.items():
                all_rows.append({
                    "country_code": code,
                    "country": name,
                    "indicator": col_name,
                    "year": year,
                    "value": value,
                })
            time.sleep(0.15)
        print(f"Fetched: {name}")

    long_df = pd.DataFrame(all_rows)
    long_df.to_csv("raw_data_long.csv", index=False)

    # Also produce a "latest available value per indicator" wide table for convenience
    latest_rows = []
    for code, name in COUNTRIES.items():
        row = {"country_code": code, "country": name}
        sub = long_df[long_df["country_code"] == code]
        for col_name in INDICATORS.values():
            ind_sub = sub[sub["indicator"] == col_name].sort_values("year", ascending=False)
            if not ind_sub.empty:
                row[col_name] = ind_sub.iloc[0]["value"]
                row[f"{col_name}_year"] = ind_sub.iloc[0]["year"]
            else:
                row[col_name] = None
                row[f"{col_name}_year"] = None
        latest_rows.append(row)

    wide_df = pd.DataFrame(latest_rows)
    wide_df.to_csv("raw_data.csv", index=False)

    print(f"\nSaved raw_data_long.csv ({len(long_df)} rows) and raw_data.csv ({len(wide_df)} countries)")


if __name__ == "__main__":
    main()
