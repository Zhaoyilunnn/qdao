import sys
import time

sys.path.append('.')

from utils.misc import profile
from qiskit import *
from mqt import ddsim


@profile
def main(qasm_file: str):
    circ = QuantumCircuit.from_qasm_file(qasm_file)
    backend = ddsim.DDSIMProvider().get_backend('statevector_simulator')
    job = execute(circ, backend, shots=1)
    result = job.result()

if __name__ == '__main__':
    qasm_file = sys.argv[1]
    st_time = time.time()
    main(qasm_file)
    print("ddqsim runs:: {}".format(time.time() - st_time))
