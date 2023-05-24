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

# pylint: disable=bad-docstring-quotes,invalid-name

"""Quantum circuit object."""

import copy
import functools
import itertools
import multiprocessing as mp
import re
import string
import typing
from collections import OrderedDict, defaultdict, namedtuple
from typing import (Callable, Dict, Iterable, List, Mapping, Optional,
                    Sequence, Set, Tuple, Type, TypeVar, Union)

from qiskit.circuit.classicalregister import ClassicalRegister, Clbit
from qiskit.circuit.exceptions import CircuitError
from qiskit.circuit.instruction import Instruction
from qiskit.circuit.instructionset import InstructionSet
from qiskit.circuit.operation import Operation
from qiskit.circuit.parameter import Parameter
from qiskit.circuit.quantumcircuitdata import CircuitInstruction
from qiskit.circuit.quantumregister import QuantumRegister, Qubit

# The following types are not marked private to avoid leaking this "private/public" abstraction out
# into the documentation.  They are not imported by circuit.__init__, nor are they meant to be.

# Arbitrary type variables for marking up generics.
S = TypeVar("S")
T = TypeVar("T")

# Types that can be coerced to a valid Qubit specifier in a circuit.
QubitSpecifier = Union[
    Qubit,
    QuantumRegister,
    int,
    slice,
    Sequence[Union[Qubit, int]],
]

# Types that can be coerced to a valid Clbit specifier in a circuit.
ClbitSpecifier = Union[
    Clbit,
    ClassicalRegister,
    int,
    slice,
    Sequence[Union[Clbit, int]],
]

# Generic type which is either :obj:`~Qubit` or :obj:`~Clbit`, used to specify types of functions
# which operate on either type of bit, but not both at the same time.
BitType = TypeVar("BitType", Qubit, Clbit)

# Regex pattern to match valid OpenQASM identifiers
VALID_QASM2_IDENTIFIER = re.compile("[a-z][a-zA-Z_0-9]*")


def _append_init_sv(self, instruction, qargs=None, cargs=None):
    """Append an instruction to the end of the circuit, modifying the circuit in place.

    .. warning::

        This is an internal fast-path function, and it is the responsibility of the caller to
        ensure that all the arguments are valid; there is no error checking here.  In
        particular, all the qubits and clbits must already exist in the circuit and there can be
        no duplicates in the list.

    .. note::

        This function may be used by callers other than :obj:`.QuantumCircuit` when the caller
        is sure that all error-checking, broadcasting and scoping has already been performed,
        and the only reference to the circuit the instructions are being appended to is within
        that same function.  In particular, it is not safe to call
        :meth:`QuantumCircuit._append` on a circuit that is received by a function argument.
        This is because :meth:`.QuantumCircuit._append` will not recognise the scoping
        constructs of the control-flow builder interface.

    Args:
        instruction: Operation instance to append
        qargs: Qubits to attach the instruction to.
        cargs: Clbits to attach the instruction to.

    Returns:
        Operation: a handle to the instruction that was just added

    :meta public:
    """
    old_style = not isinstance(instruction, CircuitInstruction)
    if old_style:
        instruction = CircuitInstruction(instruction, qargs, cargs)
    self._data.append(instruction)

    # FIXME: No need to do so when appending initializing
    # statevector instruction
    #if isinstance(instruction.operation, Instruction):
    #    self._update_parameter_table(instruction)

    # mark as normal circuit if a new instruction is added
    self.duration = None
    self.unit = "dt"
    return instruction.operation if old_style else instruction



def append_init_sv(
    self,
    instruction: Union[Operation, CircuitInstruction],
    qargs: Optional[Sequence[QubitSpecifier]] = None,
    cargs: Optional[Sequence[ClbitSpecifier]] = None,
) -> InstructionSet:
    """Append one or more instructions to the end of the circuit, modifying the circuit in
    place.

    The ``qargs`` and ``cargs`` will be expanded and broadcast according to the rules of the
    given :class:`~.circuit.Instruction`, and any non-:class:`.Bit` specifiers (such as
    integer indices) will be resolved into the relevant instances.

    If a :class:`.CircuitInstruction` is given, it will be unwrapped, verified in the context of
    this circuit, and a new object will be appended to the circuit.  In this case, you may not
    pass ``qargs`` or ``cargs`` separately.

    Args:
        instruction: :class:`~.circuit.Instruction` instance to append, or a
            :class:`.CircuitInstruction` with all its context.
        qargs: specifiers of the :class:`.Qubit`\\ s to attach instruction to.
        cargs: specifiers of the :class:`.Clbit`\\ s to attach instruction to.

    Returns:
        qiskit.circuit.InstructionSet: a handle to the :class:`.CircuitInstruction`\\ s that
        were actually added to the circuit.

    Raises:
        CircuitError: if the operation passed is not an instance of
            :class:`~.circuit..Instruction`.
    """
    if isinstance(instruction, CircuitInstruction):
        operation = instruction.operation
        qargs = instruction.qubits
        cargs = instruction.clbits
    else:
        operation = instruction
    # Convert input to instruction
    if not isinstance(operation, Operation) and not hasattr(operation, "to_instruction"):
        if issubclass(operation, Operation):
            raise CircuitError(
                "Object is a subclass of Operation, please add () to "
                "pass an instance of this object."
            )

        raise CircuitError(
            "Object to append must be an Operation or have a to_instruction() method."
        )
    if not isinstance(operation, Operation) and hasattr(operation, "to_instruction"):
        operation = operation.to_instruction()
    if not isinstance(operation, Operation):
        raise CircuitError("object is not an Operation.")

    # FIXME: No use when initializing statevector
    ## Make copy of parameterized gate instances
    #if hasattr(operation, "params"):
    #    is_parameter = any(isinstance(param, Parameter) for param in operation.params)
    #    if is_parameter:
    #        operation = copy.deepcopy(operation)

    expanded_qargs = [self.qbit_argument_conversion(qarg) for qarg in qargs or []]
    expanded_cargs = [self.cbit_argument_conversion(carg) for carg in cargs or []]

    if self._control_flow_scopes:
        appender = self._control_flow_scopes[-1].append
        requester = self._control_flow_scopes[-1].request_classical_resource
    else:
        appender = self._append_init_sv
        requester = self._resolve_classical_resource
    instructions = InstructionSet(resource_requester=requester)
    if isinstance(operation, Instruction):
        for qarg, carg in operation.broadcast_arguments(expanded_qargs, expanded_cargs):
            self._check_dups(qarg)
            instruction = CircuitInstruction(operation, qarg, carg)
            appender(instruction)
            instructions.add(instruction)
    else:
        # For Operations that are non-Instructions, we use the Instruction's default method
        for qarg, carg in Instruction.broadcast_arguments(
            operation, expanded_qargs, expanded_cargs
        ):
            self._check_dups(qarg)
            instruction = CircuitInstruction(operation, qarg, carg)
            appender(instruction)
            instructions.add(instruction)
    return instructions

