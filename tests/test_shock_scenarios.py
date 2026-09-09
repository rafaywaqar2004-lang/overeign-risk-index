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


# ---------------------------------------------------------------------------
# Iran-Israel-US War / India-Pakistan Crisis: new one-off fiscal mechanisms
# ---------------------------------------------------------------------------
def _scored_df_with_qatar_israel_india():
    df = _synthetic_scored_df()
    df.loc[len(df)] = {
        "country_code": "QAT", "country": "Qatar", "risk_score": 20.0,
        "imports_pct_gdp": 30.0, "exports_pct_gdp": 50.0,
        "gdp_current_usd": 2.2e11, "reserves_months_imports": 6.0,
    }
    df.loc[len(df)] = {
        "country_code": "ISR", "country": "Israel", "risk_score": 35.0,
        "imports_pct_gdp": 25.0, "exports_pct_gdp": 28.0,
        "gdp_current_usd": 5.5e11, "reserves_months_imports": 10.0,
    }
    df.loc[len(df)] = {
        "country_code": "IND", "country": "India", "risk_score": 40.0,
        "imports_pct_gdp": 22.0, "exports_pct_gdp": 20.0,
        "gdp_current_usd": 3.9e12, "reserves_months_imports": 9.0,
    }
    return df


def _energy_df_with_qatar_israel_india():
    df = _synthetic_energy_df()
    df.loc[len(df)] = {"country_code": "QAT", "energy_import_dependency": -400.0}
    df.loc[len(df)] = {"country_code": "ISR", "energy_import_dependency": 20.0}
    df.loc[len(df)] = {"country_code": "IND", "energy_import_dependency": 35.0}
    return df


def test_iran_israel_and_india_pakistan_scenarios_exist_with_expected_shape():
    assert "Iran-Israel-US War: Renewed Escalation" in SCENARIOS
    assert "India-Pakistan Crisis: Renewed Escalation" in SCENARIOS
    iran_israel = SCENARIOS["Iran-Israel-US War: Renewed Escalation"]
    assert iran_israel["conflict_affected"] == {"IRN", "ISR", "SAU", "QAT", "ARE", "KWT", "BHR", "OMN", "IRQ"}
    assert iran_israel["qatar_lng_shock"] is True
    assert iran_israel["country_fiscal_shock_usd"] == {"ISR": 11.5e9}

    india_pakistan = SCENARIOS["India-Pakistan Crisis: Renewed Escalation"]
    assert india_pakistan["conflict_affected"] == {"IND", "PAK"}
    assert india_pakistan["country_direct_fiscal_pct_gdp_shock"] == {"PAK": -0.0175}


def test_qatar_lng_shock_only_applies_to_qatar_and_only_when_flagged():
    scored = _scored_df_with_qatar_israel_india()
    energy = _energy_df_with_qatar_israel_india()

    result_off = compute_scenario_impact(scored, energy, scenario_key="Pakistan Sovereign Default")
    qat_off = result_off[result_off["country_code"] == "QAT"].iloc[0]
    assert qat_off["delta"] == pytest.approx(0.0, abs=1e-6)

    result_on = compute_scenario_impact(scored, energy, scenario_key="Iran-Israel-US War: Renewed Escalation")
    qat_on = result_on[result_on["country_code"] == "QAT"].iloc[0]
    # Qatar is a large net energy exporter (energy_import_dependency very
    # negative) so the oil-price windfall term is negative-risk (a benefit);
    # the real 17% LNG-capacity loss should still push its net fiscal
    # effect toward higher risk than a country with no such loss.
    sau_on = result_on[result_on["country_code"] == "SAU"].iloc[0]
    assert qat_on["fiscal_pts"] > sau_on["fiscal_pts"]


def test_israel_country_specific_usd_shock_scales_with_its_own_real_gdp():
    scored = _scored_df_with_qatar_israel_india()
    energy = _energy_df_with_qatar_israel_india()
    result = compute_scenario_impact(scored, energy, scenario_key="Iran-Israel-US War: Renewed Escalation")
    isr_row = result[result["country_code"] == "ISR"].iloc[0]
    # Israel's own real GDP in the synthetic frame is 5.5e11; the $11.5bn
    # shock is ~2.09% of that -- confirm it's actually being applied (a
    # meaningfully large fiscal_pts contribution), not silently dropped.
    assert isr_row["fiscal_pts"] > 5.0


def test_india_pakistan_scenario_hits_pakistan_harder_than_india():
    """Mirrors the real, documented 2025 asymmetry (Pakistan's KSE-30 fell
    7.2% in a day while India's Sensex barely moved) -- Pakistan carries a
    real, disclosed GDP-level shock (the Indus Waters Treaty suspension)
    that India does not."""
    scored = _scored_df_with_qatar_israel_india()
    energy = _energy_df_with_qatar_israel_india()
    result = compute_scenario_impact(scored, energy, scenario_key="India-Pakistan Crisis: Renewed Escalation")
    pak_delta = result[result["country_code"] == "PAK"].iloc[0]["delta"]
    ind_delta = result[result["country_code"] == "IND"].iloc[0]["delta"]
    assert pak_delta > ind_delta > 0
