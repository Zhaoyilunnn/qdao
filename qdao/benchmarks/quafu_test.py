import sys
sys.path.append('.')

from quafu import simulate, QuantumCircuit
from utils.misc import profile

@profile
def main(qasm_file: str):
    f = open(qasm_file, 'r')
    qasm_str = f.read()
    circ = QuantumCircuit(1)
    circ.from_openqasm(qasm_str)
    f.close()
    sv = simulate(circ, output="state_vector").get_statevector()

if __name__ == '__main__':
    qasm_file = sys.argv[1]
    main(qasm_file)
