# Independent R Validation

This folder reproduces the app's own two validation checks (the PCA redundancy
check and the six-crisis historical backtest) **independently, in R**, against
the same committed data files used by the live app (`driver_history.csv`,
`scored_history.csv`).

The point isn't to re-explain the Python result — it's a second, separately
written implementation (R's `prcomp()` and the `plm` package, rather than this
app's own `numpy`/`pandas` code) checked against the same data, to confirm the
finding holds up under independent computation rather than a single codebase's
own arithmetic.

## Files

- `validation.Rmd` — the R Markdown source. Open this to see exactly what's
  computed and how.
- `validation.html` — the rendered report, embedded live in the app's own
  Methodology tab ("Reproduced Independently in R").

## Re-running it

```bash
sudo apt-get install -y --no-install-recommends r-base-core r-cran-rmarkdown r-cran-knitr r-cran-plm pandoc
cd r-validation
Rscript -e "rmarkdown::render('validation.Rmd')"
```

This regenerates `validation.html` from the current data files — worth doing
whenever `driver_history.csv` or `scored_history.csv` meaningfully change, so
the embedded report doesn't quietly go stale relative to the live app above it.
