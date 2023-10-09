import logging
from typing import Optional

import numpy as np
from qiskit_aer import Aer
from qdao.exceptions import QdaoError


class QiskitSimulator:
    def __init__(
        self,
        provider: Optional[str] = None,
        fusion: Optional[bool] = False,
        device: str = "CPU",
    ) -> None:
        if provider:
            if provider == "ddsim":
                from mqt import ddsim

                self._sim = ddsim.DDSIMProvider().get_backend("qasm_simulator")
        else:
            self._sim = Aer.get_backend("aer_simulator")

        self._sim.set_options(fusion_enable=fusion)
        self._sim.set_options(method="statevector")
        self._sim.set_options(device=device)

    def run(self, simobj) -> np.ndarray:
        res = self._sim.run(simobj.circ).result()
        if not res.success:
            raise QdaoError(
                f"Running simulation using qiskit failed due to: {res.status}"
            )
        try:
            sv = res.get_statevector().data
        except Exception as e:
            sv = np.zeros(1 << simobj.circ.num_qubits)
            logging.info(f"No state vector for this sub-circuit: {e}")
        return sv
