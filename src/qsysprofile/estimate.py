from __future__ import annotations

import numpy as np

BASIS = ["cx", "rz", "sx", "x"]


def analytic_cx(family: str, n: int) -> float | None:
    """Closed-form CX counts where the construction makes them exact (None where no formula is used)."""
    if family == "qft":
        return n * (n - 1) + 3 * (
            n // 2
        )  # n(n-1)/2 controlled phases (2 CX each) + n//2 swaps (3 CX each)
    if family == "qaoa_ring_p3":
        return 2 * n * 3  # n rzz per layer, 2 CX each (n>=3)
    if family == "linear_ansatz_r3":
        return (n - 1) * 3
    return None


def fit_poly(ns: np.ndarray, y: np.ndarray, deg: int = 2) -> np.ndarray:
    return np.polyfit(ns, y, deg)


def predict_poly(coef: np.ndarray, n: np.ndarray) -> np.ndarray:
    return np.polyval(coef, n)


def rel_err(pred: float, truth: float) -> float:
    return float(abs(pred - truth) / max(abs(truth), 1.0))
