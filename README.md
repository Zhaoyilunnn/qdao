# qdao
Quantum Data Access Optimizaton

# Install

```BASH
# First clone this repo
pip install -r requirements.txt
pip install .
```

# Usage
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
`
<!--stackedit_data:
eyJoaXN0b3J5IjpbOTU1ODE2NTY3XX0=
-->