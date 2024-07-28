"""
Simulator Provider Module
=========================

This module provides the `SimulatorProvider` class and associated objects for managing
and interacting with different quantum simulators. The simulators can be accessed through
a unified interface, making it easy to switch between different backend providers.

Modules:
--------

- qdao.qiskit.simulator: Contains the QiskitSimulator class.
- qdao.quafu.simulator: Contains the QuafuSimulator class.

Classes:
--------

- QdaoSimObj: Represents a simulation object containing the circuit and run options.
- SimulatorProvider: Provides access to different quantum simulators based on backend name.

Attributes:
-----------

- SIMS: A dictionary mapping backend names to their respective simulator classes.
"""

from qdao.qiskit.simulator import QiskitSimulator
from qdao.quafu.simulator import QuafuSimulator


class QdaoSimObj:
    """
    Simulation object for managing quantum circuits and run options.

    This class encapsulates the quantum circuit and any additional options required
    to run the simulation.

    Attributes:
        _objs (tuple): Tuple containing the simulation objects.
        _circ (Any): The quantum circuit object.
        _run_options (dict): Options for running the simulation.
    """

    def __init__(self, *objs, **options) -> None:
        """
        Initializes the QdaoSimObj with the provided objects and options.

        Args:
            objs (tuple): Simulation objects.
            options (dict): Run options for the simulation.
        """
        self._objs = objs
        self._circ = objs[-1]
        self._run_options = options

    @property
    def circ(self):
        """Returns the quantum circuit object."""
        return self._circ

    @property
    def objs(self):
        """Returns the simulation objects."""
        return self._objs

    @property
    def run_options(self):
        """Returns the run options for the simulation."""
        return self._run_options


SIMS = {"qiskit": QiskitSimulator, "quafu": QuafuSimulator}


class SimulatorProvider:
    """
    Provides access to different quantum simulators.

    This class allows the selection and initialization of a quantum simulator
    based on the specified backend name.

    Methods:
        get_simulator: Returns an instance of the specified simulator backend.

    Attributes:
        SIMS (dict): Dictionary mapping backend names to simulator classes.
    """

    @classmethod
    def get_simulator(cls, backend_name: str, **kwargs):
        """
        Returns an instance of the specified simulator backend.

        Args:
            backend_name (str): The name of the backend simulator.
            kwargs (dict): Additional arguments for the simulator.

        Returns:
            Simulator: An instance of the requested simulator backend.
        """
        return SIMS[backend_name](**kwargs)
