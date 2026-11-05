# TRL assessment – QSysProfile

**Claimed level: TRL 4** (simulation-based). Not TRL 5: no device, no calibration data, one transpiler version (Qiskit 2.6.2).

CX counts at the largest size of each family (n = 20; Grover n = 12). "Level 0/3" = transpiler optimisation level on all-to-all connectivity; grid and line = level 1 on that coupling map (mean of 5 seeds, overhead against level 3). Last column: largest relative error of a quadratic fit trained on n <= 8 when extrapolated to the larger sizes (all-to-all / line).

| Family | n | Closed form | Level 0 | Level 3 | Grid | Line | Scaling exponent | Fit extrapolation error |
|---|---|---|---|---|---|---|---|---|
| qft | 20 | 410 | 410 | 350 | 833 (2.4x) | 1237 (3.5x) | 2.11 | 0.086 / 0.233 |
| qaoa_ring_p3 | 20 | 120 | 120 | 120 | 120 (1.0x) | 297 (2.5x) | 1.00 | 0.000 / 0.453 |
| linear_ansatz_r3 | 20 | 57 | 57 | 57 | 57 (1.0x) | 57 (1.0x) | 1.14 | 0.000 / 0.000 |
| grover_iteration | 12 | n/a | 884 | 880 | 1723 (2.0x) | 2357 (2.7x) | 3.08 | 0.011 / 0.046 |

## Findings and caveats
- The closed forms equal the unoptimised transpiled counts exactly (tests, n = 4, 5, 8; and the table). They are therefore only as good as the assumption that the transpiler does not optimise: for QFT the optimiser removes 60 of 410 CX at n = 20 (15 %), so the closed form over-estimates by 17 % at the highest optimisation level.
- QAOA on a ring and the linear ansatz are not changed by optimisation; the ring maps onto the grid without any extra CX, but costs 2.5x more CX on a line (the closing edge needs SWAPs).
- Routing overhead is large for dense circuits: QFT needs 2.4x (grid) and 3.5x (line) the all-to-all CX count at n = 20.
- A quadratic fit from n <= 8 predicts the optimised all-to-all counts well (<= 9 % for QFT, 0 % for the sparse families, 1 % for Grover at n <= 12), but extrapolates the routed (line) counts badly for QFT and the ring (up to 23 % and 45 % at n = 20) because routing overhead is not polynomial of that low degree.
- Grover with ancilla-free multi-controlled gates scales as n^3 in this range; results depend on the transpiler version and its stochastic router (seeds averaged).
