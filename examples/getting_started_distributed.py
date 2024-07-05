from qiskit import transpile, QuantumCircuit
from qiskit.circuit.random import random_circuit
from qiskit.qasm2 import dumps
from qiskit_aer import Aer
from qdao import Engine
from mpi4py import MPI
from qdao import util
import math
import pickle
import logging
import os

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# logging.debug("This message should go to the log file")
# logging.info("So should this")
# logging.warning("And this, too")
# logging.error("And non-ASCII stuff, too, like? resund and Malm?")
# logging.critical("critical")


if not util.is_power_of_two(size):
    print("The number of processes must be a power of 2")
    raise SystemExit

if rank == 0:
    num_qubits = 6
    num_primary = int(num_qubits - math.log2(size))
    num_local = num_qubits - 4
    depth = 10
    # Create a qiskit quantum circuit `circ`
    circ = random_circuit(num_qubits, depth, measure=False, max_operands=2)
    backend = Aer.get_backend("aer_simulator")
    qasm_code = dumps(circ)
    with open("random_circuit1.qasm", "w") as file:
        file.write(qasm_code)
    with open("random_circuit.qasm", "r") as file:
        qasm_code_from_file = file.read()
    print(qasm_code_from_file)
    circ = QuantumCircuit.from_qasm_str(qasm_code_from_file)
    circ = transpile(circ, backend=backend)
    eng = Engine(circuit=circ, num_primary=num_primary, num_local=num_local)
    serialized_data = pickle.dumps(eng)
else:
    serialized_data = None
serialized_data = comm.bcast(serialized_data, root=0)
eng = pickle.loads(serialized_data)
cur_dir = os.path.abspath(__file__).rsplit("\\", 1)[0]
log_path = os.path.join(cur_dir, f"{rank}example.log")
os.makedirs(os.path.dirname(log_path), exist_ok=True)
if not os.path.exists(log_path):
    with open(log_path, "w") as file:
        pass

logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,
    filemode="w",
    format="%(levelname)s:%(asctime)s:%(message)s",
    datefmt="%Y-%d-%m %H:%M:%S",
)
# `num_primary`: size of a compute unit
# `num_local`: size of a storage unit
eng.run()
