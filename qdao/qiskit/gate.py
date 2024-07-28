# This code is part of Qiskit.
#
# (C) Copyright IBM 2017.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Unitary Gate Module
====================

This module provides a `Gate` class to represent unitary gates in quantum circuits.
It includes methods for matrix conversion, exponentiation, control, and argument broadcasting.

Modules:
--------
- qiskit.circuit.exceptions: Contains exceptions related to quantum circuits.
- qiskit.circuit.parameterexpression: Handles parameter expressions in quantum circuits.
- .annotated_operation: Provides classes for annotated operations.
- .instruction: Defines the base `Instruction` class.

Classes:
--------
- Gate: Represents a unitary gate in a quantum circuit.

Methods:
--------
- __init__(self, name: str, num_qubits: int, params: list, label: str | None = None, duration: Any = None, unit: str = "dt")
    Create a new gate.
- to_matrix(self) -> np.ndarray
    Return a Numpy.array for the gate unitary matrix.
- power(self, exponent: float)
    Creates a unitary gate as `gate^exponent`.
- __pow__(self, exponent: float) -> "Gate"
    Allows exponentiation using the `**` operator.
- _return_repeat(self, exponent: float) -> "Gate"
    Returns a repeated version of the gate.
- control(self, num_ctrl_qubits: int = 1, label: str | None = None, ctrl_state: int | str | None = None, annotated: bool = False)
    Return the controlled version of itself.
- _broadcast_single_argument(qarg: list) -> Iterator[tuple[list, list]]
    Expands a single argument for broadcasting.
- _broadcast_2_arguments(qarg0: list, qarg1: list) -> Iterator[tuple[list, list]]
    Expands two arguments for broadcasting.
- _broadcast_3_or_more_args(qargs: list) -> Iterator[tuple[list, list]]
    Expands three or more arguments for broadcasting.
- broadcast_arguments(self, qargs: list, cargs: list) -> Iterable[tuple[list, list]]
    Validation and handling of the arguments and their relationships.
- validate_parameter(self, parameter: Any)
    Gate parameters should be int, float, or ParameterExpression.

"""

from __future__ import annotations

from typing import Iterable, Iterator

import numpy as np
from qiskit.circuit.exceptions import CircuitError
from qiskit.circuit.parameterexpression import ParameterExpression

from .annotated_operation import AnnotatedOperation, ControlModifier
from .instruction import Instruction


class Gate(Instruction):
    """Unitary gate."""

    def __init__(
        self,
        name: str,
        num_qubits: int,
        params: list,
        label: str | None = None,
        duration=None,
        unit="dt",
    ) -> None:
        """Create a new gate.

        Args:
            name (str): The Qobj name of the gate.
            num_qubits (int): The number of qubits the gate acts on.
            params (list): A list of parameters.
            label (str | None): An optional label for the gate.
            duration (Any): The duration of the gate.
            unit (str): The unit of the gate duration.
        """
        self.definition = None
        super().__init__(
            name, num_qubits, 0, params, label=label, duration=duration, unit=unit
        )

    # Set higher priority than Numpy array and matrix classes
    __array_priority__ = 20

    def to_matrix(self) -> np.ndarray:
        """Return a Numpy.array for the gate unitary matrix.

        Returns:
            np.ndarray: if the Gate subclass has a matrix definition.

        Raises:
            CircuitError: If a Gate subclass does not implement this method an
                exception will be raised when this base class method is called.
        """
        if hasattr(self, "__array__"):
            return self.__array__(dtype=complex)
        raise CircuitError(f"to_matrix not defined for this {type(self)}")

    def power(self, exponent: float):
        """Creates a unitary gate as `gate^exponent`.

        Args:
            exponent (float): Gate^exponent

        Returns:
            .library.UnitaryGate: To which `to_matrix` is self.to_matrix^exponent.

        Raises:
            CircuitError: If Gate is not unitary
        """
        # pylint: disable=cyclic-import
        from qiskit.circuit.library.generalized_gates.unitary import UnitaryGate
        from qiskit.quantum_info.operators import Operator

        return UnitaryGate(
            Operator(self).power(exponent), label=f"{self.name}^{exponent}"
        )

    def __pow__(self, exponent: float) -> "Gate":
        return self.power(exponent)

    def _return_repeat(self, exponent: float) -> "Gate":
        return Gate(
            name=f"{self.name}*{exponent}",
            num_qubits=self.num_qubits,
            params=self.params,
        )

    def control(
        self,
        num_ctrl_qubits: int = 1,
        label: str | None = None,
        ctrl_state: int | str | None = None,
        annotated: bool = False,
    ):
        """
        Return the controlled version of itself.

        Implemented either as a controlled gate (ref. :class:`.ControlledGate`)
        or as an annotated operation (ref. :class:`.AnnotatedOperation`).

         Args:
            num_ctrl_qubits (int): number of controls to add to gate (default: ``1``)
            label (str | None): optional gate label. Ignored if implemented as an annotated
                operation.
            ctrl_state (int | str | None): the control state in decimal or as a bitstring
                (e.g. ``'111'``). If ``None``, use ``2**num_ctrl_qubits-1``.
            annotated (bool): indicates whether the controlled gate can be implemented
                as an annotated gate.

        Returns:
            Controlled version of the given operation.

        Raises:
            QiskitError: unrecognized mode or invalid ctrl_state
        """
        if not annotated:
            # pylint: disable=cyclic-import
            from .add_control import add_control

            return add_control(self, num_ctrl_qubits, label, ctrl_state)

        else:
            return AnnotatedOperation(
                self,
                ControlModifier(num_ctrl_qubits=num_ctrl_qubits, ctrl_state=ctrl_state),
            )

    @staticmethod
    def _broadcast_single_argument(qarg: list) -> Iterator[tuple[list, list]]:
        """Expands a single argument.
        
        Args:
           qarg (list): List of qubit arguments.
        
        Returns:
            Iterator[tuple[list, list]]: Iterator of expanded arguments.   
           
        For example: [q[0], q[1]] -> [q[0]], [q[1]]
        """
        # [q[0], q[1]] -> [q[0]]
        #              -> [q[1]]
        for arg0 in qarg:
            yield [arg0], []

    @staticmethod
    def _broadcast_2_arguments(qarg0: list, qarg1: list) -> Iterator[tuple[list, list]]:
        """Expands two arguments for broadcasting.

        Args:
            qarg0 (list): First list of qubit arguments.
            qarg1 (list): Second list of qubit arguments.
        
        Returns:
            Iterator[tuple[list, list]]: Iterator of expanded arguments.    

        Raises:
            CircuitError: If the arguments cannot be combined.
        """
        if len(qarg0) == len(qarg1):
            # [[q[0], q[1]], [r[0], r[1]]] -> [q[0], r[0]]
            #                              -> [q[1], r[1]]
            for arg0, arg1 in zip(qarg0, qarg1):
                yield [arg0, arg1], []
        elif len(qarg0) == 1:
            # [[q[0]], [r[0], r[1]]] -> [q[0], r[0]]
            #                        -> [q[0], r[1]]
            for arg1 in qarg1:
                yield [qarg0[0], arg1], []
        elif len(qarg1) == 1:
            # [[q[0], q[1]], [r[0]]] -> [q[0], r[0]]
            #                        -> [q[1], r[0]]
            for arg0 in qarg0:
                yield [arg0, qarg1[0]], []
        else:
            raise CircuitError(
                f"Not sure how to combine these two-qubit arguments:\n {qarg0}\n {qarg1}"
            )

    @staticmethod
    def _broadcast_3_or_more_args(qargs: list) -> Iterator[tuple[list, list]]:
        """Expands three or more arguments for broadcasting.

        Args:
            qargs (list): List of lists of qubit arguments.
        
        Returns:
            Iterator[tuple[list, list]]: Iterator of expanded arguments.    
            
        Raises:
            CircuitError: If the arguments cannot be combined.    
        """    

        if all(len(qarg) == len(qargs[0]) for qarg in qargs):
            for arg in zip(*qargs):
                yield list(arg), []
        else:
            raise CircuitError(
                "Not sure how to combine these qubit arguments:\n %s\n" % qargs
            )

    def broadcast_arguments(
        self, qargs: list, cargs: list
    ) -> Iterable[tuple[list, list]]:
        """Validation and handling of the arguments and its relationship.

        For example, ``cx([q[0],q[1]], q[2])`` means ``cx(q[0], q[2]); cx(q[1], q[2])``. This
        method yields the arguments in the right grouping. In the given example::

            in: [[q[0],q[1]], q[2]],[]
            outs: [q[0], q[2]], []
                  [q[1], q[2]], []

        The general broadcasting rules are:

            * If len(qargs) == 1::

                [q[0], q[1]] -> [q[0]],[q[1]]

            * If len(qargs) == 2::

                [[q[0], q[1]], [r[0], r[1]]] -> [q[0], r[0]], [q[1], r[1]]
                [[q[0]], [r[0], r[1]]]       -> [q[0], r[0]], [q[0], r[1]]
                [[q[0], q[1]], [r[0]]]       -> [q[0], r[0]], [q[1], r[0]]

            * If len(qargs) >= 3::

                [q[0], q[1]], [r[0], r[1]],  ...] -> [q[0], r[0], ...], [q[1], r[1], ...]

        Args:
            qargs (list): List of quantum bit arguments.
            cargs (list): List of classical bit arguments.

        Returns:
            Iterable[tuple[list, list]]: A tuple with single arguments.

        Raises:
            CircuitError: If the input is not valid. For example, the number of
                arguments does not match the gate expectation.
        
        """
        if len(qargs) != self.num_qubits or cargs:
            raise CircuitError(
                f"The amount of qubit({len(qargs)})/clbit({len(cargs)}) arguments does"
                f" not match the gate expectation ({self.num_qubits})."
            )

        if any(not qarg for qarg in qargs):
            raise CircuitError("One or more of the arguments are empty")

        if len(qargs) == 0:
            return [
                ([], []),
            ]
        if len(qargs) == 1:
            return Gate._broadcast_single_argument(qargs[0])
        elif len(qargs) == 2:
            return Gate._broadcast_2_arguments(qargs[0], qargs[1])
        elif len(qargs) >= 3:
            return Gate._broadcast_3_or_more_args(qargs)
        else:
            raise CircuitError("This gate cannot handle %i arguments" % len(qargs))

    def validate_parameter(self, parameter):
        """Gate parameters should be int, float, or ParameterExpression

        Args:
            parameter (Any): Parameter to validate.

        Raises:
            CircuitError: If the parameter is invalid.
        """
        if isinstance(parameter, ParameterExpression):
            if len(parameter.parameters) > 0:
                return (
                    parameter  # expression has free parameters, we cannot validate it
                )
            if not parameter.is_real():
                msg = f"Bound parameter expression is complex in gate {self.name}"
                raise CircuitError(msg)
            return parameter  # per default assume parameters must be real when bound
        if isinstance(parameter, (int, float)):
            return parameter
        elif isinstance(parameter, (np.integer, np.floating)):
            return parameter.item()
        else:
            raise CircuitError(
                f"Invalid param type {type(parameter)} for gate {self.name}."
            )
