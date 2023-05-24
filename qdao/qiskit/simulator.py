import logging
from typing import Optional

import numpy as np
from mqt import ddsim
from qiskit_aer import Aer


class QiskitSimulator:

    def __init__(
            self,
            provider: Optional[str]=None,
            fusion: Optional[bool]=False
        ) -> None:
        if provider:
            if provider == 'ddsim':
                self._sim = ddsim.DDSIMProvider().get_backend('qasm_simulator')
        else:
            self._sim = Aer.get_backend("aer_simulator")

        self._sim.set_options(fusion_enable=fusion)
        self._sim.set_options(method='statevector')

    def run(self, simobj) -> np.ndarray:

        res = self._sim.run(simobj.circ).result()
        try:
            sv = res.get_statevector().data
        except Exception as e:
            sv = np.zeros(1<<simobj.circ.num_qubits)
            logging.info(f"No state vector for this sub-circuit: {e}")
        return sv

