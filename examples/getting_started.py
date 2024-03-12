from qiskit import transpile
from qiskit.circuit.random import random_circuit
from qiskit_aer import Aer

from qdao import Engine

num_qubits = 12
num_primary = 10
num_local = 8

# Create a qiskit quantum circuit `circ`
circ = random_circuit(num_qubits, 10, measure=False, max_operands=2)
backend = Aer.get_backend("aer_simulator")
circ = transpile(circ, backend=backend)

# `num_primary`: size of a compute unit
# `num_local`: size of a storage unit
eng = Engine(circuit=circ, num_primary=num_primary, num_local=num_local)
eng.run()

# First transform qiskit circuit to a quafu circuit
from quafu import QuantumCircuit

quafu_circ = QuantumCircuit(1)

# For qiskit >= 1.0, `qasm()` api has been deprecated.
from qiskit.qasm2 import dumps

quafu_circ.from_openqasm(dumps(circ))

# For qiskit < 1.0
# quafu_circ.from_openqasm(circ.qasm())


# Create a new engine using quafu backend
eng = Engine(
    circuit=quafu_circ, num_primary=num_primary, num_local=num_local, backend="quafu"
)
eng.run()

from qdao.util import retrieve_sv

res = retrieve_sv(num_qubits, num_local=num_local)
print(res)
