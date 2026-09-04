"""
Market Signals — supplementary, market-based indicators shown on the Country
Deep Dive page, ADDITIVE to (never a replacement for) the World Bank/WGI
-based composite risk score computed in compute_scores.py. None of these
four feed into risk_score, risk_tier, or any factor weight.

Each of the four sub-signals is independently gated on real data actually
being available. Where it isn't, this module returns available=False with an
honest reason string — it never fabricates a number to fill a gap, matching
this project's existing practice (see FI_RES_MOM in econometric_drivers.py).

1. Exchange Rate Pressure Index
   Real, DAILY granularity where available: fx_daily.py runs once a day via
   its own GitHub Action, hitting the free, no-key ExchangeRate-API "Open
   Access" endpoint (open.er-api.com) and appending one real row per country
   to fx_daily_history.csv. pressure_index = abs(latest day-over-day %
   change) / (std dev of the country's own recent daily % changes). Once at
   least MIN_DAILY_OBSERVATIONS real days have accumulated for a country,
   this daily figure is used and disclosed as "daily" granularity.

   Before that history has built up (e.g. right after this feature first
   shipped, or for a currency briefly missing from a given day's feed), this
   falls back to the original real ANNUAL World Bank series (PA.NUS.FCRF,
   "Official exchange rate, LCU per US$", ultimately sourced from IMF
   International Financial Statistics) — specifically the
   currency_depreciation_pct factor fetch_data.py already derives from it
   and stores in raw_data_long.csv. This fallback path uses:
       pressure_index = abs(latest year's % change) / (std dev of the
                         country's own prior years' % changes)
   and is disclosed as "annual" granularity — the two are never silently
   blended; every result says explicitly which one it is.

   GRANULARITY DISCLOSURE (why daily-via-World-Bank/IMF wasn't possible):
   IMF's own monthly effective-exchange-rate SDMX API (dataflow
   IMF.STA:EER, 6.0.0) was evaluated for this feature and found unusable
   within reasonable effort — its real indicator codes are undocumented
   composite strings (e.g. NEER_IX_RY2010_ACW, discovered only via a
   wildcard structural query) that returned an EMPTY dataset even for
   reference queries (Pakistan, Turkey, the US) during live testing against
   the real API. ExchangeRate-API's free endpoint closed this gap instead —
   see fx_daily.py's own module docstring for its terms of use and why a
   new daily Action (not a live per-page-load fetch) was the only way to
   build a real historical series from a "latest snapshot only" free API.

2. ACLED Conflict Events
   Reuses fetch_data.fetch_acled_events(), a real, already-working
   integration against ACLED's live API — no new fetch logic. Requires a
   free ACLED account (email + key, from acleddata.com/register). With no
   credentials configured, this returns available=False rather than a
   fabricated event count; the app's curated Live Conflicts tab is
   unaffected either way.

3. Trade Vulnerability Index (HHI)
   A real Herfindahl-Hirschman concentration index computed from live UN
   Comtrade import-partner data (comtradeapi.un.org/data/v1), gated on a
   user-supplied Comtrade API subscription key (free tier available at
   comtradeapi.un.org). Reporter codes below are UN Comtrade's own current
   numeric codes, confirmed against Comtrade's public reference file
   (comtradeapi.un.org/files/v1/app/reference/Reporters.json) — not M49
   codes assumed from memory, since several of this app's 34 countries
   (Sudan, Ethiopia) have superseded historical reporter codes in that file
   that had to be disambiguated from the current one.

4. Sovereign Bond Yields
   INVESTIGATED AND DELIBERATELY NOT IMPLEMENTED AS LIVE DATA. A full scan
   of the World Bank WDI indicator catalog (1,498 series) turned up no
   sovereign-bond-yield series of any kind. IMF's free public APIs
   (DataMapper, SDMX IFS) don't cover market bond yields either. Real yield
   data for most of these 34 economies exists only behind commercial
   terminals (Bloomberg, Refinitiv) or non-machine-readable national
   debt-office bulletins. Rather than substitute a proxy (e.g. WDI's real
   or lending interest rate) and mislabel it as a bond yield, this signal
   always reports available=False with the reason disclosed.
"""
import json
import os
import subprocess
import time
from datetime import datetime, timedelta, timezone

import numpy as np

# UN Comtrade's own CURRENT numeric reporter codes for this app's 34
# countries, confirmed via comtradeapi.un.org/files/v1/app/reference/
# Reporters.json (not assumed to equal UN M49 codes, which for two of these
# — Sudan and Ethiopia — Comtrade has since reassigned to a superseded
# "(...pre-split)" historical entry).
COMTRADE_REPORTER_CODES = {
    "DZA": 12, "BHR": 48, "EGY": 818, "IRN": 364, "IRQ": 368, "ISR": 376,
    "JOR": 400, "KWT": 414, "LBN": 422, "LBY": 434, "MAR": 504, "OMN": 512,
    "PSE": 275, "QAT": 634, "SAU": 682, "SYR": 760, "TUN": 788, "ARE": 784,
    "YEM": 887, "AFG": 4, "BGD": 50, "BTN": 64, "IND": 699, "MDV": 462,
    "NPL": 524, "PAK": 586, "LKA": 144, "TUR": 792, "SDN": 729, "SSD": 728,
    "ETH": 231, "SOM": 706, "DJI": 262, "ERI": 232,
}

ACLED_WINDOWS = (30, 90, 365)


# ---------------------------------------------------------------------------
# 1. Exchange Rate Pressure Index
# ---------------------------------------------------------------------------
MIN_DAILY_OBSERVATIONS = 8  # daily pct-changes needed (9 raw daily rows) before trusting a daily volatility figure
DAILY_LOOKBACK_ROWS = 31    # cap history used per country to the most recent ~30 days, so an old regime shift doesn't linger in the volatility denominator forever


def _pressure_level(pressure):
    if pressure >= 2.0:
        return "High"
    if pressure >= 1.0:
        return "Elevated"
    return "Normal"


def _exchange_rate_pressure_daily(fx_daily_df, country_code, min_observations=MIN_DAILY_OBSERVATIONS):
    """Real DAILY granularity, built from fx_daily.py's own accumulated
    snapshots (see that module's docstring for the data source and why this
    has to accumulate over time rather than being fetched live per page
    load). Returns None (not a dict) if there isn't yet enough real daily
    history for this country -- the caller falls back to the annual
    calculation in that case."""
    if fx_daily_df is None or fx_daily_df.empty:
        return None
    sub = fx_daily_df[fx_daily_df["country_code"] == country_code].dropna(subset=["lcu_per_usd"]).sort_values("date")
    sub = sub.tail(DAILY_LOOKBACK_ROWS)
    if len(sub) < min_observations + 1:
        return None

    rates = sub["lcu_per_usd"].to_numpy(dtype=float)
    dates = sub["date"].to_numpy()
    pct_changes = (rates[1:] - rates[:-1]) / rates[:-1] * 100

    latest_change = float(pct_changes[-1])
    prior_changes = pct_changes[:-1]
    volatility = float(np.std(prior_changes, ddof=1))
    if volatility == 0 or np.isnan(volatility):
        return None

    pressure = abs(latest_change) / volatility
    return {
        "available": True,
        "granularity": "daily",
        "latest_date": str(dates[-1]),
        "latest_change_pct": latest_change,
        "volatility": volatility,
        "pressure_index": pressure,
        "level": _pressure_level(pressure),
        "n_days": len(sub),
    }


def _exchange_rate_pressure_annual(long_df, country_code, min_years=4):
    """Real, annual: abs(latest YoY FX % change) / std dev of the country's
    own prior years' YoY % changes. Needs at least `min_years` reported
    years (so the volatility denominator means something) or returns
    available=False."""
    sub = long_df[
        (long_df["country_code"] == country_code)
        & (long_df["indicator"] == "currency_depreciation_pct")
    ].dropna(subset=["value"]).sort_values("year")

    if len(sub) < min_years:
        return {
            "available": False,
            "reason": f"Only {len(sub)} year(s) of exchange-rate history reported (need at least {min_years}).",
        }

    changes = sub["value"].to_numpy(dtype=float)
    latest_year = int(sub["year"].iloc[-1])
    latest_change = float(changes[-1])
    prior_changes = changes[:-1]
    volatility = float(np.std(prior_changes, ddof=1))

    if volatility == 0 or np.isnan(volatility):
        return {"available": False, "reason": "No variation in this country's prior exchange-rate history to measure pressure against."}

    pressure = abs(latest_change) / volatility
    return {
        "available": True,
        "granularity": "annual",
        "latest_year": latest_year,
        "latest_change_pct": latest_change,
        "volatility": volatility,
        "pressure_index": pressure,
        "level": _pressure_level(pressure),
        "n_years": len(sub),
    }


def exchange_rate_pressure(long_df, country_code, fx_daily_df=None, min_years=4, min_daily_observations=MIN_DAILY_OBSERVATIONS):
    """Tries the real daily series first (see _exchange_rate_pressure_daily);
    falls back to the real annual World Bank series once daily history is
    genuinely insufficient. The two are never blended -- the returned dict's
    "granularity" key always says exactly which one produced the result."""
    daily = _exchange_rate_pressure_daily(fx_daily_df, country_code, min_daily_observations)
    if daily is not None:
        return daily
    return _exchange_rate_pressure_annual(long_df, country_code, min_years)


# ---------------------------------------------------------------------------
# 2. ACLED Conflict Events
# ---------------------------------------------------------------------------
def _parse_acled_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


def acled_signal(country_name, api_key=None, email=None):
    """Thin wrapper around fetch_data.fetch_acled_events() that buckets real
    returned events into 30/90/365-day windows and flags a simple trend.
    api_key/email, if given (e.g. from the sidebar), are passed straight
    through as explicit overrides — never via a shared/global env mutation,
    so concurrent sessions on the deployed app can't stomp on each other's
    credentials."""
    from fetch_data import fetch_acled_events

    if not api_key or not email:
        return {"available": False, "status": "not_configured", "reason": "ACLED API key / email not configured."}

    cutoff_365 = (datetime.now(timezone.utc) - timedelta(days=400)).strftime("%Y-%m-%d")
    events, request_succeeded = fetch_acled_events(
        [country_name], event_date_from=cutoff_365, api_key=api_key, email=email, return_status=True,
    )
    if not request_succeeded:
        return {
            "available": False,
            "status": "error",
            "reason": "ACLED request failed — the key/email may be invalid, or the API was unreachable just now.",
        }

    now = datetime.now(timezone.utc)
    dated_events = [(e, _parse_acled_date(e.get("event_date"))) for e in events]
    dated_events = [(e, d) for e, d in dated_events if d is not None]

    counts = {}
    for w in ACLED_WINDOWS:
        cutoff_dt = now - timedelta(days=w)
        counts[w] = sum(1 for _, d in dated_events if d >= cutoff_dt)

    rate_30 = counts[30] / 30.0
    rate_prior_60 = max(0, counts[90] - counts[30]) / 60.0
    if rate_prior_60 == 0:
        trend = "up" if rate_30 > 0 else "flat"
    else:
        ratio = rate_30 / rate_prior_60
        trend = "up" if ratio > 1.25 else ("down" if ratio < 0.75 else "flat")

    return {
        "available": True,
        "counts": counts,
        "trend": trend,
        "n_total_365d": counts[365],
    }


# ---------------------------------------------------------------------------
# 3. Trade Vulnerability Index (HHI)
# ---------------------------------------------------------------------------
def fetch_trade_hhi(country_code, api_key, retries=2):
    """Real Herfindahl-Hirschman import-partner concentration index (0-10000
    scale) from live UN Comtrade data. Tries the latest full year, then one
    year back (Comtrade reporting commonly lags 12-18 months) before giving
    up. Requires a real, user-supplied Comtrade subscription key — with none
    given, returns available=False rather than a fabricated index."""
    if not api_key:
        return {"available": False, "status": "not_configured", "reason": "UN Comtrade API key not configured."}

    reporter = COMTRADE_REPORTER_CODES.get(country_code)
    if reporter is None:
        return {"available": False, "status": "error", "reason": "No UN Comtrade reporter code mapped for this country."}

    this_year = datetime.now(timezone.utc).year
    for year in (this_year - 1, this_year - 2):
        url = (
            "https://comtradeapi.un.org/data/v1/get/C/A/HS"
            f"?reporterCode={reporter}&period={year}&cmdCode=TOTAL&flowCode=M"
            "&partnerCode=&partner2Code=0&customsCode=C00&motCode=0&includeDesc=false"
            f"&subscription-key={api_key}"
        )
        result = None
        for _ in range(retries):
            # Azure API Management (which fronts this API) accepts the key
            # either as the Ocp-Apim-Subscription-Key header or the
            # subscription-key query parameter -- both are sent here since
            # the query-param form is the one actually confirmed working
            # against this specific API with a real key during development.
            result = subprocess.run(
                ["curl", "-s", "-m", "20", "-H", f"Ocp-Apim-Subscription-Key: {api_key}", url],
                capture_output=True, text=True, timeout=25,
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

        if isinstance(payload, dict) and payload.get("statusCode") and payload.get("statusCode") != 200:
            return {"available": False, "status": "error", "reason": f"UN Comtrade rejected the request: {payload.get('message', 'invalid key or parameters')}."}

        rows = payload.get("data", []) if isinstance(payload, dict) else []
        partner_rows = [r for r in rows if r.get("partnerCode", 0) != 0 and r.get("primaryValue")]
        total = sum(r["primaryValue"] for r in partner_rows)
        if not partner_rows or total <= 0:
            continue

        hhi = sum((r["primaryValue"] / total) ** 2 for r in partner_rows) * 10000
        if hhi >= 2500:
            level = "High concentration"
        elif hhi >= 1500:
            level = "Moderate concentration"
        else:
            level = "Low concentration (diversified)"
        return {
            "available": True, "year": year, "hhi": hhi, "level": level,
            "n_partners": len(partner_rows),
        }

    return {"available": False, "status": "error", "reason": "UN Comtrade returned no partner-level import data for the last two reporting years."}


# ---------------------------------------------------------------------------
# 4. Sovereign Bond Yields — real gap, disclosed rather than papered over
# ---------------------------------------------------------------------------
def bond_yield_signal(country_code):
    return {
        "available": False,
        "reason": (
            "No free public API publishes market sovereign bond yields for this country set. "
            "A full scan of the World Bank WDI indicator catalog (1,498 series) found none, and "
            "IMF's free public APIs (DataMapper, SDMX IFS) don't cover market yields either. Real "
            "yield data for most of these economies exists only via commercial terminals (Bloomberg, "
            "Refinitiv) or national debt-office bulletins that aren't machine-readable."
        ),
    }


def get_market_signals(long_df, country_code, country_name, acled_key=None, acled_email=None, comtrade_key=None, fx_daily_df=None):
    """Orchestrates all 4 signals for one country. Never raises — each
    sub-signal degrades to available=False on its own if its data/credential
    isn't there."""
    try:
        fx = exchange_rate_pressure(long_df, country_code, fx_daily_df=fx_daily_df)
    except Exception as exc:
        fx = {"available": False, "reason": f"Error computing exchange-rate pressure: {exc}"}

    try:
        acled = acled_signal(country_name, api_key=acled_key, email=acled_email)
    except Exception as exc:
        acled = {"available": False, "reason": f"ACLED request failed: {exc}"}

    try:
        hhi = fetch_trade_hhi(country_code, comtrade_key)
    except Exception as exc:
        hhi = {"available": False, "reason": f"UN Comtrade request failed: {exc}"}

    bonds = bond_yield_signal(country_code)

    return {"fx_pressure": fx, "acled": acled, "trade_hhi": hhi, "bond_yield": bonds}
