from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit


def qft(n: int) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    for j in range(n):
        qc.h(j)
        for k in range(j + 1, n):
            qc.cp(np.pi / 2 ** (k - j), k, j)
    for j in range(n // 2):
        qc.swap(j, n - 1 - j)
    return qc


def qaoa_ring(n: int, p: int) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    qc.h(range(n))
    for layer in range(p):
        for j in range(n):
            qc.rzz(0.3 + 0.1 * layer, j, (j + 1) % n)
        for j in range(n):
            qc.rx(0.7 - 0.1 * layer, j)
    return qc


def linear_ansatz(n: int, reps: int) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    for r in range(reps):
        for j in range(n):
            qc.ry(0.1 * (r + 1), j)
            qc.rz(0.2 * (r + 1), j)
        for j in range(n - 1):
            qc.cx(j, j + 1)
    for j in range(n):
        qc.ry(0.5, j)
    return qc


def grover_iteration(n: int) -> QuantumCircuit:
    """One Grover iteration: phase oracle for |1...1> and the diffuser, each with a multi-controlled Z."""
    qc = QuantumCircuit(n)
    qc.h(range(n))
    for _ in range(2):
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)
        qc.h(range(n))
        qc.x(range(n))
    return qc


FAMILIES = {
    "qft": lambda n: qft(n),
    "qaoa_ring_p3": lambda n: qaoa_ring(n, 3),
    "linear_ansatz_r3": lambda n: linear_ansatz(n, 3),
    "grover_iteration": lambda n: grover_iteration(n),
}
