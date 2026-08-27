"""
Pulls sovereign risk indicators from the World Bank's public API
(no API key needed) for a set of MENA / South Asia countries.
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
}

INDICATORS = {
    "GC.DOD.TOTL.GD.ZS": "debt_to_gdp",
    "BN.CAB.XOKA.GD.ZS": "current_account_pct_gdp",
    "FI.RES.TOTL.MO": "reserves_months_imports",
    "GOV_WGI_PV.EST": "political_stability",
}

BASE_URL = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"


def fetch_indicator(country_code, indicator_code, retries=3):
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
        return None

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None

    if len(data) < 2 or data[1] is None:
        return None

    # Find the most recent non-null value
    for entry in data[1]:
        if entry["value"] is not None:
            return {"year": entry["date"], "value": entry["value"]}
    return None


def main():
    rows = []
    for code, name in COUNTRIES.items():
        row = {"country_code": code, "country": name}
        for indicator_code, col_name in INDICATORS.items():
            result = fetch_indicator(code, indicator_code)
            if result:
                row[col_name] = result["value"]
                row[f"{col_name}_year"] = result["year"]
            else:
                row[col_name] = None
                row[f"{col_name}_year"] = None
            time.sleep(0.2)  # be polite to the free API
        rows.append(row)
        print(f"Fetched: {name}")

    df = pd.DataFrame(rows)
    df.to_csv("raw_data.csv", index=False)
    print("\nSaved raw_data.csv")
    print(df)


if __name__ == "__main__":
    main()
