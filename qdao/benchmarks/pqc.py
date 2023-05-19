import sys
from qiskit.circuit.library import NLocal, EvolvedOperatorAnsatz
from qiskit import transpile
from qiskit.opflow import X, Y, Z, I, MatrixEvolution
from qiskit_aer import Aer


###TODO: Delete this file


def DummyPqc(
        N: int,
        D: int
    ):
    """
    Create a parameterized quantum circuit using NLocal module

    Args:
        N: Number of qubits
        D: Number of repetition
    """
    #qc = NLocal(N, reps=D)
    ops = [Z ^ N, Y ^ N, X ^ N]
    evo = EvolvedOperatorAnsatz(ops, 2)
    #evo.parameter_bounds
    print(evo.parameters)
    return evo


if __name__ == '__main__':
    sim = Aer.get_backend("aer_simulator")
    N = int(sys.argv[1])
    D = int(sys.argv[2])
    output = sys.argv[3]

    qc = DummyPqc(N, D)
    qc = transpile(qc, sim)
    with open(output, 'w') as f:
        f.write(qc.qasm())


