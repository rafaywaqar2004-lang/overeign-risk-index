# Independent Stata Validation

This folder holds the Stata counterpart to `../r-validation/`: the same two
checks (PCA redundancy across the 11 factors, and the six-crisis historical
backtest), reproduced in Stata rather than Python or R.

## Why this one is different from the R version

I (the AI assisting with this repo) don't have a Stata license and can't
execute Stata in the environment I work in, so unlike the R notebook, I
couldn't run this myself and commit real output. This `.do` file is written
and checked for correct Stata syntax, but it needs to actually be run by a
person with a Stata install for the output to mean anything as evidence.

That's a deliberate, honest split: the R validation is fully reproducible and
already run; this one is a script waiting for you to execute it, which is
exactly the point — the resulting log is real, hands-on Stata work, not
something generated on your behalf.

## Files

- `driver_history.dta`, `scored_history.dta` — the same panel data used
  everywhere else in this project, exported to Stata format (`pandas.to_stata`,
  format 118, compatible with Stata 15+).
- `validation.do` — the script. Reproduces the crisis-backtest deltas, runs
  Stata's native `pca` command across the 11 factors, and a panel structure
  check (`xtsum`) on the same data the planned sovereign distress model will
  use.

## How to run it

1. Open Stata (any recent version — the NetCourse 101 / 471 environment works).
2. `cd` to this folder.
3. `do validation.do`
4. Save the output: either run `log using validation_log.txt, text` before
   the script and `log close` after, or copy the Results window output into
   `validation_log.txt`.
5. Commit `validation_log.txt` alongside this `.do` file — that log is the
   actual evidence of having run this yourself, and it's what should be cited
   in an interview, not the `.do` file alone.

## What to check once you have output

- Do the crisis-backtest deltas match the R notebook's output exactly
  (Syria +22.0, Sri Lanka +13.9, Afghanistan +14.2, Pakistan +3.4, Egypt -0.7)?
  They should — same data, same arithmetic, third independent implementation.
- Does Stata's `pca` output agree with R's `prcomp()` on which factors load
  together on the first component? Minor sign flips on loadings are normal
  and don't indicate disagreement (PCA components are only defined up to
  sign) — compare magnitudes and which factors cluster, not the raw sign.
