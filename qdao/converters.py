"""
Converters that convert np.array to statevector objects of other frameworks.

Classes:
    BaseConverter: Abstract base class for statevector converters.
    QiskitConverter: Converts np.ndarray to Qiskit Statevector.
"""

import numpy as np
from qiskit.quantum_info.states import Statevector


class BaseConverter:
    """
    Base class for statevector converters.
    """

    def __init__(self) -> None:
        """
        Initializes the BaseConverter.
        """
        pass

    def convert(self):
        """
        Abstract method to convert statevectors.

        This method should be implemented by subclasses.
        """
        pass


class QiskitConverter(BaseConverter):
    """
    Converts np.ndarray to Qiskit Statevector.

    Attributes:
        sv (np.ndarray): The numpy array representing the statevector.
    """

    def __init__(self, sv: np.ndarray) -> None:
        """
        Initializes the QiskitConverter with a statevector.

        Args:
            sv (np.ndarray): The numpy array representing the statevector.
        """
        super().__init__()
        self._sv = sv

    def convert(self) -> Statevector:
        """
        Converts the numpy array to a Qiskit Statevector.

        Returns:
            Statevector: The Qiskit Statevector object.
        """
        return Statevector(self._sv)
