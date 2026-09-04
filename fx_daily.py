"""
Accumulates a real DAILY exchange-rate time series for this app's 34
countries, one snapshot per day, via a new daily GitHub Action
(.github/workflows/fx-daily-refresh.yml) appending to fx_daily_history.csv.

WHY THIS EXISTS: the app's existing Exchange Rate Pressure Index (see
market_signals.py) is built on real World Bank annual data (PA.NUS.FCRF) --
correct and disclosed, but annual, not the daily/monthly granularity the
feature was originally meant to have. IMF's monthly effective-exchange-rate
API was evaluated separately and found unworkable (see market_signals.py's
module docstring). This module closes that gap with a genuinely free, no-key
DAILY source instead.

DATA SOURCE: the ExchangeRate-API "Open Access" endpoint
(open.er-api.com/v6/latest/USD) -- free, no API key, updates once every 24
hours, real central-bank/market-sourced rates aggregated by
exchangerate-api.com. Per its published terms (exchangerate-api.com/terms,
exchangerate-api.com/docs/free): caching the response is explicitly
permitted (this module does exactly that -- one fetch per day, stored
locally, never re-fetched more than once daily), and using it for analysis
inside this app is allowed; only *re-distributing the raw feed itself* is
not, which this app doesn't do. Required attribution ("Rates By Exchange
Rate API", linking to exchangerate-api.com) is shown in-app next to the
Exchange Rate Pressure signal and on the Methodology page.

WHY A NEW GITHUB ACTION, NOT A LIVE PER-REQUEST FETCH: the free endpoint
only ever returns the CURRENT day's snapshot, not a historical series --
there is no way to ask it "what was the rate 10 days ago." The only way to
build a real day-over-day time series is to accumulate our own snapshots
over time, exactly like every other data source in this project. This means
the daily granularity genuinely improves over the following ~1-2 weeks as
fx_daily_history.csv accumulates real rows -- market_signals.py's
exchange_rate_pressure() explicitly checks how many real daily rows exist
for a country and falls back to the existing annual World Bank calculation
until there's enough history to compute a meaningful daily volatility
figure, rather than ever computing a volatility from too few points.
"""
import subprocess
import time
from datetime import datetime, timezone

import pandas as pd

from fetch_data import COUNTRIES

ER_API_URL = "https://open.er-api.com/v6/latest/USD"

# ISO 4217 currency code for each tracked country. Palestine is
# intentionally absent -- it has no national currency of its own (the West
# Bank and Gaza use the Israeli new shekel and, to a lesser extent, the
# Jordanian dinar) -- a real fact already reflected elsewhere in this app
# (its "Primary Market" reference shows "No national exchange"), not a data
# gap to paper over.
COUNTRY_CURRENCY = {
    "DZA": "DZD", "BHR": "BHD", "EGY": "EGP", "IRN": "IRR", "IRQ": "IQD",
    "ISR": "ILS", "JOR": "JOD", "KWT": "KWD", "LBN": "LBP", "LBY": "LYD",
    "MAR": "MAD", "OMN": "OMR", "QAT": "QAR", "SAU": "SAR", "SYR": "SYP",
    "TUN": "TND", "ARE": "AED", "YEM": "YER",
    "AFG": "AFN", "BGD": "BDT", "BTN": "BTN", "IND": "INR", "MDV": "MVR",
    "NPL": "NPR", "PAK": "PKR", "LKA": "LKR",
    "TUR": "TRY", "SDN": "SDG", "SSD": "SSP", "ETH": "ETB", "SOM": "SOS",
    "DJI": "DJF", "ERI": "ERN",
}

FX_HISTORY_FILE = "fx_daily_history.csv"


def fetch_latest_rates(retries=3):
    """Real, live fetch of today's USD exchange rates for every tracked
    currency. Returns {currency_code: lcu_per_usd} or {} on failure --
    never fabricated, matching every other fetch in this project."""
    result = None
    for _ in range(retries):
        result = subprocess.run(
            ["curl", "-s", "-m", "15", ER_API_URL],
            capture_output=True, text=True, timeout=20,
        )
        if result.returncode == 0 and result.stdout:
            break
        time.sleep(1)

    if result is None or result.returncode != 0 or not result.stdout:
        return {}
    try:
        import json
        payload = json.loads(result.stdout)
    except (ValueError, ImportError):
        return {}

    if payload.get("result") != "success":
        return {}
    return payload.get("rates", {})


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    try:
        existing = pd.read_csv(FX_HISTORY_FILE)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        existing = pd.DataFrame(columns=["date", "country_code", "currency_code", "lcu_per_usd"])

    if today in existing["date"].astype(str).values:
        print(f"fx_daily_history.csv already has a snapshot for {today} -- skipping (idempotent).")
        return

    rates = fetch_latest_rates()
    if not rates:
        print("Could not fetch live exchange rates -- no snapshot recorded for today. "
              "The pressure index will simply reflect one fewer day of real history; "
              "nothing is ever backfilled or estimated.")
        return

    rows = []
    missing = []
    for country_code, currency_code in COUNTRY_CURRENCY.items():
        rate = rates.get(currency_code)
        if rate is None:
            missing.append(f"{country_code} ({currency_code})")
            continue
        rows.append({
            "date": today, "country_code": country_code,
            "currency_code": currency_code, "lcu_per_usd": rate,
        })

    if missing:
        print(f"No rate returned today for: {', '.join(missing)} -- recorded as genuinely missing, not estimated.")

    new_df = pd.DataFrame(rows)
    combined = new_df if existing.empty else pd.concat([existing, new_df], ignore_index=True)
    combined.to_csv(FX_HISTORY_FILE, index=False)
    print(f"Recorded {len(rows)} real exchange-rate snapshots for {today} "
          f"({len(combined)} total rows in {FX_HISTORY_FILE}).")


if __name__ == "__main__":
    main()
