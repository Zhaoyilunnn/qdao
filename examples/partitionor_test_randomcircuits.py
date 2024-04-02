from qiskit import transpile
from qiskit.circuit.random import random_circuit
from qiskit_aer import Aer
from qiskit.qasm2 import dumps
from qdao import Engine
from quafu import QuantumCircuit
from qdao.circuit import (
    BasePartitioner,
    CircuitHelperProvider,
    QdaoCircuit,
    StaticPartitioner,
    UniQPartitioner,
    BaselinePartitioner,
)
import pandas as pd

data = {"qubit": [], "static-partitionor": [], "Uniq-partitioner": []}
for i in range(8, 26):
    for j in range(10):
        num_qubits = i
        num_primary = i - 4
        num_local = 0
        circ = random_circuit(num_qubits, i, measure=False, max_operands=2)
        backend = Aer.get_backend("aer_simulator")
        circ = transpile(circ, backend=backend)
        quafu_circ = QuantumCircuit(1)
        quafu_circ.from_openqasm(dumps(circ))
        eng = Engine(
            partitioner=StaticPartitioner(
                np=num_primary, nl=num_local, backend="quafu"
            ),
            circuit=quafu_circ,
            num_primary=num_primary,
            num_local=num_local,
            backend="quafu",
        )
        data["qubit"].append(i)
        data["static-partitionor"].append(eng.run())
        eng = Engine(
            partitioner=UniQPartitioner(np=num_primary, nl=num_local, backend="quafu"),
            circuit=quafu_circ,
            num_primary=num_primary,
            num_local=num_local,
            backend="quafu",
        )
        data["Uniq-partitioner"].append(eng.run())
df = pd.DataFrame(data)
df.to_csv("test_randomcircuit.csv", index=False)
