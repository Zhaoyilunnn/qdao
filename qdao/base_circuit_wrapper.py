from abc import ABC, abstractmethod
from typing import Any

import numpy as np


class BaseCircWrapper(ABC):
    """Base class of circuit wrapper for different backends"""

    @property
    @abstractmethod
    def num_qubits(self) -> Any:
        """Number of qubits of the quantum circuit"""

    @property
    @abstractmethod
    def instructions(self) -> Any:
        """List of instructions in the quantum circuit"""

    @abstractmethod
    def get_instr_qubits(self, instruction) -> Any:
        """The qubit indices that current instruction act on"""

    @abstractmethod
    def init_circ_from_sv(self, sv: np.ndarray) -> Any:
        """Set initial state vector of the quantum circuit"""

    @abstractmethod
    def gen_sub_circ(self, instrs, num_local, num_primary) -> Any:
        """Generate a new subcircuit based on given list of instructions"""
