from test.base import BaseTest
from typing import Any, Tuple

import numpy as np
from qiskit.quantum_info.states import Statevector


class QdaoBaseTest(BaseTest):

    def debug_run_quafu_circ(
            self,
            circ: Any,
            input_sv: np.ndarray,
            expected_sv: np.ndarray,
            pos_range: Tuple[int, int]
        ):
        """
        This function is used to debug quafu circuit result
        for each sub_circ

        Args:
            circ: Original Quafu quantum circuit
            input_sv: output sv from last sub_circ
            expected_sv: output sv from current sub_circ
                (the one to be checked)
            pos_range: Current sub_circ's operations indexes range
                in original circuit
        """
        from quafu.circuits.quantum_circuit import QuantumCircuit
        NUM = circ.num
        mock_circ = QuantumCircuit(NUM)

        for i in range(pos_range[0], pos_range[1]):
            mock_circ.add_gate(circ.gates[i])

        print("\n::::::::mock_circ::::::::\n")
        mock_circ.draw_circuit()

        from quafu.simulators.simulator import simulate

        actual_sv = simulate(mock_circ, psi=input_sv, output="state_vector").get_statevector()
        print(actual_sv.shape)
        print(expected_sv)
        print(actual_sv)
        assert Statevector(actual_sv).equiv(Statevector(expected_sv))
