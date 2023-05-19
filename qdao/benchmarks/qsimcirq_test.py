import sys
sys.path.append('.')
import cirq
import qsimcirq

from cirq.contrib.qasm_import.qasm import circuit_from_qasm
from utils.misc import profile

# Pick a qubit.
#qubit = cirq.GridQubit(0, 0)

# Create a circuit
#circuit = cirq.Circuit(
#    cirq.X(qubit)**0.5,  # Square root of NOT.
#    cirq.measure(qubit, key='m')  # Measurement.
#)
#print("Circuit:")
#print(circuit)

@profile
def main(qasm_file: str):
    f = open(qasm_file, 'r')
    qasm_str = f.read()
    circuit = circuit_from_qasm(qasm_str)
    f.close()

    # Simulate the circuit several times.
    #simulator = cirq.Simulator()
    #result = simulator.run(circuit, repetitions=1)
    #print("Results:")
    #print(result)
    # Use eight threads to parallelize simulation.
    options = {'t': 8}

    qsim_simulator = qsimcirq.QSimSimulator(options)
    qsim_results = qsim_simulator.simulate(circuit)


if __name__ == '__main__':
    qasm_file = sys.argv[1]
    main(qasm_file)
