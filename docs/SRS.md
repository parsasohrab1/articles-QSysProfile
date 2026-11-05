# Software Requirements Specification – QSysProfile

- SR-1 `circuits`: generators for QFT (explicit controlled-phase construction), QAOA on a ring (p = 3), a linear-entanglement ansatz (3 repetitions) and one Grover iteration with multi-controlled Z.
- SR-2 `estimate.analytic_cx`: closed-form CX counts for the first three families; `fit_poly`/`predict_poly`: quadratic fits trained on n <= 8 and extrapolated; `rel_err`.
- SR-3 `research/run_study.py`: transpilation to cx, rz, sx, x at optimisation levels 0 and 3 (all-to-all) and level 1 on a line and a rectangular grid (5 seeds, means); log-log scaling exponent; extrapolation error of the polynomial fit.
- SR-4 Three unit tests (closed forms equal the unoptimised transpiled counts for n = 4, 5, 8).
