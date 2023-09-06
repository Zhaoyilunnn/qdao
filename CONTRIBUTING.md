# Contributing Guide

# Test

Install additional utilization package to profile the time consumption of key steps (Optional).
```bash
cd qutils/
pip install .
cd -
```

Pass the following cases
```bash

# Test run on quafu backend
cd qcs/
pytest -s -k test_run_quafu_any_qasm tst/qdao/engine.py --nq 12 --np 10 --nl 8 --qasm random_12_9_max_operands_2_gen.qasm

# Test run on qiskit backend
pytest -s -k test_run_qiskit_any_qasm tst/qdao/engine.py --qasm random_12_9_max_operands_2_gen.qasm --nq 12 --np 10 --nl 8
```

Command line options

 - `--qasm`: Test qasm file name under `benchmarks/qasm/` directory.
 - `--nq`: Number of qubits.
 - `--np`: Number of qubits in a compute unit.
 - `--nl`: Number of qubits in a storage unit.

It is encouraged to build similar unit test for newly supported backend. 
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTg4OTkyNDk1Ml19
-->