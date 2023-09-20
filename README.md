[![Tests](https://github.com/Zhaoyilunnn/qdao/actions/workflows/unit_test.yml/badge.svg?branch=main)](https://github.com/Zhaoyilunnn/qdao/actions/workflows/unit_test.yml)
[![qiskit](https://img.shields.io/badge/qiskit%20community-8A2BE2)](https://qiskit.org/ecosystem)


---


<p align="center">
  <img alt="QDAO" src="assets/logo.svg" width="400" />
</p>


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

The following code snippet shows the basic usage of qdao. You can configure the `num_primary` parameter to reduce the memory occupation. In this example, a 28-qubit circuit (4 GB memory requirement) to configured to use only 1 GB memory (`num_primary=26`, i.e., $2^{26} * 16 \text{ Byte} = 1\text{ GB}$).
```Python
from qdao import Engine
from qiskit.circuit.random import random_circuit
from qiskit import transpile
from qiskit_aer import Aer

# Create a qiskit quantum circuit `circ`
circ = random_circuit(28, 20, measure=False)
backend = Aer.get_backend("aer_simulator")
circ = transpile(circ, backend=backend)

# `num_primary`: size of a compute unit
# `num_local`: size of a storage unit
eng = Engine(circuit=circ, num_primary=26, num_local=22)
eng.run()
```

To use GPU for simulation and use host memory to store the entire statevector, try following configurations
```Python
eng = Engine(circuit=circ, num_primary=26, num_local=22, sv_location="memory", device="GPU")
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
Setting smaller memory requirement leads to larger performance overhead. This can be more severe when using qiskit backend as setting initial statevector in qiskit incurs additional data copy, this problem is avoided in [pyquafu](https://github.com/ScQ-Cloud/pyquafu), although pyquafu is slower than qiskit.

<!--stackedit_data:
eyJoaXN0b3J5IjpbODI1MjA3MjgxLC0xNjQ3MjEyMzY0LC0zMD
Q1NzcyMDVdfQ==
-->
