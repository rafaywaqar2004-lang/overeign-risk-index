*-----------------------------------------------------------------------
* MENASA Risk Monitor -- Independent Validation in Stata
*
* Reproduces the same two checks already validated in the app itself
* (Python) and independently in R (see ../r-validation/): the 11-factor
* PCA redundancy check, and the six-crisis historical backtest.
*
* This is the version YOU run yourself in Stata -- I cannot execute
* Stata here (no license in this environment), so this script is
* written and reviewed for correct syntax, but the actual output log
* below is what makes it real evidence of hands-on Stata work.
*
* How to run:
*   1. Open Stata
*   2. cd to this folder (stata-validation/)
*   3. do validation.do
*   4. Save the Results window output as validation_log.txt (or use
*      `log using validation_log.txt, text` before running, `log close`
*      after) and commit that log file alongside this .do file.
*-----------------------------------------------------------------------

clear all
set more off

*-----------------------------------------------------------------------
* 1. Independent historical crisis backtest
*    Recomputes each year-over-year risk_score delta directly from
*    scored_history.dta, independent of the app's own rendering code.
*-----------------------------------------------------------------------

use "scored_history.dta", clear

* Declare as panel data: country_code (string) needs a numeric id for
* xtset -- encode gives each country a stable numeric code.
encode country_code, gen(country_id)
xtset country_id year

display ""
display as text "=== Crisis backtest: year-over-year risk_score delta ==="
display ""

foreach pair in "SYR 2011 2012" "LKA 2021 2022" "AFG 2020 2021" ///
                "LBN 2019 2020" "PAK 2021 2022" "EGY 2021 2022" {
    local code : word 1 of `pair'
    local y0   : word 2 of `pair'
    local y1   : word 3 of `pair'

    quietly summarize risk_score if country_code == "`code'" & year == `y0'
    local prior = r(mean)
    quietly summarize risk_score if country_code == "`code'" & year == `y1'
    local curr = r(mean)
    local delta = `curr' - `prior'

    display as text "`code'  `y0' -> `y1':  " as result %6.1f `delta' " points"
}

*-----------------------------------------------------------------------
* 2. Independent PCA redundancy check
*    Stata's native `pca` command -- a genuinely different implementation
*    from both the app's numpy eigendecomposition and R's prcomp().
*-----------------------------------------------------------------------

use "driver_history.dta", clear

display ""
display as text "=== PCA redundancy check across the 11 factors (complete-case) ==="
display ""

pca debt_to_gdp current_account_pct_gdp reserves_months_imports gdp_growth ///
    inflation currency_depreciation_pct political_stability ///
    government_effectiveness rule_of_law regulatory_quality ///
    control_of_corruption, components(11)

* Displays eigenvalues, proportion of variance explained by each
* component, and factor loadings -- compare PC1's loadings directly
* against the app's stated result (governance factors clustering
* together at 0.38-0.45 each) and against the R notebook's prcomp()
* output in ../r-validation/validation.html.

screeplot

display ""
display as text "=== Governance-cluster pairwise correlations ==="
display ""
pwcorr rule_of_law control_of_corruption political_stability government_effectiveness, sig

*-----------------------------------------------------------------------
* 3. Panel structure check (xtsum) -- the same country-year panel the
*    planned EM Macro & Geopolitical Risk Engine's sovereign distress
*    model will build on directly.
*-----------------------------------------------------------------------

display ""
display as text "=== Panel structure (xtsum) ==="
display ""
encode country_code, gen(country_id)
xtset country_id year
xtsum debt_to_gdp current_account_pct_gdp gdp_growth inflation

display ""
display as text "=== End of validation script ==="
