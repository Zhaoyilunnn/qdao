# Contributing Guide

# Development
Fork this repository
```bash
pip install -e .
```

# Style
It is recommended to use [black](https://black.readthedocs.io/en/stable/) to unify the code style.

# Test

## Use `pytest`

We have a [collection](https://github.com/Zhaoyilunnn/qcs) of qasm benchmarks for testing and experiment.

```bash
git clone https://github.com/Zhaoyilunnn/qcs.git
```


Pass the following cases
```bash

# Test run on quafu backend
pytest -s -k test_run_quafu_any_qasm tests/qdao/engine_test.py --nq 12 --np 10 --nl 8 --qasm random_12_9_max_operands_2_gen.qasm

# Test run on qiskit backend
pytest -s -k test_run_qiskit_any_qasm tests/qdao/engine_test.py --nq 12 --np 10 --nl 8 --qasm random_12_9_max_operands_2_gen.qasm
```

Command line options

 - `--qasm`: Test qasm file name under `benchmarks/qasm/` directory.
 - `--nq`: Number of qubits.
 - `--np`: Number of qubits in a compute unit.
 - `--nl`: Number of qubits in a storage unit.
 - `--device`: "CPU" or "GPU", now this is only enabled for qiskit backend.
 - `--sv_location`: "memory" or "disk", for GPU mode, it is recommended to use "memory".

It is encouraged to build similar unit test for newly supported backend.

## Use `tox`
Install [tox](https://tox.wiki/en/4.11.3/installation.html) following the official guidline.

```bash
tox run
```
