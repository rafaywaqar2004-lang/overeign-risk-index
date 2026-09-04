"""
Tests for fx_daily.py's accumulation/idempotency logic -- the part that
doesn't require a real network call. fetch_latest_rates() itself is
monkeypatched everywhere here; this file never hits the real
ExchangeRate-API endpoint.
"""
import pandas as pd
import pytest

import fx_daily


def test_country_currency_covers_all_countries_except_palestine():
    from fetch_data import COUNTRIES
    missing = [c for c in COUNTRIES if c not in fx_daily.COUNTRY_CURRENCY and c != "PSE"]
    assert not missing, f"Unexpectedly missing a currency mapping for: {missing}"
    assert "PSE" not in fx_daily.COUNTRY_CURRENCY  # no national currency -- real fact, not a gap


def test_main_appends_new_snapshot_to_empty_history(tmp_path, monkeypatch):
    history_file = tmp_path / "fx_daily_history.csv"
    monkeypatch.setattr(fx_daily, "FX_HISTORY_FILE", str(history_file))
    monkeypatch.setattr(fx_daily, "fetch_latest_rates", lambda retries=3: {"PKR": 280.5, "EGP": 48.1})

    fx_daily.main()

    df = pd.read_csv(history_file)
    assert set(df["country_code"]) == {"PAK", "EGY"}
    assert df.loc[df["country_code"] == "PAK", "lcu_per_usd"].iloc[0] == pytest.approx(280.5)


def test_main_is_idempotent_for_the_same_day(tmp_path, monkeypatch):
    history_file = tmp_path / "fx_daily_history.csv"
    monkeypatch.setattr(fx_daily, "FX_HISTORY_FILE", str(history_file))
    monkeypatch.setattr(fx_daily, "fetch_latest_rates", lambda retries=3: {"PKR": 280.5})

    fx_daily.main()
    first_len = len(pd.read_csv(history_file))

    # Second call same "day" should be a no-op even if rates differ.
    monkeypatch.setattr(fx_daily, "fetch_latest_rates", lambda retries=3: {"PKR": 999.0})
    fx_daily.main()
    second_len = len(pd.read_csv(history_file))

    assert first_len == second_len
    df = pd.read_csv(history_file)
    assert (df["lcu_per_usd"] == 999.0).sum() == 0


def test_main_records_nothing_and_does_not_crash_on_fetch_failure(tmp_path, monkeypatch):
    history_file = tmp_path / "fx_daily_history.csv"
    monkeypatch.setattr(fx_daily, "FX_HISTORY_FILE", str(history_file))
    monkeypatch.setattr(fx_daily, "fetch_latest_rates", lambda retries=3: {})

    fx_daily.main()  # must not raise

    assert not history_file.exists()


def test_main_records_missing_currencies_honestly_not_estimated(tmp_path, monkeypatch, capsys):
    history_file = tmp_path / "fx_daily_history.csv"
    monkeypatch.setattr(fx_daily, "FX_HISTORY_FILE", str(history_file))
    # Only return one currency out of the full mapping -- the rest are "missing" for today.
    monkeypatch.setattr(fx_daily, "fetch_latest_rates", lambda retries=3: {"PKR": 280.5})

    fx_daily.main()

    df = pd.read_csv(history_file)
    assert len(df) == 1
    assert df.iloc[0]["country_code"] == "PAK"
    captured = capsys.readouterr()
    assert "missing" in captured.out.lower() or "No rate returned" in captured.out
