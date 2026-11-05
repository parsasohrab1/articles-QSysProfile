import numpy as np
from qiskit import transpile

from qsysprofile.circuits import FAMILIES
from qsysprofile.estimate import BASIS, analytic_cx, fit_poly, predict_poly, rel_err


def _cx(qc):
    return transpile(qc, basis_gates=BASIS, optimization_level=0).count_ops().get("cx", 0)


def test_analytic_counts_match_unoptimised_transpilation():
    for fam in ("qft", "qaoa_ring_p3", "linear_ansatz_r3"):
        for n in (4, 5, 8):
            assert _cx(FAMILIES[fam](n)) == analytic_cx(fam, n), (fam, n)


def test_polynomial_extrapolation_exact_on_quadratic():
    ns = np.array([4, 6, 8, 10])
    y = 3 * ns**2 + 2 * ns + 1
    c = fit_poly(ns, y)
    assert abs(predict_poly(c, np.array([20]))[0] - (3 * 400 + 40 + 1)) < 1e-6
    assert rel_err(10.0, 10.0) == 0.0


def test_grover_circuit_builds_for_small_n():
    assert FAMILIES["grover_iteration"](4).num_qubits == 4
