"""
Pure-logic regression tests for compute_scores.py -- no network calls, no
CSV I/O against live data. These pin down the invariants this project has
already found and fixed real bugs in (see git history), so a future change
can't silently reintroduce one of them.
"""
import pandas as pd
import pytest

from compute_scores import (
    WEIGHTS, ECON_FACTORS, GOV_FACTORS,
    normalize_to_risk_0_100, compute_weighted_score, risk_tier,
)


def test_weights_sum_to_one():
    assert WEIGHTS["debt_to_gdp"] == pytest.approx(1 / 12)
    assert sum(WEIGHTS.values()) == pytest.approx(1.0)


def test_econ_and_gov_factors_partition_weights_evenly():
    """The Economic/Political Risk Index split (see app.py's "Composite,
    Split in Two" section) is only mathematically valid because each pillar
    is exactly 50% of the composite's weight -- this is the invariant that
    guarantees composite == 0.5*economic + 0.5*political below."""
    assert set(ECON_FACTORS) | set(GOV_FACTORS) == set(WEIGHTS.keys())
    assert set(ECON_FACTORS) & set(GOV_FACTORS) == set()
    assert sum(WEIGHTS[f] for f in ECON_FACTORS) == pytest.approx(0.5)
    assert sum(WEIGHTS[f] for f in GOV_FACTORS) == pytest.approx(0.5)


def test_normalize_higher_is_riskier():
    s = pd.Series([0.0, 50.0, 100.0])
    out = normalize_to_risk_0_100(s, higher_is_riskier=True)
    assert out.iloc[0] == 0
    assert out.iloc[1] == 50
    assert out.iloc[2] == 100


def test_normalize_lower_is_riskier_inverts():
    s = pd.Series([0.0, 50.0, 100.0])
    out = normalize_to_risk_0_100(s, higher_is_riskier=False)
    assert out.iloc[0] == 100
    assert out.iloc[2] == 0


def test_normalize_all_missing_returns_none():
    s = pd.Series([None, None, None])
    out = normalize_to_risk_0_100(s, higher_is_riskier=True)
    assert out.isna().all()


def test_normalize_no_variation_returns_none():
    """Every country tied at the same value has no cross-sectional signal to
    normalize against -- must not divide by zero or invent a score."""
    s = pd.Series([42.0, 42.0, 42.0])
    out = normalize_to_risk_0_100(s, higher_is_riskier=True)
    assert out.isna().all()


def test_compute_weighted_score_full_coverage_uses_raw_weights():
    row = {f: 50.0 for f in WEIGHTS}
    df = pd.DataFrame([row])
    score = compute_weighted_score(df)
    assert score.iloc[0] == pytest.approx(50.0)


def test_compute_weighted_score_rescales_for_missing_factors():
    """A country missing some factors must have the remaining weights
    rescaled to still sum to 100% -- never silently treated as 'safe' by
    letting the missing factors count as zero risk."""
    row = {f: None for f in WEIGHTS}
    row["debt_to_gdp"] = 100.0  # only one factor reported, at max risk
    df = pd.DataFrame([row])
    score = compute_weighted_score(df)
    assert score.iloc[0] == pytest.approx(100.0)


def test_compute_weighted_score_all_missing_returns_none():
    row = {f: None for f in WEIGHTS}
    df = pd.DataFrame([row])
    score = compute_weighted_score(df)
    assert score.iloc[0] is None


def test_economic_and_political_subscores_sum_to_composite():
    """The exact invariant the Country Deep Dive's "Composite, Split in Two"
    section and the Regional Overview's quadrant chart both depend on:
    composite == 0.5*economic + 0.5*political whenever both pillars have
    full coverage."""
    row = {f: 60.0 for f in WEIGHTS}
    df = pd.DataFrame([row])
    composite = compute_weighted_score(df).iloc[0]
    econ = compute_weighted_score(df[ECON_FACTORS]).iloc[0]
    gov = compute_weighted_score(df[GOV_FACTORS]).iloc[0]
    assert composite == pytest.approx(0.5 * econ + 0.5 * gov, abs=0.1)


@pytest.mark.parametrize("score,expected", [
    (0, "Lower Risk"),
    (32.9, "Lower Risk"),
    (33, "Moderate Risk"),
    (65.9, "Moderate Risk"),
    (66, "Higher Risk"),
    (100, "Higher Risk"),
])
def test_risk_tier_thresholds(score, expected):
    assert risk_tier(score) == expected


def test_risk_tier_none_is_insufficient_data():
    assert risk_tier(None) == "Insufficient data"
    assert risk_tier(float("nan")) == "Insufficient data"
