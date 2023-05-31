"""
Generate the walk-through example circuit
Pleas run in qcs root directory
"""
import sys

sys.path.append(".")

import matplotlib.pyplot as plt
from qiskit import QuantumCircuit

from qdao.engine import Engine

if __name__ == "__main__":
    # circ_path = "qdao/benchmarks/qasm/random_8_5_max_operands_2_gen.qasm"
    circ_path = "qdao/benchmarks/qasm/random_5_2_max_operands_2_gen.qasm"
    circ = QuantumCircuit.from_qasm_file(circ_path)
    # Show and save original circuit
    fig = circ.draw(output="mpl")
    print(circ.draw(output="latex_source"))
    plt.show()
    plt.savefig("complete_circ.pdf")

    # engine = Engine(circuit=circ, num_primary=6, num_local=4)
    engine = Engine(circuit=circ, num_primary=4, num_local=1)

    sub_circs = engine._part.run(circ)

    for i, sc in enumerate(sub_circs):
        sc.circ.data.pop(-1)
        print(sc.real_qubits)
        print(sc.circ.draw(output="latex_source"))
        fig = sc.circ.draw(output="mpl")
        plt.show()
        plt.savefig("sub_circ-{}.pdf".format(i))
