"""
Pulls sovereign risk indicators (full historical series, 2010-present) from the
World Bank's public API for a set of MENA / South Asia economies.
"""
import os
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
    "PSE": "Palestine",
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
    # Dollar-denominated scale indicators — descriptive context (how large the
    # economy/reserve buffer actually is in absolute terms), not part of the
    # risk score, which is intentionally built on ratios (% of GDP, months of
    # imports) so a small and a large economy are comparable on the same scale.
    "NY.GDP.MKTP.CD": "gdp_current_usd",
    "NY.GDP.PCAP.CD": "gdp_per_capita_usd",
    "FI.RES.TOTL.CD": "total_reserves_usd",
    # Labor-market and inequality indicators for the Country Deep Dive's
    # "Major Indicators" box — descriptive context, not part of the risk
    # score. Gini coverage is real but notoriously sparse for this region
    # (many Gulf states have never reported it) — shown as "No data" rather
    # than estimated, consistent with how every other missing value is
    # handled throughout this app.
    "SL.UEM.TOTL.ZS": "unemployment_rate",
    "SL.UEM.1524.ZS": "youth_unemployment_rate",
    "SI.POV.GINI": "gini_index",
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


# IMF World Economic Outlook series (via the IMF DataMapper REST/JSON API —
# public, no API key required). Used purely as a FALLBACK for countries where
# the World Bank has no figure for a given factor, exactly like the existing
# debt fallback below — never overriding a real World Bank figure when one
# exists, since the composite score's methodology is built and documented
# around World Bank WDI/WGI as the primary source.
IMF_DATAMAPPER_SERIES = {
    "debt_to_gdp": "GGXWDG_NGDP",       # General government gross debt (% of GDP)
    "gdp_growth": "NGDP_RPCH",          # Real GDP growth (annual % change)
    "inflation": "PCPIPCH",             # Inflation, average consumer prices (annual % change)
}


def fetch_imf_datamapper_fallback(series_code, country_codes, retries=3):
    """Fetches one IMF WEO DataMapper series for all countries in a single
    call. Returns {country_code: (year, value)} using the latest year at or
    before the current year, to avoid relying on the IMF's forward-looking
    WEO projection years. Used as a fallback source only (see
    IMF_DATAMAPPER_SERIES) — this is a real, working call against IMF's own
    public API, not a placeholder."""
    url = f"https://www.imf.org/external/datamapper/api/v1/{series_code}"
    result = None
    for attempt in range(retries):
        result = subprocess.run(
            ["curl", "-s", "-m", "20", url],
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

    values = data.get("values", {}).get(series_code, {})
    fallback = {}
    for code in country_codes:
        series = values.get(code)
        if not series:
            continue
        eligible_years = [int(y) for y in series if int(y) <= CURRENT_YEAR]
        if not eligible_years:
            continue
        latest_year = max(eligible_years)
        fallback[code] = (latest_year, series[str(latest_year)])
    return fallback


def fetch_imf_debt_fallback(country_codes, retries=3):
    """Backwards-compatible wrapper around fetch_imf_datamapper_fallback for
    the debt series specifically, kept so existing callers/tests don't need
    to change."""
    return fetch_imf_datamapper_fallback(IMF_DATAMAPPER_SERIES["debt_to_gdp"], country_codes, retries)


# ---------------------------------------------------------------------------
# ACLED (Armed Conflict Location & Event Data Project) — OPTIONAL live conflict
# event feed.
#
# ACLED's API requires a free registered account (email + access key from
# acleddata.com) — there is no public, keyless endpoint. This function is a
# real, complete integration against ACLED's actual REST API: if
# ACLED_API_KEY and ACLED_EMAIL are present as environment variables (set as
# GitHub repo secrets in CI, or exported locally), it will genuinely fetch and
# parse live conflict events. If they are NOT set, it prints a clear message
# and returns an empty list rather than fabricating conflict data — this app's
# curated, hand-sourced LIVE_CONFLICTS dataset (see context_data.py) remains
# the source of truth for the Live Conflicts tab either way; this function
# only ever supplies an OPTIONAL supplementary raw event feed.
# ---------------------------------------------------------------------------
ACLED_API_URL = "https://api.acleddata.com/acled/read"


def fetch_acled_events(country_names, event_date_from=None, retries=3):
    """Fetches recent conflict/security incident events from the real ACLED
    API for the given country names. Returns a list of event dicts (event_date,
    country, event_type, actor1, actor2, fatalities, notes) or an empty list
    if credentials aren't configured or the request fails — never synthetic
    data standing in for a real response.

    To activate: register a free account at https://acleddata.com/register/,
    then set ACLED_API_KEY and ACLED_EMAIL as repository secrets (see
    .github/workflows/refresh-data.yml, which already passes them through as
    environment variables if present)."""
    api_key = os.environ.get("ACLED_API_KEY")
    email = os.environ.get("ACLED_EMAIL")
    if not api_key or not email:
        print(
            "ACLED_API_KEY / ACLED_EMAIL not set — skipping the optional live ACLED conflict feed. "
            "Register at https://acleddata.com/register/ and set both as repo secrets to enable it. "
            "The curated Live Conflicts tab (context_data.py) is unaffected either way."
        )
        return []

    all_events = []
    for country in country_names:
        params = (
            f"key={api_key}&email={email}&country={country.replace(' ', '%20')}"
            f"&limit=100&format=json"
        )
        if event_date_from:
            params += f"&event_date={event_date_from}&event_date_where=%3E%3D"
        url = f"{ACLED_API_URL}?{params}"

        result = None
        for attempt in range(retries):
            result = subprocess.run(
                ["curl", "-s", "-m", "20", url],
                capture_output=True, text=True, timeout=25
            )
            if result.returncode == 0 and result.stdout:
                break
            time.sleep(1)

        if result is None or result.returncode != 0 or not result.stdout:
            continue
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError:
            continue
        if not payload.get("success"):
            continue

        for entry in payload.get("data", []):
            all_events.append({
                "country": country,
                "event_date": entry.get("event_date"),
                "event_type": entry.get("event_type"),
                "actor1": entry.get("actor1"),
                "actor2": entry.get("actor2"),
                "fatalities": entry.get("fatalities"),
                "notes": entry.get("notes"),
            })
        time.sleep(0.2)

    return all_events


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

    # ---------- IMF WEO fallback for factors missing World Bank data ----------
    # Applied to all 3 series in IMF_DATAMAPPER_SERIES (debt, GDP growth,
    # inflation) using the identical fallback-only pattern: a real World Bank
    # figure always wins; IMF WEO only fills a genuine gap, and every filled
    # cell is labeled with its actual source so nothing is silently blended.
    for factor, series_code in IMF_DATAMAPPER_SERIES.items():
        print(f"\nFetching IMF WEO fallback for {factor} ({series_code})...")
        imf_fallback = fetch_imf_datamapper_fallback(series_code, list(COUNTRIES.keys()))
        fallback_used = []
        for i, row in wide_df.iterrows():
            if pd.isna(row[factor]) and row["country_code"] in imf_fallback:
                year, value = imf_fallback[row["country_code"]]
                wide_df.at[i, factor] = value
                wide_df.at[i, f"{factor}_year"] = year
                wide_df.at[i, f"{factor}_source"] = "IMF WEO (fallback)"
                fallback_used.append(row["country"])
            else:
                wide_df.at[i, f"{factor}_source"] = "World Bank WDI" if pd.notna(row[factor]) else None
        if fallback_used:
            print(f"Used IMF WEO fallback for {factor}: {', '.join(fallback_used)}")

    wide_df.to_csv("raw_data.csv", index=False)

    # ---------- Optional ACLED live conflict event feed ----------
    # No-ops cleanly (see fetch_acled_events docstring) unless ACLED_API_KEY /
    # ACLED_EMAIL are actually configured. The curated LIVE_CONFLICTS dataset
    # in context_data.py remains the Live Conflicts tab's source either way —
    # this is a supplementary raw feed only, written to its own file so it
    # never silently overwrites hand-sourced, fact-checked content.
    acled_events = fetch_acled_events(list(COUNTRIES.values()))
    if acled_events:
        pd.DataFrame(acled_events).to_csv("acled_events_raw.csv", index=False)
        print(f"Saved acled_events_raw.csv ({len(acled_events)} events)")

    with open("last_refreshed.txt", "w") as f:
        f.write(datetime.now(timezone.utc).strftime("%Y-%m-%d"))

    print(f"\nSaved raw_data_long.csv ({len(long_df)} rows) and raw_data.csv ({len(wide_df)} countries)")


if __name__ == "__main__":
    main()
