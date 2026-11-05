# articles-QSysProfile

Resource estimation for quantum circuits: closed-form and fitted CNOT-count estimates versus the counts produced by the
Qiskit transpiler (basis cx, rz, sx, x), including the routing overhead on line and grid coupling maps. Circuits are generated, not run
(**simulation-only**, no hardware data). TRL 4.

```
pip install -e ".[dev]" && python -m pytest
python research/run_study.py   # writes research/results.json
```
