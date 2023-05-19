import sys
sys.path.append('.')

from qiskit.circuit import QuantumCircuit
from qiskit_aer import Aer
from utils.misc import profile


@profile
def main(qasm_file: str):
    sim = Aer.get_backend('aer_simulator')
    sim.set_options(fusion_enable=False)
    circ = QuantumCircuit.from_qasm_file(qasm_file)
    circ.save_state()
    sim.run(circ)


if __name__ == '__main__':
    qasm_file = sys.argv[1]
    main(qasm_file)
