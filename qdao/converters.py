"""Converters that convert np.array to statevector objects of other frameworks"""

import numpy as np
from qiskit.quantum_info.states import Statevector


class BaseConverter:
    def __init__(self) -> None:
        pass

    def convert(self):
        pass


class QiskitConverter(BaseConverter):
    def __init__(self, sv: np.ndarray) -> None:
        super().__init__()
        self._sv = sv

    def convert(self):
        return Statevector(self._sv)
