"""
Tests for market_signals.py. Only the fully offline paths are exercised
here (no ACLED/UN Comtrade keys) -- this pins down the "never fabricate a
figure when data/credentials aren't there" contract that's the whole point
of this module, and a real bug this project already found and fixed: a
failed ACLED request used to look identical to a genuine zero-event result.
"""
import pandas as pd
import pytest

import market_signals as ms
from fetch_data import COUNTRIES


def test_comtrade_reporter_codes_cover_all_34_countries():
    missing = [code for code in COUNTRIES if code not in ms.COMTRADE_REPORTER_CODES]
    assert not missing, f"Missing UN Comtrade reporter codes for: {missing}"


def _fx_long_df(changes, country_code="PAK", start_year=2015):
    rows = [
        {"country_code": country_code, "indicator": "currency_depreciation_pct", "year": start_year + i, "value": v}
        for i, v in enumerate(changes)
    ]
    return pd.DataFrame(rows)


def test_exchange_rate_pressure_insufficient_history_is_honest():
    long_df = _fx_long_df([1.0, 2.0])  # fewer than min_years
    result = ms.exchange_rate_pressure(long_df, "PAK", min_years=4)
    assert result["available"] is False
    assert "reason" in result


def test_exchange_rate_pressure_computes_real_ratio():
    changes = [1.0, -1.0, 2.0, -2.0, 10.0]  # last value is the "latest", rest are history
    long_df = _fx_long_df(changes)
    result = ms.exchange_rate_pressure(long_df, "PAK", min_years=4)
    assert result["available"] is True
    assert result["latest_change_pct"] == pytest.approx(10.0)
    prior = pd.Series(changes[:-1])
    expected_vol = prior.std(ddof=1)
    assert result["volatility"] == pytest.approx(expected_vol)
    assert result["pressure_index"] == pytest.approx(abs(10.0) / expected_vol)


def test_exchange_rate_pressure_zero_variance_history_is_honest_not_divide_by_zero():
    long_df = _fx_long_df([2.0, 2.0, 2.0, 2.0, 5.0])
    result = ms.exchange_rate_pressure(long_df, "PAK", min_years=4)
    assert result["available"] is False


def test_acled_signal_without_credentials_reports_not_configured():
    result = ms.acled_signal("Pakistan", api_key=None, email=None)
    assert result["available"] is False
    assert result["status"] == "not_configured"


def test_acled_signal_failed_request_distinguished_from_zero_events(monkeypatch):
    """The exact bug this project fixed: fetch_acled_events returning ([],
    False) (a failed request) must NOT be reported the same way as a
    genuine zero-conflict-events result."""
    import fetch_data as fd

    def _fake_fetch(*args, **kwargs):
        assert kwargs.get("return_status") is True
        return [], False

    monkeypatch.setattr(fd, "fetch_acled_events", _fake_fetch)
    result = ms.acled_signal("Pakistan", api_key="fake-key", email="fake@example.com")
    assert result["available"] is False
    assert result["status"] == "error"


def test_acled_signal_genuine_zero_events_reports_available(monkeypatch):
    import fetch_data as fd
    monkeypatch.setattr(fd, "fetch_acled_events", lambda *a, **k: ([], True))
    result = ms.acled_signal("UAE", api_key="fake-key", email="fake@example.com")
    assert result["available"] is True
    assert result["counts"] == {30: 0, 90: 0, 365: 0}


def test_fetch_trade_hhi_without_key_reports_not_configured():
    result = ms.fetch_trade_hhi("PAK", api_key=None)
    assert result["available"] is False
    assert result["status"] == "not_configured"


def test_fetch_trade_hhi_unmapped_country_is_honest():
    result = ms.fetch_trade_hhi("ZZZ", api_key="fake-key")
    assert result["available"] is False


def test_bond_yield_signal_is_always_honest_na():
    for code in list(COUNTRIES)[:5]:
        result = ms.bond_yield_signal(code)
        assert result["available"] is False
        assert "reason" in result


def test_get_market_signals_never_raises_even_with_bad_inputs():
    empty_long_df = pd.DataFrame(columns=["country_code", "indicator", "year", "value"])
    signals = ms.get_market_signals(empty_long_df, "PAK", "Pakistan")
    assert set(signals.keys()) == {"fx_pressure", "acled", "trade_hhi", "bond_yield"}
    for sig in signals.values():
        assert "available" in sig


# ---------------------------------------------------------------------------
# Daily FX granularity (fx_daily_history.csv path), with annual fallback
# ---------------------------------------------------------------------------
def _fx_daily_df(rates, country_code="PAK", start_date="2026-08-01"):
    start = pd.Timestamp(start_date)
    rows = [
        {"date": (start + pd.Timedelta(days=i)).strftime("%Y-%m-%d"), "country_code": country_code,
         "currency_code": "PKR", "lcu_per_usd": rate}
        for i, rate in enumerate(rates)
    ]
    return pd.DataFrame(rows)


def test_exchange_rate_pressure_prefers_daily_when_enough_real_history():
    # 10 rates -> 9 real day-over-day pct changes, above MIN_DAILY_OBSERVATIONS (8).
    rates = [280.0, 280.5, 279.8, 281.0, 280.2, 279.9, 280.7, 281.5, 280.9, 285.0]
    fx_daily_df = _fx_daily_df(rates)
    long_df = _fx_long_df([1.0, 2.0])  # deliberately too little annual history to matter
    result = ms.exchange_rate_pressure(long_df, "PAK", fx_daily_df=fx_daily_df)
    assert result["available"] is True
    assert result["granularity"] == "daily"
    assert result["n_days"] == 10

    pct_changes = [(rates[i] - rates[i - 1]) / rates[i - 1] * 100 for i in range(1, len(rates))]
    expected_latest = pct_changes[-1]
    expected_vol = pd.Series(pct_changes[:-1]).std(ddof=1)
    assert result["latest_change_pct"] == pytest.approx(expected_latest)
    assert result["volatility"] == pytest.approx(expected_vol)
    assert result["pressure_index"] == pytest.approx(abs(expected_latest) / expected_vol)


def test_exchange_rate_pressure_falls_back_to_annual_with_too_little_daily_history():
    # Only 5 rates -> 4 real pct changes, below MIN_DAILY_OBSERVATIONS (8).
    fx_daily_df = _fx_daily_df([280.0, 280.5, 279.8, 281.0, 280.2])
    changes = [1.0, -1.0, 2.0, -2.0, 10.0]
    long_df = _fx_long_df(changes)
    result = ms.exchange_rate_pressure(long_df, "PAK", fx_daily_df=fx_daily_df, min_years=4)
    assert result["available"] is True
    assert result["granularity"] == "annual"


def test_exchange_rate_pressure_falls_back_to_annual_when_no_daily_data_at_all():
    changes = [1.0, -1.0, 2.0, -2.0, 10.0]
    long_df = _fx_long_df(changes)
    result = ms.exchange_rate_pressure(long_df, "PAK", fx_daily_df=None, min_years=4)
    assert result["available"] is True
    assert result["granularity"] == "annual"


def test_exchange_rate_pressure_ignores_other_countries_daily_rows():
    rates = [280.0, 280.5, 279.8, 281.0, 280.2, 279.9, 280.7, 281.5, 280.9, 285.0]
    fx_daily_df = _fx_daily_df(rates, country_code="EGY")  # not PAK
    changes = [1.0, -1.0, 2.0, -2.0, 10.0]
    long_df = _fx_long_df(changes, country_code="PAK")
    result = ms.exchange_rate_pressure(long_df, "PAK", fx_daily_df=fx_daily_df, min_years=4)
    assert result["granularity"] == "annual"


def test_exchange_rate_pressure_daily_zero_variance_falls_back_to_annual():
    fx_daily_df = _fx_daily_df([280.0] * 10)  # all pct changes are 0 -> zero volatility
    changes = [1.0, -1.0, 2.0, -2.0, 10.0]
    long_df = _fx_long_df(changes)
    result = ms.exchange_rate_pressure(long_df, "PAK", fx_daily_df=fx_daily_df, min_years=4)
    assert result["available"] is True
    assert result["granularity"] == "annual"


def test_pressure_level_thresholds():
    assert ms._pressure_level(0.5) == "Normal"
    assert ms._pressure_level(1.0) == "Elevated"
    assert ms._pressure_level(1.9) == "Elevated"
    assert ms._pressure_level(2.0) == "High"
