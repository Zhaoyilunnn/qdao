# What is qdao
qdao is a **q**uantum **d**ata **a**ccess **o**ptimization framework. It leverages secondary storage to simulate large scale quantum circuits and minimizes the data movement between memory and secondary storage. The memory requirement of full state quantum circuit simulation grows exponentially with the number of qubits. For example, on a typical PC, simulate a circuit with more than 30 qubits can easily result in out-of-memory error. With qdao, the memory occupation of simulation is  completely under your control.

# Install

```BASH
# First clone this repo
pip install -r requirements.txt
pip install .
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

# Citation
```bib
@inproceedings{zhao2022q,
  title={Full State Quantum Circuit Simulation Beyond Memory Limit},
  author={Zhao, Yilun and Chen, Yu and Li, He and Wang, Ying and Chang, Kaiyan and Wang, Bingmeng and Li, Bing and Han, Yinhe},
  booktitle={2023 IEEE/ACM International Conference on Computer-Aided Design (ICCAD)},
  year={2023},
  organization={IEEE}
}
```

# Under Development
There are some key features to be supported in the future

 - [ ] GPU simulation
 - [ ] Noisy simulation

 
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTMwNDU3NzIwNV19
-->