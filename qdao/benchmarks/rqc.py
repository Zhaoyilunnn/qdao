import sys
import time
from qiskit.circuit import QuantumCircuit

from qiskit.compiler import transpile
from qiskit_aer import Aer

#from qdao.test import QdaoBaseTest
#from qdao.engine import Engine
#
#from utils.misc import profile
#
#TEST_BASE = QdaoBaseTest()
#
#
#@profile
#def run_base(circ: QuantumCircuit):
#    TEST_BASE._sv_sim.run(circ)
#
#@profile
#def run_qdao(circ: QuantumCircuit):
#    eng = Engine(circuit=circ, num_primary=circ.num_qubits-2, num_local=20)
#    eng.run()
#
#def main():
#    circ = TEST_BASE.get_qiskit_circ("random", num_qubits=30, depth=10, measure=False)
#    circ = transpile(circ, TEST_BASE._sv_sim)
#
#    run_base(circ)
#
#    run_qdao(circ)



if __name__ == '__main__':
    #main()
    from qiskit.circuit.random.utils import random_circuit

    # Number of qubits
    n = int(sys.argv[1])

    # Depth
    d = int(sys.argv[2])

    sim = Aer.get_backend("aer_simulator")
    circ = random_circuit(n, d, max_operands=2, measure=False)

    circ = transpile(circ, sim)
    file_name = "qasm/rqc_n{}_d{}.qasm".format(n, d)
    with open(file_name, 'w') as f:
        f.write(circ.qasm())
