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
