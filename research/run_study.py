"""Analytic / fitted resource estimates versus Qiskit transpilation (basis cx, rz, sx, x).

usage: python research/run_study.py
Simulation-only: circuits are generated, not run. Qiskit version is recorded in the output.
"""

import json
import warnings
from pathlib import Path

import numpy as np
import qiskit
from qiskit import transpile
from qiskit.transpiler import CouplingMap

from qsysprofile.circuits import FAMILIES
from qsysprofile.estimate import BASIS, analytic_cx, fit_poly, predict_poly, rel_err

warnings.filterwarnings("ignore")
NS = {
    "qft": [4, 6, 8, 10, 12, 16, 20],
    "qaoa_ring_p3": [4, 6, 8, 10, 12, 16, 20],
    "linear_ansatz_r3": [4, 6, 8, 10, 12, 16, 20],
    "grover_iteration": [4, 5, 6, 7, 8, 10, 12],
}
TRAIN_MAX = 8
SEEDS = range(5)


def grid_map(n: int) -> CouplingMap:
    w = int(np.ceil(np.sqrt(n)))
    h = int(np.ceil(n / w))
    cm = CouplingMap.from_grid(h, w)
    return cm


def stats(qc, **kw):
    t = transpile(qc, basis_gates=BASIS, **kw)
    ops = t.count_ops()
    return ops.get("cx", 0), t.depth()


def main():
    out = {
        "qiskit": qiskit.__version__,
        "note": "simulation-only; basis cx,rz,sx,x; routing results are means over 5 seeds",
        "families": {},
    }
    for fam, ns in NS.items():
        rows = []
        for n in ns:
            qc = FAMILIES[fam](n)
            cx0, _ = stats(qc, optimization_level=0)
            cx3, d3 = stats(qc, optimization_level=3, seed_transpiler=0)
            line = [
                stats(
                    qc,
                    coupling_map=CouplingMap.from_line(n),
                    optimization_level=1,
                    seed_transpiler=s,
                )
                for s in SEEDS
            ]
            gr = [
                stats(qc, coupling_map=grid_map(n), optimization_level=1, seed_transpiler=s)
                for s in SEEDS
            ]
            rows.append(
                {
                    "n": n,
                    "cx_level0": cx0,
                    "cx_level3": cx3,
                    "depth_level3": d3,
                    "analytic_cx": analytic_cx(fam, n),
                    "cx_line_mean": float(np.mean([a for a, _ in line])),
                    "depth_line_mean": float(np.mean([b for _, b in line])),
                    "cx_grid_mean": float(np.mean([a for a, _ in gr])),
                    "depth_grid_mean": float(np.mean([b for _, b in gr])),
                }
            )
        ns_a = np.array([r["n"] for r in rows])
        tr = ns_a <= TRAIN_MAX
        fit = {}
        for key in ("cx_level3", "cx_line_mean"):
            y = np.array([r[key] for r in rows], float)
            coef = fit_poly(ns_a[tr], y[tr], 2)
            errs = {
                str(int(n)): rel_err(float(predict_poly(coef, np.array([n]))[0]), float(yy))
                for n, yy in zip(ns_a[~tr], y[~tr], strict=True)
            }
            fit[key] = {"train_max_n": TRAIN_MAX, "extrapolation_rel_error": errs}
        # scaling exponent of the level-3 CX count (log-log slope over all n)
        slope = float(
            np.polyfit(np.log(ns_a), np.log([max(r["cx_level3"], 1) for r in rows]), 1)[0]
        )
        out["families"][fam] = {
            "rows": rows,
            "poly_extrapolation": fit,
            "cx_scaling_exponent": slope,
        }
        r_last = rows[-1]
        print(
            fam,
            "exp",
            round(slope, 2),
            "n",
            r_last["n"],
            "cx0",
            r_last["cx_level0"],
            "cx3",
            r_last["cx_level3"],
            "analytic",
            r_last["analytic_cx"],
            "line",
            r_last["cx_line_mean"],
            "grid",
            r_last["cx_grid_mean"],
            {
                k: {a: round(b, 3) for a, b in v["extrapolation_rel_error"].items()}
                for k, v in fit.items()
            },
        )
    Path(__file__).with_name("results.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
