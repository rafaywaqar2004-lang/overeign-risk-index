"""
Regression tests for econometric_drivers.py's pure logic (panel prep,
regression fitting, Hausman test, code export). All network-dependent
fetches are stubbed with synthetic data -- these tests must run fully
offline and fast, matching this project's established test-stub pattern
(see the CI workflow, which never sets ACLED_API_KEY/UN Comtrade secrets
for this job on purpose).

test_max_year_tracks_current_year pins down a real bug this project shipped
and fixed: MAX_YEAR used to be hardcoded to 2024, which silently discarded
already-available 2025 data every time the Drivers Analysis panel was
assembled (see git history, "Fix Drivers Analysis panel to stop truncating
at a hardcoded 2024").
"""
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import pytest

import econometric_drivers as ed


def test_max_year_tracks_current_year_not_a_hardcoded_past_year():
    assert ed.MAX_YEAR >= datetime.now(timezone.utc).year
    assert ed.MAX_YEAR > 2024


def _synthetic_long_df(n_countries=8, start_year=2010, end_year=None, seed=0):
    end_year = end_year or ed.MAX_YEAR
    rng = np.random.default_rng(seed)
    countries = list(ed.COUNTRIES.items())[:n_countries]
    rows = []
    for code, name in countries:
        base = {col: rng.normal(0, 1) for col in ed.ALL_COLS}
        for year in range(start_year, end_year + 1):
            for col in ed.ALL_COLS:
                if col in ("trade_openness", "gov_expenditure"):
                    continue  # fetched separately by fetch_new_indicators_long, stubbed empty below
                rows.append({
                    "country_code": code, "country": name, "indicator": col,
                    "year": year, "value": base[col] + rng.normal(0, 0.3) + 0.05 * (year - start_year),
                })
    return pd.DataFrame(rows)


@pytest.fixture(autouse=True)
def _stub_network_fetches(monkeypatch):
    """Every test in this file runs fully offline."""
    monkeypatch.setattr(ed, "fetch_new_indicators_long", lambda: pd.DataFrame(
        columns=["country_code", "country", "indicator", "year", "value"]
    ))
    monkeypatch.setattr(ed, "_fetch_imf_datamapper_full_series", lambda *a, **k: {})


def test_build_panel_spans_min_year_to_max_year():
    long_df = _synthetic_long_df()
    panel, _fallback_counts = ed.build_panel(long_df)
    assert panel["year"].min() == ed.MIN_YEAR
    assert panel["year"].max() == ed.MAX_YEAR


def test_build_panel_does_not_fabricate_new_indicator_values():
    """trade_openness/gov_expenditure are stubbed to return nothing -- the
    panel must show them as genuinely missing (NaN), never zero-filled or
    otherwise invented."""
    long_df = _synthetic_long_df()
    panel, _ = ed.build_panel(long_df)
    assert panel["trade_openness"].isna().all()
    assert panel["gov_expenditure"].isna().all()


def test_variable_coverage_counts_match_manual_count():
    long_df = _synthetic_long_df()
    panel, _ = ed.build_panel(long_df)
    cov = ed.variable_coverage(panel, [ed.DV_COL])
    non_null, total, pct = cov[ed.DV_COL]
    assert non_null == int(panel[ed.DV_COL].notna().sum())
    assert total == len(panel)
    assert pct == pytest.approx(non_null / total * 100)


def test_full_regression_pipeline_runs_without_crashing():
    """End-to-end smoke test: build a panel, fit Pooled/FE/RE, run the
    Hausman test, and render the results table -- on a small but real
    (non-network) panel, matching what the Drivers Analysis tab does on
    every render."""
    ivs = ["debt_to_gdp", "gdp_growth", "inflation"]
    long_df = _synthetic_long_df(n_countries=10, end_year=ed.MIN_YEAR + 8)
    panel, _ = ed.build_panel(long_df)
    clean, n_total, n_dropped = ed.prepare_regression_frame(panel, ed.DV_COL, ivs)
    assert n_total == len(panel)
    assert len(clean) <= n_total

    n_entities = clean.index.get_level_values("country_code").nunique()

    pooled_res, pooled_err = ed.fit_pooled(clean, ed.DV_COL, ivs)
    fe_res, fe_err = ed.fit_fe(clean, ed.DV_COL, ivs)
    re_res, re_err = ed.fit_re(clean, ed.DV_COL, ivs)
    assert pooled_err is None and pooled_res is not None
    assert fe_err is None and fe_res is not None
    assert re_err is None and re_res is not None

    fe_entity_only, fe_entity_only_err = ed.fit_fe(clean, ed.DV_COL, ivs, time_effects=False)
    assert fe_entity_only_err is None
    hausman = ed.hausman_test(fe_entity_only, re_res)
    assert hausman is not None
    # A pseudo-inverse Hausman statistic can come out slightly negative on a
    # small/noisy panel when the variance-difference matrix isn't truly
    # positive semi-definite -- a documented limitation in hausman_test's own
    # docstring, not something this test should treat as a crash.
    assert np.isfinite(hausman["statistic"])
    assert 0 <= hausman["pvalue"] <= 1
    assert hausman["df"] == len(ivs)

    rows, labels = ed.results_table_rows(
        {
            "Pooled OLS": (pooled_res, pooled_err),
            "Fixed Effects": (fe_res, fe_err),
            "Random Effects": (re_res, re_err),
        },
        ivs, n_entities,
    )
    assert len(rows) > 0
    assert len(labels) == 3


def test_standardize_frame_zero_variance_column_does_not_crash():
    df = pd.DataFrame({"a": [1.0, 1.0, 1.0], "b": [1.0, 2.0, 3.0]})
    out = ed.standardize_frame(df, ["a", "b"])
    assert (out["a"] == 0.0).all()
    assert out["b"].std() == pytest.approx(1.0)


def test_generate_r_code_and_stata_code_reference_selected_ivs():
    ivs = ["debt_to_gdp", "gdp_growth"]
    r_code = ed.generate_r_code(ed.DV_COL, ivs)
    stata_code = ed.generate_stata_code(ed.DV_COL, ivs)
    for iv in ivs:
        assert iv in r_code
        assert iv in stata_code
    assert ed.DV_COL in r_code
    assert ed.DV_COL in stata_code
