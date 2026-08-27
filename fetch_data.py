"""
Pulls sovereign risk indicators (full historical series, 2010-present) from the
World Bank's public API for a set of MENA / South Asia economies.
"""
import subprocess
import json
import pandas as pd
import time
from datetime import datetime, timezone

COUNTRIES = {
    # MENA
    "DZA": "Algeria",
    "BHR": "Bahrain",
    "EGY": "Egypt",
    "IRN": "Iran",
    "IRQ": "Iraq",
    "ISR": "Israel",
    "JOR": "Jordan",
    "KWT": "Kuwait",
    "LBN": "Lebanon",
    "LBY": "Libya",
    "MAR": "Morocco",
    "OMN": "Oman",
    "QAT": "Qatar",
    "SAU": "Saudi Arabia",
    "SYR": "Syria",
    "TUN": "Tunisia",
    "ARE": "UAE",
    "YEM": "Yemen",
    # South Asia
    "AFG": "Afghanistan",
    "BGD": "Bangladesh",
    "BTN": "Bhutan",
    "IND": "India",
    "MDV": "Maldives",
    "NPL": "Nepal",
    "PAK": "Pakistan",
    "LKA": "Sri Lanka",
}

# Economic pillar
ECON_INDICATORS = {
    "GC.DOD.TOTL.GD.ZS": "debt_to_gdp",
    "BN.CAB.XOKA.GD.ZS": "current_account_pct_gdp",
    "FI.RES.TOTL.MO": "reserves_months_imports",
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",
    "FP.CPI.TOTL.ZG": "inflation",
}

# Investment/trade context (descriptive only — NOT part of the risk score)
CONTEXT_INDICATORS = {
    "BX.KLT.DINV.WD.GD.ZS": "fdi_net_inflows_pct_gdp",
    "NE.EXP.GNFS.ZS": "exports_pct_gdp",
    "NE.IMP.GNFS.ZS": "imports_pct_gdp",
}

# Governance pillar (World Bank Worldwide Governance Indicators)
GOV_INDICATORS = {
    "GOV_WGI_PV.EST": "political_stability",
    "GOV_WGI_GE.EST": "government_effectiveness",
    "GOV_WGI_RL.EST": "rule_of_law",
    "GOV_WGI_RQ.EST": "regulatory_quality",
    "GOV_WGI_CC.EST": "control_of_corruption",
}

INDICATORS = {**ECON_INDICATORS, **GOV_INDICATORS, **CONTEXT_INDICATORS}

BASE_URL = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"


CURRENT_YEAR = datetime.now(timezone.utc).year


def fetch_indicator_series(country_code, indicator_code, retries=3):
    """Returns a dict of {year: value} for all available years 2010-present.
    The upper bound tracks the current year rather than a fixed cutoff, since
    fast-updating indicators (GDP growth, inflation, etc.) are often available
    close to real time even when slower ones (WGI governance scores) lag by a
    year or two — the World Bank API simply omits years it has no data for."""
    url = BASE_URL.format(country=country_code, indicator=indicator_code)
    full_url = f"{url}?format=json&date=2010:{CURRENT_YEAR}&per_page=100"

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


IMF_WEO_URL = "https://www.imf.org/external/datamapper/api/v1/GGXWDG_NGDP"


def fetch_imf_debt_fallback(country_codes, retries=3):
    """Fetches IMF World Economic Outlook general government gross debt
    (% of GDP) for all countries in one call, used as a fallback where the
    World Bank has no debt_to_gdp figure. Returns {country_code: (year, value)}
    using the latest year at or before the current year, to avoid relying on
    the IMF's forward-looking WEO projection years."""
    result = None
    for attempt in range(retries):
        result = subprocess.run(
            ["curl", "-s", "-m", "20", IMF_WEO_URL],
            capture_output=True, text=True, timeout=25
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

    values = data.get("values", {}).get("GGXWDG_NGDP", {})
    fallback = {}
    for code in country_codes:
        series = values.get(code)
        if not series:
            continue
        # Use the latest year <= current year to avoid relying on IMF's forward projections
        eligible_years = [int(y) for y in series if int(y) <= CURRENT_YEAR]
        if not eligible_years:
            continue
        latest_year = max(eligible_years)
        fallback[code] = (latest_year, series[str(latest_year)])
    return fallback


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

    # ---------- IMF WEO debt fallback for countries missing World Bank debt data ----------
    print("\nFetching IMF WEO debt fallback...")
    imf_fallback = fetch_imf_debt_fallback(list(COUNTRIES.keys()))
    fallback_used = []
    for i, row in wide_df.iterrows():
        if pd.isna(row["debt_to_gdp"]) and row["country_code"] in imf_fallback:
            year, value = imf_fallback[row["country_code"]]
            wide_df.at[i, "debt_to_gdp"] = value
            wide_df.at[i, "debt_to_gdp_year"] = year
            wide_df.at[i, "debt_to_gdp_source"] = "IMF WEO (fallback)"
            fallback_used.append(row["country"])
        else:
            wide_df.at[i, "debt_to_gdp_source"] = "World Bank WDI" if pd.notna(row["debt_to_gdp"]) else None

    if fallback_used:
        print(f"Used IMF WEO fallback for: {', '.join(fallback_used)}")

    wide_df.to_csv("raw_data.csv", index=False)

    with open("last_refreshed.txt", "w") as f:
        f.write(datetime.now(timezone.utc).strftime("%Y-%m-%d"))

    print(f"\nSaved raw_data_long.csv ({len(long_df)} rows) and raw_data.csv ({len(wide_df)} countries)")


if __name__ == "__main__":
    main()
