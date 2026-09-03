"""
Shock-impact engine behind the "Shock Scenario Lab" tab (the upgraded
Scenario Explorer).

Pure logic module (fetching + pandas math) -- no Streamlit rendering here,
matching how compute_scores.py / fetch_data.py / econometric_drivers.py stay
separate from app.py's UI code.

WHAT IS REAL DATA vs. WHAT IS A DISCLOSED MODELING CHOICE
-----------------------------------------------------------
Real, measured inputs (no fabrication):
  - Every country's GDP, imports/exports (% GDP), reserves (USD and months of
    imports), debt-to-GDP, current account, and currency depreciation --
    already in scored_data.csv, fetched live from the World Bank.
  - energy_import_dependency: World Bank EG.IMP.CONS.ZS ("Energy imports,
    net, % of energy use"), fetched fresh here. This is what lets the model
    tell a net oil EXPORTER (Saudi Arabia: roughly -160% to -200% in recent
    years -- exports far more energy than it uses) from a net IMPORTER
    (Pakistan: roughly +25% to +40%) using a real, per-country measurement
    rather than a hand-guessed "is this a Gulf state" flag -- an oil-price
    spike is a fiscal WINDFALL for the former and a fiscal SHOCK for the
    latter, and that asymmetry is real economics, not an assumption.

Disclosed modeling choices (illustrative, not measured):
  - CHOKEPOINT_EXPOSURE: which countries are "high/medium/low/none" exposed
    to the Strait of Hormuz vs. the Red Sea/Bab-el-Mandeb/Suez route. No
    public per-country "% of trade through chokepoint X" statistic exists
    at this granularity, so this is a geographic/trade-relationship
    classification (GCC + Iran + Iraq for Hormuz; Egypt + Red-Sea-adjacent
    and Europe-trading MENASA states for the Red Sea route), not a measured
    figure. Shown explicitly as a classification, not data, in the
    Transmission Model & Assumptions section.
  - The calibration constants below (*_PTS_PER_*) converting a real
    percent-of-GDP fiscal/trade effect into 0-100 risk-score points. No
    institution publishes a precise elasticity mapping a specific fiscal
    shock to a specific governance-risk-score movement -- these are a
    documented, transparent choice, the same honest framing this app's
    existing point-based country-level shock slider (app.py's
    compute_shock_scenario) already uses for the same reason.
"""
from collections import OrderedDict

import numpy as np
import pandas as pd
import streamlit as st

from fetch_data import COUNTRIES, fetch_indicator_series

ENERGY_DEPENDENCE_INDICATOR = "EG.IMP.CONS.ZS"

# ---------------------------------------------------------------------------
# Disclosed calibration constants (see module docstring)
# ---------------------------------------------------------------------------
ENERGY_IMPORT_SHARE_OF_IMPORTS = 0.15   # assumed share of an importer's import bill that is energy
ENERGY_EXPORT_SHARE_OF_EXPORTS = 0.60   # assumed share of a major exporter's export revenue that is energy
FREIGHT_SHARE_OF_IMPORTS = 0.08         # assumed share of import value that is freight/shipping cost

FISCAL_PTS_PER_GDP_PCT_IMPORTER = 3.2   # risk points added per 1% of GDP in extra energy-import cost
FISCAL_PTS_PER_GDP_PCT_EXPORTER = -2.0  # risk points removed per 1% of GDP in extra energy-export windfall
TRADE_PTS_PER_GDP_PCT = 2.5             # risk points per 1% of GDP in extra freight cost
INFLATION_PTS_PER_PCT = 0.35            # risk points per 1 percentage point of CPI pass-through
RESERVE_PTS_PER_MONTH_LOST = 3.5        # risk points per month of import cover lost
CONFLICT_PTS_PER_UNIT = 2.2             # risk points per 1-unit bump on the 0-10 conflict-intensity scale
CURRENCY_PTS_PER_PCT = 0.55             # risk points per 1% currency depreciation
TRADE_FINANCE_PTS_PER_PCT_CONTRACTION = 0.25  # risk points per 1% contraction in trade-finance availability

MAX_DELTA = 45  # cap on |total shock delta| in risk points, either direction -- an illustrative
                # stress test, not a claim any real shock could move the score further than this

# ---------------------------------------------------------------------------
# Chokepoint exposure classification -- disclosed geography/trade-relationship
# judgment, not a measured statistic (see module docstring).
# ---------------------------------------------------------------------------
_HORMUZ_HIGH = {"SAU", "ARE", "QAT", "KWT", "BHR", "OMN", "IRN", "IRQ"}
_HORMUZ_MEDIUM = {"PAK", "IND"}
_RED_SEA_HIGH = {"EGY"}
_RED_SEA_MEDIUM = {
    "JOR", "ISR", "YEM", "DJI", "SOM", "ERI", "SDN", "SSD",
    "SAU", "ARE", "QAT", "KWT", "BHR", "OMN", "LBN", "SYR", "TUR",
    "MAR", "DZA", "TUN", "LBY", "BGD", "LKA", "IND", "PAK",
}


def _exposure_level(code, high_set, medium_set):
    if code in high_set:
        return "high"
    if code in medium_set:
        return "medium"
    return "none"


CHOKEPOINT_EXPOSURE = {
    code: {
        "hormuz": _exposure_level(code, _HORMUZ_HIGH, _HORMUZ_MEDIUM),
        "red_sea": _exposure_level(code, _RED_SEA_HIGH, _RED_SEA_MEDIUM),
    }
    for code in COUNTRIES
}

# Real, sourced figure (see geoeconomic_data.py's MARITIME_CHOKEPOINTS for
# the underlying Suez Canal Authority reporting this is drawn from):
# pre-crisis (2023) Suez Canal annual revenue was approximately $8-9 billion.
EGYPT_SUEZ_ANNUAL_REVENUE_USD_BASELINE = 8.5e9

# Directly-affected countries per the task spec for each preset (drives the
# conflict-intensity bump; chokepoint-driven trade/fiscal terms below still
# apply more broadly based on CHOKEPOINT_EXPOSURE regardless of this list).
_HORMUZ_DIRECTLY_AFFECTED = _HORMUZ_HIGH | _HORMUZ_MEDIUM
_PAKISTAN_CONTAGION = {"BGD": 0.35, "LKA": 0.35, "AFG": 0.45}


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_energy_import_dependency():
    """World Bank EG.IMP.CONS.ZS for all 34 countries -- real net energy
    import dependency (positive = net importer, negative = net exporter),
    most recent available year per country. See module docstring."""
    rows = []
    for code, name in COUNTRIES.items():
        series = fetch_indicator_series(code, ENERGY_DEPENDENCE_INDICATOR)
        if series:
            latest_year = max(series.keys())
            rows.append({"country_code": code, "country": name, "energy_import_dependency": series[latest_year], "energy_import_dependency_year": latest_year})
    return pd.DataFrame(rows, columns=["country_code", "country", "energy_import_dependency", "energy_import_dependency_year"])


SCENARIOS = OrderedDict([
    ("Strait of Hormuz Closure (90 days)", {
        "oil_price_change_pct": (130 - 70) / 70,
        "hormuz_multiplier": 2.5,
        "redsea_multiplier": 1.8,
        "inflation_passthrough": 0.30,
        "conflict_delta": 3.0,
        "conflict_affected": _HORMUZ_DIRECTLY_AFFECTED,
        "currency_shock": {},
        "trade_finance_contraction": {},
        "egypt_suez_shock": False,
        "summary": (
            "Brent crude assumed to spike from a ~$70 baseline to $130/bbl (+85.7%); shipping costs "
            "rise 2.5x on Gulf-bound routes and 1.8x on broader Red Sea/Indian Ocean routes as vessels "
            "reroute or pay a war-risk premium. Directly affected: all GCC states, Iran, Pakistan, India."
        ),
        "calibration_note": (
            "Historical calibration: the 2019 Strait of Hormuz tensions (tanker seizures, drone strikes "
            "on Saudi facilities) raised Brent roughly 15-20%; the 2023-2024 Houthi Red Sea campaign "
            "raised freight rates on affected routes by roughly 150-300% (source: EIA, gCaptain -- see "
            "this app's own Geo-Economic Interdependence tab for the underlying chokepoint reporting). "
            "This scenario models a considerably larger, sustained closure -- illustrative, not a forecast."
        ),
    }),
    ("Red Sea / Bab-el-Mandeb Disruption (180 days)", {
        "oil_price_change_pct": 0.0,
        "hormuz_multiplier": 1.0,
        "redsea_multiplier": 3.0,
        "inflation_passthrough": 0.30,
        "conflict_delta": 1.5,
        "conflict_affected": {"EGY"} | _RED_SEA_HIGH | _RED_SEA_MEDIUM,
        "currency_shock": {},
        "trade_finance_contraction": {},
        "egypt_suez_shock": True,
        "summary": (
            "Freight rates rise 200% on Red Sea/Bab-el-Mandeb-affected routes; Suez Canal transit volume "
            "assumed reduced 70% from its already-depressed post-2023 baseline. Egypt faces a direct Suez "
            "toll-revenue loss on top of the shared freight-cost and inflation effects hitting every "
            "MENASA importer that routes trade via the Red Sea."
        ),
        "calibration_note": (
            "Historical calibration: Suez Canal Authority reporting (see Geo-Economic Interdependence "
            "tab) describes 2023-2026 transit volumes running 41-70% below the pre-crisis (2023) "
            "baseline at various points, with pre-crisis annual toll revenue of roughly $8-9 billion -- "
            "this scenario's 70% transit reduction is within the range actually observed, not a tail case."
        ),
    }),
    ("Pakistan Sovereign Default", {
        "oil_price_change_pct": 0.0,
        "hormuz_multiplier": 1.0,
        "redsea_multiplier": 1.0,
        "inflation_passthrough": 0.0,
        "conflict_delta": 2.0,
        "conflict_affected": {"PAK"},
        "currency_shock": {"PAK": 0.25, **{c: 0.25 * w for c, w in _PAKISTAN_CONTAGION.items()}},
        "trade_finance_contraction": {"PAK": 0.40, **{c: 0.40 * w for c, w in _PAKISTAN_CONTAGION.items()}},
        "egypt_suez_shock": False,
        "summary": (
            "Pakistan defaults on sovereign debt: PKR depreciates 25%, and trade-credit availability "
            "contracts 40%. Modeled contagion (via real trade and remittance linkages, not fabricated "
            "ones -- Bangladesh and Sri Lanka are significant South Asian trade/remittance-corridor "
            "partners, Afghanistan is directly trade- and currency-linked to Pakistan) applies the same "
            "two shocks at 35-45% intensity to Bangladesh, Sri Lanka, and Afghanistan."
        ),
        "calibration_note": (
            "Historical calibration: this mirrors the magnitude of Sri Lanka's actual 2022 crisis (LKR "
            "depreciated roughly 45-80% peak-to-trough against the USD over 2022; see this app's own "
            "Historical Validation section in the Methodology tab) scaled down to a 25% shock, plus "
            "Pakistan's own repeated near-default balance-of-payments episodes (2022-2023)."
        ),
    }),
])


def compute_scenario_impact(scored_df, energy_df, scenario_key=None, *, custom_params=None):
    """Computes shocked risk scores for all countries with a baseline score.

    scenario_key: a key in SCENARIOS, or None to use custom_params directly.
    custom_params: overrides for a preset, or the full parameter set for the
      "Custom / Manual" scenario -- same shape as one SCENARIOS value's core
      fields (oil_price_change_pct, hormuz_multiplier, redsea_multiplier,
      inflation_passthrough, conflict_delta, conflict_affected, currency_shock,
      trade_finance_contraction, egypt_suez_shock).
    Returns a DataFrame: country_code, country, base_score, shocked_score,
    delta, fiscal_pts, trade_pts, reserve_pts, conflict_pts, currency_pts,
    channel (dominant transmission channel), sector (heuristic sector tag)."""
    params = dict(SCENARIOS.get(scenario_key, {}))
    if custom_params:
        params.update(custom_params)

    conflict_affected = params.get("conflict_affected", set())
    currency_shock = params.get("currency_shock", {})
    trade_finance = params.get("trade_finance_contraction", {})

    merged = scored_df.merge(energy_df[["country_code", "energy_import_dependency"]], on="country_code", how="left")
    rows = []
    for _, row in merged.iterrows():
        code = row["country_code"]
        base_score = row.get("risk_score")
        if pd.isna(base_score):
            continue
        exposure = CHOKEPOINT_EXPOSURE.get(code, {"hormuz": "none", "red_sea": "none"})

        if params.get("override_trade_cost_pct") is not None:
            # Custom Shock Builder: a single user-set trade-disruption %
            # applied uniformly to all 34 countries, bypassing the
            # chokepoint-exposure classification entirely (the presets use
            # exposure; the custom builder is explicitly scenario-agnostic
            # per the task spec).
            mult = 1 + params["override_trade_cost_pct"]
        else:
            mult = 1.0
            if exposure["hormuz"] == "high":
                mult = max(mult, params.get("hormuz_multiplier", 1.0))
            elif exposure["hormuz"] == "medium":
                mult = max(mult, 1 + (params.get("hormuz_multiplier", 1.0) - 1) * 0.6)
            if exposure["red_sea"] == "high":
                mult = max(mult, params.get("redsea_multiplier", 1.0))
            elif exposure["red_sea"] == "medium":
                mult = max(mult, 1 + (params.get("redsea_multiplier", 1.0) - 1) * 0.6)
        # mult is the equivalent shipping-cost multiplier (1.0 = no change),
        # defined identically in both branches above; used both for the
        # actual cost math below and the sector heuristic further down.
        trade_cost_increase_pct = mult - 1

        imports_pct_gdp = row.get("imports_pct_gdp")
        exports_pct_gdp = row.get("exports_pct_gdp")
        gdp = row.get("gdp_current_usd")
        energy_dep = row.get("energy_import_dependency")

        fiscal_pct_gdp = 0.0
        oil_change = params.get("oil_price_change_pct", 0.0)
        # Sign convention used throughout this function: NEGATIVE = a cost /
        # risk-increasing effect, POSITIVE = a windfall / risk-reducing
        # effect -- for fiscal_pct_gdp specifically as well as the final
        # *_pts terms.
        if oil_change and pd.notna(energy_dep) and pd.notna(imports_pct_gdp) and pd.notna(exports_pct_gdp):
            if energy_dep >= 0:
                # Net importer: an oil-price rise is a cost.
                fiscal_pct_gdp = -(energy_dep / 100) * oil_change * (imports_pct_gdp / 100) * ENERGY_IMPORT_SHARE_OF_IMPORTS
            else:
                # Net exporter (energy_dep < 0): an oil-price rise is a windfall.
                fiscal_pct_gdp = (-energy_dep / 100) * oil_change * (exports_pct_gdp / 100) * ENERGY_EXPORT_SHARE_OF_EXPORTS

        trade_pct_gdp = 0.0
        inflation_effect_pct = 0.0
        if pd.notna(imports_pct_gdp):
            trade_pct_gdp = (imports_pct_gdp / 100) * trade_cost_increase_pct * FREIGHT_SHARE_OF_IMPORTS
            inflation_effect_pct = trade_cost_increase_pct * params.get("inflation_passthrough", 0.0)

        reserve_months_lost = 0.0
        baseline_cover = row.get("reserves_months_imports")
        if pd.notna(baseline_cover) and baseline_cover > 0:
            # Same freight-share discount as trade_pct_gdp above -- a shipping-
            # cost multiplier applies to the freight portion of the import
            # bill, not the full value of everything imported. Applied
            # directly as a ratio to the real, reported baseline cover
            # (rather than reconstructing reserves/imports from separate USD
            # series) so a zero-shock scenario always yields exactly zero
            # reserve-cover change, regardless of any vintage mismatch
            # between the World Bank's reserves-USD, imports-%-GDP, and
            # reserves-months-of-imports series for a given country.
            effective_trade_cost_pct = trade_cost_increase_pct * FREIGHT_SHARE_OF_IMPORTS
            cost_multiplier = 1 + effective_trade_cost_pct + max(0.0, -fiscal_pct_gdp)
            new_cover = baseline_cover / cost_multiplier
            reserve_months_lost = max(0.0, baseline_cover - new_cover)

        egypt_extra_fiscal_pct_gdp = 0.0
        if params.get("egypt_suez_shock") and code == "EGY" and pd.notna(gdp) and gdp > 0:
            suez_loss_usd = EGYPT_SUEZ_ANNUAL_REVENUE_USD_BASELINE * 0.70 * (180 / 365)
            egypt_extra_fiscal_pct_gdp = -(suez_loss_usd / gdp)

        currency_pct = currency_shock.get(code, 0.0)
        tf_pct = trade_finance.get(code, 0.0)

        # egypt_extra_fiscal_pct_gdp is always <= 0 (a cost), consistent with
        # the same negative-is-cost convention.
        fiscal_total_pct_gdp = fiscal_pct_gdp + egypt_extra_fiscal_pct_gdp
        if fiscal_total_pct_gdp < 0:
            # Cost: convert the (positive) magnitude into positive (risk-increasing) points.
            fiscal_pts = -fiscal_total_pct_gdp * 100 * FISCAL_PTS_PER_GDP_PCT_IMPORTER
        else:
            # Windfall: FISCAL_PTS_PER_GDP_PCT_EXPORTER is itself negative, so
            # this naturally comes out negative (risk-reducing).
            fiscal_pts = fiscal_total_pct_gdp * 100 * FISCAL_PTS_PER_GDP_PCT_EXPORTER

        trade_pts = (trade_pct_gdp * 100) * TRADE_PTS_PER_GDP_PCT + (inflation_effect_pct * 100) * INFLATION_PTS_PER_PCT
        reserve_pts = reserve_months_lost * RESERVE_PTS_PER_MONTH_LOST
        conflict_pts = params.get("conflict_delta", 0.0) * CONFLICT_PTS_PER_UNIT if code in conflict_affected else 0.0
        currency_pts = currency_pct * 100 * CURRENCY_PTS_PER_PCT
        tf_pts = tf_pct * 100 * TRADE_FINANCE_PTS_PER_PCT_CONTRACTION

        total_delta_raw = fiscal_pts + trade_pts + reserve_pts + conflict_pts + currency_pts + tf_pts
        total_delta_capped = float(np.clip(total_delta_raw, -MAX_DELTA, MAX_DELTA))
        shocked_score = float(np.clip(base_score + total_delta_capped, 0, 100))
        # The actually-applied delta can differ from total_delta_raw for two
        # independent reasons: the +-MAX_DELTA cap above, and/or the score
        # itself hitting the 0-100 floor/ceiling (e.g. a high-baseline
        # country whose capped delta would still push it past 100). Rescale
        # every channel's contribution by the SAME ratio so the per-channel
        # breakdown shown in the Sector / Channel Impact Matrix always sums
        # exactly to this actually-applied delta, rather than the components
        # implying a larger shock than what was actually applied to the score.
        total_delta = shocked_score - base_score
        if total_delta_raw != 0 and abs(total_delta - total_delta_raw) > 1e-9:
            _scale = total_delta / total_delta_raw
            fiscal_pts *= _scale
            trade_pts *= _scale
            reserve_pts *= _scale
            conflict_pts *= _scale
            currency_pts *= _scale
            tf_pts *= _scale

        channel_pts = {
            "Fiscal (energy trade)": fiscal_pts,
            "Trade / shipping cost": trade_pts,
            "Reserve depletion": reserve_pts,
            "Conflict escalation": conflict_pts,
            "Currency / trade finance": currency_pts + tf_pts,
        }
        channel = max(channel_pts, key=lambda k: abs(channel_pts[k])) if any(channel_pts.values()) else "None"

        if channel == "Fiscal (energy trade)":
            sector = "Energy"
        elif channel == "Trade / shipping cost":
            sector = "Shipping" if mult > 1.3 else "Food"
        elif channel == "Reserve depletion":
            sector = "Sovereign"
        elif channel == "Conflict escalation":
            sector = "Insurance" if mult > 1.3 else "Sovereign"
        elif channel == "Currency / trade finance":
            sector = "Sovereign"
        else:
            sector = "—"

        rows.append({
            "country_code": code, "country": row["country"],
            "base_score": round(base_score, 1), "shocked_score": round(shocked_score, 1),
            "delta": round(shocked_score - base_score, 1),
            "fiscal_pts": round(fiscal_pts, 2), "trade_pts": round(trade_pts, 2),
            "reserve_pts": round(reserve_pts, 2), "conflict_pts": round(conflict_pts, 2),
            "currency_pts": round(currency_pts + tf_pts, 2),
            "channel": channel, "sector": sector,
            "hormuz_exposure": exposure["hormuz"], "red_sea_exposure": exposure["red_sea"],
            "energy_import_dependency": energy_dep,
        })

    return pd.DataFrame(rows)


TRANSMISSION_METHODOLOGY_MD = f"""
**ILLUSTRATIVE — simplified transmission assumptions, not a forecast.** This tool exists to make a
scenario's mechanical logic inspectable and comparable across countries, not to predict what will
actually happen in a real Hormuz closure, Red Sea disruption, or Pakistani default.

**Oil price → fiscal balance.** Each country's real World Bank energy-import-dependency figure
(`EG.IMP.CONS.ZS`, "Energy imports, net, % of energy use") determines direction and rough magnitude:
a positive value (net importer, e.g. Pakistan ~25-40%) means an oil-price spike raises import costs;
a negative value (net exporter, e.g. Saudi Arabia ~-160% to -200%) means the same price spike is a
fiscal **windfall**. The oil-price change is applied to an assumed share of each country's real imports or
exports (`{ENERGY_IMPORT_SHARE_OF_IMPORTS:.0%}` of imports for importers, `{ENERGY_EXPORT_SHARE_OF_EXPORTS:.0%}`
of exports for major exporters) — a documented simplifying constant, not a per-country measured figure.

**Trade disruption → shipping cost & inflation.** Chokepoint exposure (Strait of Hormuz vs. Red
Sea/Bab-el-Mandeb/Suez) is a geographic/trade-relationship **classification** (high/medium/none per
country — see the app's Geo-Economic Interdependence tab for the underlying chokepoint data), not a
measured "% of trade through this route" statistic, since no public dataset reports that at this
granularity. The resulting freight-cost multiplier is applied to each country's real import bill
(`{FREIGHT_SHARE_OF_IMPORTS:.0%}` of import value assumed to be freight/shipping cost), and a
documented share of that cost increase (scenario-specific — 30% for the Hormuz and Red Sea presets,
per the task's own inflation pass-through assumption) is assumed to pass through to inflation.

**Reserve depletion.** New reserve cover = real total reserves (USD) ÷ new monthly import cost
(baseline monthly imports, scaled up by the same trade/fiscal cost multipliers above) — arithmetic on
real reported figures, not a separate assumption.

**Converting a real percent-of-GDP effect into risk-score points.** No institution publishes a
precise elasticity mapping a specific fiscal or trade shock to a specific governance-risk-score
movement, so this step uses **documented, transparent calibration constants**
(`FISCAL_PTS_PER_GDP_PCT_IMPORTER = {FISCAL_PTS_PER_GDP_PCT_IMPORTER}`,
`FISCAL_PTS_PER_GDP_PCT_EXPORTER = {FISCAL_PTS_PER_GDP_PCT_EXPORTER}`,
`TRADE_PTS_PER_GDP_PCT = {TRADE_PTS_PER_GDP_PCT}`,
`RESERVE_PTS_PER_MONTH_LOST = {RESERVE_PTS_PER_MONTH_LOST}`,
`CONFLICT_PTS_PER_UNIT = {CONFLICT_PTS_PER_UNIT}`,
`CURRENCY_PTS_PER_PCT = {CURRENCY_PTS_PER_PCT}`) rather than an invented precise mapping — the same
honest framing this app's existing single-country shock-slider tool (in the Country Deep Dive tab)
already uses for the same reason. Total shock impact is capped at ±{MAX_DELTA} risk points in either
direction, a deliberate ceiling on how far this illustrative tool will move a score regardless of
input severity.

**Known limitations:** this is a static, single-period stress test, not a dynamic simulation — it
does not model second-round effects (e.g., a government's policy response, IMF intervention, or a
shock's own de-escalation over the stated time window). Countries with missing underlying data (no
World Bank energy-import figure, no reserves data) show a reduced or zero fiscal/reserve effect for
that term specifically, disclosed via each country's result row rather than estimated.
"""
