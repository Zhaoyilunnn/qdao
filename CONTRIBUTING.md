# Contributing Guide

# Development
Fork this repository
```bash
pip install -r requirements.txt
pip install -e .
```

# Style
It is recommended to use [black](https://black.readthedocs.io/en/stable/) to unify the code style.

# Test

Install additional utilization package to profile the time consumption of key steps and enable running of unit tests.
```bash
cd qutils/
pip install .
cd -
```

Pass the following cases
```bash

# Test run on quafu backend
pytest -s -k test_run_quafu_any_qasm test/qdao/engine.py --nq 12 --np 10 --nl 8 --qasm random_12_9_max_operands_2_gen.qasm

# Test run on qiskit backend
pytest -s -k test_run_qiskit_any_qasm test/qdao/engine.py --qasm random_12_9_max_operands_2_gen.qasm --nq 12 --np 10 --nl 8
```

Command line options

 - `--qasm`: Test qasm file name under `benchmarks/qasm/` directory.
 - `--nq`: Number of qubits.
 - `--np`: Number of qubits in a compute unit.
 - `--nl`: Number of qubits in a storage unit.
 - `--device`: "CPU" or "GPU", now this is only enabled for qiskit backend.
 - `--sv_location`: "memory" or "disk", for GPU mode, it is recommended to use "memory".

It is encouraged to build similar unit test for newly supported backend.
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEzOTYwMTkzODEsMjA5MDIyNjA4OCwxOD
g5OTI0OTUyXX0=
-->
