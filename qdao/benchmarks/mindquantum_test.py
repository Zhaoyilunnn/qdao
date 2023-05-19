import sys
from mindquantum import Simulator
sys.path.append('.')
from mindquantum.io.qasm.openqasm import OpenQASM
from utils.misc import profile


@profile
def main(qasm_file: str):
    qasm = OpenQASM()
    circ = qasm.from_file(qasm_file)

    nq = circ.n_qubits
    sim = Simulator('mqvector', nq)
    sim.apply_circuit(circ)


if __name__ == '__main__':
    qasm_file = sys.argv[1]
    main(qasm_file)
