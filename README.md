[![Tests](https://github.com/Zhaoyilunnn/qdao/actions/workflows/unit_test.yml/badge.svg?branch=main)](https://github.com/Zhaoyilunnn/qdao/actions/workflows/unit_test.yml)
[![qiskit](https://img.shields.io/badge/qiskit%20community-8A2BE2)](https://qiskit.org/ecosystem)

- [What is QDAO](#what-is-qdao)
- [Install](#install)
- [Testing](#testing)
- [Usage](#usage)
  * [Basic Usage](#basic-usage)
  * [GPU Simulation](#gpu-simulation)
  * [Backends](#backends)
  * [Get Simulation Results](#get-simulation-results)
- [Citation](#citation)
- [Development](#development)
- [Features](#features)
- [Limitations](#limitations)
  * [Short-Term Solutions](#short-term-solutions)
  * [Long-Term](#long-term)
- [Issues](#issues)


# What is qdao
qdao is a **q**uantum **d**ata **a**ccess **o**ptimization framework. It leverages secondary storage to simulate large scale quantum circuits and minimizes the data movement between memory and secondary storage. The memory requirement of full state quantum circuit simulation grows exponentially with the number of qubits. For example, on a typical PC, simulate a circuit with more than 30 qubits can easily result in out-of-memory error. With qdao, the memory occupation of simulation is  completely under your control.

# Install

```BASH
git clone https://github.com/Zhaoyilunnn/qdao.git
cd qdao
pip install .
```

# Testing
```BASH
pytest tests/
```

# Usage

## Basic Usage

The following example can be found in the `examples/` directory and more examples will be added in the future.

The following code snippet shows the basic usage of qdao. You can configure the `num_primary` parameter to reduce the memory occupation.

$\text{memory consumption} = 2^{\text{num-primary}} * 16 \text{ Byte}$

```Python
from qdao import Engine
from qiskit.circuit.random import random_circuit
from qiskit import transpile
from qiskit_aer import Aer

num_qubits = 12
num_primary = 10
num_local = 8

# Create a qiskit quantum circuit `circ`
circ = random_circuit(num_qubits, 10, measure=False, max_operands=2)
backend = Aer.get_backend("aer_simulator")
circ = transpile(circ, backend=backend)

# `num_primary`: size of a compute unit, i.e., $m$ in QDAO paper
# `num_local`: size of a storage unit, i.e., $t$ in QDAO paper
eng = Engine(circuit=circ, num_primary=num_primary, num_local=num_local)
eng.run()
```

## GPU Simulation

To use GPU for simulation and use host memory to store the entire statevector, try following configurations.

First you need to install `qiskit-aer-gpu`. Please refer to the [official document](https://github.com/Qiskit/qiskit-aer).

```Python
eng = Engine(circuit=circ, num_primary=num_primary, num_local=num_local, sv_location="memory", device="GPU")
```


## Backends

You can specify a backend simulator by using `backend` option, currently only qiskit and pyquafu are supported.

```Python
# First transform qiskit circuit to a quafu circuit
from quafu import QuantumCircuit
quafu_circ = QuantumCircuit(1)

# For qiskit < 1.0
quafu_circ.from_openqasm(circ.qasm())

# For qiskit >= 1.0, `qasm()` api has been deprecated.
from qiskit.qasm2 import dumps
quafu_circ.from_openqasm(dumps(circ))

# Create a new engine using quafu backend
eng = Engine(circuit=quafu_circ, num_primary=num_primary, num_local=num_local, backend="quafu")
eng.run()
```

## Get Simulation Results

We're working on to support measurement in qdao, currently please obtain state vector after simulation as follows.

```Python
from qdao.util import retrieve_sv
res = retrieve_sv(num_qubits, num_local=num_local)
print(res)
```

# Citation
If you find our work useful, please kindly cite our paper as below.
```bib
@inproceedings{qdao2023,
  title={Full State Quantum Circuit Simulation Beyond Memory Limit},
  author={Zhao, Yilun and Chen, Yu and Li, He and Wang, Ying and Chang, Kaiyan and Wang, Bingmeng and Li, Bing and Han, Yinhe},
  booktitle={2023 IEEE/ACM International Conference on Computer-Aided Design (ICCAD)},
  year={2023},
  organization={IEEE}
}
```

# Development

See the [CONTRIBUTING.md](https://github.com/Zhaoyilunnn/qdao/blob/main/CONTRIBUTING.md).

# Features
There are some key features to be supported in the future

 - [x] GPU simulation
 - [ ] Noisy simulation

# Limitations

When using qiskit backend, setting initial statevector in qiskit incurs significant overhead due To
1. Qiskit treats state vector as parameters and implements time-coonsuming validation logics, see https://github.com/Zhaoyilunnn/qdao/issues/14.
2. There exists additional data copy when submitting circuit with initial state vector to Aer. E.g., if you set 1 GB initial state vector, it actually consumes 2 GB memory during simulation.


## Short-Term Solutions

1. You can use the tagged stable version, which requires qiskit < 1.0 and we did some tricky modifications in qiskit to eliminate the validation overhead.

```bash

git checkout stable/0.1
pip install .
```

2. You can use `quafu` backend. Algthough itself is slower than Qiskit, it does not have the problems of qiskit when using QDAO. Indeed, QDAO-PyQuafu is faster than QDAO-Qiskit for large circuit (>=28 Qubits).

3. Since the additional overhead of qiskit is completely implementation issue, you might want to measure the ideal performance of QDAO-Qiskit. To do so, you could comment [this line](https://github.com/Zhaoyilunnn/qdao/blob/v0.1.0/qdao/qiskit/circuit.py#L58), which however leads to wrong simulations results.


## Long-Term

- We will implement a customized C++ high-performance backend and integrate it into QDAO. Please stay tuned.


# Issues
Please file an issue or contact zyilun8@gmail.com if you encounter any problems.
