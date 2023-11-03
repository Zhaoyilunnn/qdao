from abc import ABC, abstractmethod, abstractproperty
import numpy as np


class BaseCircWrapper(ABC):
    """Base class of circuit wrapper for different backends"""

    @property
    @abstractmethod
    def num_qubits(self):
        """Number of qubits of the quantum circuit"""

    @property
    @abstractmethod
    def instructions(self):
        """List of instructions in the quantum circuit"""

    @abstractmethod
    def get_instr_qubits(self, instruction):
        """The qubit indices that current instruction act on"""

    @abstractmethod
    def init_circ_from_sv(self, sv: np.ndarray):
        """Set initial state vector of the quantum circuit"""

    @abstractmethod
    def gen_sub_circ(self, instrs, num_local, num_primary):
        """Generate a new subcircuit based on given list of instructions"""
