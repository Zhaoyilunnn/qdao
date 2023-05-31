import numpy as np
from quafu.simulators.simulator import simulate


class QuafuSimulator:
    def __init__(self) -> None:
        pass

    def run(self, simobj) -> np.ndarray:
        sv = simulate(
            simobj.circ, psi=simobj.objs[0], output="state_vector"
        ).get_statevector()

        # FIXME: Quafu will return sv less than QuantumCircuit size
        expected_sv_size = 1 << simobj.circ.num
        if sv.shape[0] < expected_sv_size:
            assert expected_sv_size % sv.shape[0] == 0

        # Calculate repeat number
        rep_num = expected_sv_size // sv.shape[0]
        if rep_num == 1:
            return sv
        return np.tile(sv, rep_num)
