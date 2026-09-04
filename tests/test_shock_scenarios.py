"""
Pure-logic regression tests for shock_scenarios.py. Pins down two real bugs
this project already found and fixed by hand (see git history):
  1. reserve-depletion drift under a zero shock (non-zero delta for an
     unaffected country even when nothing should change),
  2. per-channel point contributions not summing to the actually-applied
     delta once the +-MAX_DELTA cap or the 0-100 score bound kicks in.
No network calls -- energy_df is a small synthetic frame passed in directly.
"""
import pandas as pd
import pytest

from shock_scenarios import compute_scenario_impact, SCENARIOS, MAX_DELTA


def _synthetic_scored_df():
    return pd.DataFrame([
        {
            "country_code": "SAU", "country": "Saudi Arabia", "risk_score": 30.0,
            "imports_pct_gdp": 25.0, "exports_pct_gdp": 40.0,
            "gdp_current_usd": 1.1e12, "reserves_months_imports": 8.0,
        },
        {
            "country_code": "PAK", "country": "Pakistan", "risk_score": 60.0,
            "imports_pct_gdp": 18.0, "exports_pct_gdp": 10.0,
            "gdp_current_usd": 3.5e11, "reserves_months_imports": 2.0,
        },
        {
            "country_code": "EGY", "country": "Egypt", "risk_score": 55.0,
            "imports_pct_gdp": 20.0, "exports_pct_gdp": 15.0,
            "gdp_current_usd": 4.0e11, "reserves_months_imports": 4.5,
        },
    ])


def _synthetic_energy_df():
    return pd.DataFrame([
        {"country_code": "SAU", "energy_import_dependency": -300.0},  # large net exporter
        {"country_code": "PAK", "energy_import_dependency": 25.0},
        {"country_code": "EGY", "energy_import_dependency": 10.0},
    ])


def test_zero_shock_produces_zero_delta_for_every_country():
    """A scenario with every shock parameter at its neutral/no-op value must
    leave every country's score exactly unchanged -- this is the exact bug
    (reserve-cover drift from reconstructing a USD ratio instead of using
    the real reported baseline) this project found and fixed."""
    zero_params = {
        "oil_price_change_pct": 0.0,
        "hormuz_multiplier": 1.0,
        "redsea_multiplier": 1.0,
        "inflation_passthrough": 0.0,
        "conflict_delta": 0.0,
        "conflict_affected": set(),
        "currency_shock": {},
        "trade_finance_contraction": {},
    }
    result = compute_scenario_impact(_synthetic_scored_df(), _synthetic_energy_df(), custom_params=zero_params)
    assert (result["delta"].abs() < 1e-6).all(), result[["country_code", "delta"]]


def test_channel_points_sum_to_actually_applied_delta():
    """fiscal_pts + trade_pts + reserve_pts + conflict_pts + currency_pts
    must always sum to exactly `delta` (the score-bound/MAX_DELTA-adjusted,
    actually-applied change), not the pre-cap raw sum -- otherwise the
    Sector/Channel Impact Matrix implies a bigger shock than what was
    actually applied to the score."""
    for key in SCENARIOS:
        result = compute_scenario_impact(_synthetic_scored_df(), _synthetic_energy_df(), scenario_key=key)
        component_sum = result["fiscal_pts"] + result["trade_pts"] + result["reserve_pts"] + result["conflict_pts"] + result["currency_pts"]
        diff = (component_sum - result["delta"]).abs()
        assert (diff < 0.06).all(), f"{key}: {result[['country_code', 'delta']].assign(component_sum=component_sum)}"


def test_delta_never_exceeds_max_delta_cap():
    extreme_params = {
        "oil_price_change_pct": 500.0,
        "hormuz_multiplier": 3.0,
        "redsea_multiplier": 3.0,
        "inflation_passthrough": 1.0,
        "conflict_delta": 100.0,
        "conflict_affected": {"PAK", "EGY", "SAU"},
        "currency_shock": {"PAK": 0.9, "EGY": 0.9, "SAU": 0.9},
        "trade_finance_contraction": {"PAK": 0.9, "EGY": 0.9, "SAU": 0.9},
    }
    result = compute_scenario_impact(_synthetic_scored_df(), _synthetic_energy_df(), custom_params=extreme_params)
    assert (result["delta"].abs() <= MAX_DELTA + 1e-6).all()


def test_shocked_score_stays_within_0_100():
    for key in SCENARIOS:
        result = compute_scenario_impact(_synthetic_scored_df(), _synthetic_energy_df(), scenario_key=key)
        assert (result["shocked_score"] >= 0).all()
        assert (result["shocked_score"] <= 100).all()


def test_country_with_missing_base_score_is_dropped_not_fabricated():
    scored = _synthetic_scored_df()
    scored.loc[len(scored)] = {
        "country_code": "YEM", "country": "Yemen", "risk_score": float("nan"),
        "imports_pct_gdp": 30.0, "exports_pct_gdp": 5.0,
        "gdp_current_usd": 2.0e10, "reserves_months_imports": 1.0,
    }
    result = compute_scenario_impact(scored, _synthetic_energy_df(), scenario_key=next(iter(SCENARIOS)))
    assert "YEM" not in result["country_code"].values
