"""
Qiskit Simulator Module
========================

This module provides a `QiskitSimulator` class to interface with Qiskit's Aer simulator and other 
potential simulators. It includes methods for initialization and running simulations.

Modules:
--------
- logging: Provides logging capabilities.
- typing: Includes the Optional type hint.
- numpy: Handles numerical operations and arrays.
- qiskit_aer: Provides access to Qiskit's Aer simulator.
- qdao.exceptions: Contains custom exceptions for the quantum DAO (Qdao) module.

Classes:
--------
- QiskitSimulator: Interfaces with Qiskit simulators for running quantum circuit simulations.


"""
import logging
from typing import Optional

import numpy as np
from qiskit_aer import Aer
from qdao.exceptions import QdaoError


class QiskitSimulator:
    """
    A class to interface with Qiskit's Aer simulator and other potential simulators.

    Attributes:
    -----------
    _sim : Backend
        The backend simulator used for running quantum simulations.

    Methods:
    --------
    __init__(self, provider: Optional[str] = None, fusion: Optional[bool] = False, device: str = "CPU") -> None
        Initializes the simulator with the specified provider, fusion option, and device type.
    
    run(self, simobj) -> np.ndarray
        Runs a simulation on the provided simulation object and returns the resulting state vector.
    """
    def __init__(
        self,
        provider: Optional[str] = None,
        fusion: Optional[bool] = False,
        device: str = "CPU",
    ) -> None:
        """
        Initialize the QiskitSimulator.

        Args:
            provider (Optional[str]): The simulator provider to use (e.g., 'ddsim'). Defaults to None.
            fusion (Optional[bool]): Whether to enable fusion optimizations. Defaults to False.
            device (str): The device to use for simulation ('CPU' or 'GPU'). Defaults to 'CPU'.
        """
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
        """
        Run a simulation on the provided simulation object.

        Args:
            simobj: The simulation object containing the quantum circuit to simulate.

        Returns:
            np.ndarray: The resulting state vector from the simulation.

        Raises:
            QdaoError: If the simulation fails.
        """
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
