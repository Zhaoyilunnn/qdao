"""
Quantum Circuit Module
===================================

This module provides methods to partition original circuit into sub-circuits.

Classes:
    QdaoCircuit: A wrapper for quantum circuits with associated real qubits.
    BasePartitioner: Abstract base class for circuit partitioning.
    BaselinePartitioner: Implements a naive circuit partitioning approach.
    StaticPartitioner: Partitioner that traverses operations in their original order.
    DependencyMatrix: Assists the UniQ partitioning algorithm.
    UniQPartitioner: Partitioner using the UniQ algorithm.
    PartitionerProvider: Provides partitioner instances based on configuration.
    CircuitHelperProvider: Provides circuit helper instances based on backend.

"""

import logging
from typing import Any, List

from qdao.qiskit.circuit import QiskitCircuitWrapper
from qdao.quafu.circuit import QuafuCircuitHelper


class QdaoCircuit:
    """
    A class to represent a quantum circuit along with its real qubits.

    Attributes:
        circ (Any): The underlying quantum circuit object.
        real_qubits (List[int]): List of real qubits associated with the circuit.
    """
    def __init__(self, circ: Any, real_qubits: List[int]) -> None:
        self._circ = circ
        self._real_qubits = real_qubits

    @property
    def circ(self) -> Any:
        """Gets the underlying quantum circuit."""
        return self._circ

    @circ.setter
    def circ(self, circ: Any):
        """Sets the underlying quantum circuit."""
        self._circ = circ

    @property
    def real_qubits(self) -> List[int]:
        """Gets the list of real qubits."""
        return self._real_qubits


class BasePartitioner:
    """
    Base class for circuit partitioning.

    Attributes:
        np (int): Number of partitions.
        nl (int): Number of layers.
        backend (str): The backend used for the partitioning process.
    """

    def __init__(self, np=4, nl=2, backend="qiskit") -> None:
        self._np = np
        self._nl = nl
        self._circ_helper = CircuitHelperProvider.get_helper(backend)

    @property
    def np(self):
        """Gets the number of partitions."""
        return self._np

    @np.setter
    def np(self, n):
        """Sets the number of partitions."""
        self._np = n

    @property
    def nl(self):
        """Sets the number of layers."""
        return self._nl

    @nl.setter
    def nl(self, n):
        """Sets the number of layers."""
        self._nl = n

    def run(self, circuit: Any) -> List[QdaoCircuit]:
        """
        Partitions the given circuit into sub-circuits.

        Args:
            circuit (Any): The quantum circuit to be partitioned.

        Returns:
            List[QdaoCircuit]: A list of partitioned sub-circuits.
        """
        sub_circs = []

        return sub_circs


class BaselinePartitioner(BasePartitioner):
    """A naive implementation of circuit partitioning."""

    def run(self, circuit: Any) -> List[QdaoCircuit]:
        """
        Runs the baseline partitioning algorithm on the given circuit.

        Args:
            circuit (Any): The quantum circuit to be partitioned.

        Returns:
            List[QdaoCircuit]: A list of partitioned sub-circuits.
        """
        # Set cicuit of circuit helper
        self._circ_helper.circ = circuit

        sub_circs = []

        qset = set()
        for instr in self._circ_helper.instructions:
            # Each instruction forms a new sub-circuit
            sub_circ = self._circ_helper.gen_sub_circ([instr], self._nl, self._np)
            sub_circs.append(sub_circ)
            logging.info("Find sub-circuit: {}, qubits: {}".format(sub_circ.circ, qset))
        return sub_circs


class StaticPartitioner(BasePartitioner):
    """Static Partitioner that traverses operations in the original order."""

    def run(self, circuit: Any) -> List[QdaoCircuit]:
        """
        Runs the static partitioning algorithm on the given circuit.

        Args:
            circuit (Any): The quantum circuit to be partitioned.

        Returns:
            List[QdaoCircuit]: A list of partitioned sub-circuits.
        """
        # Set cicuit of circuit helper
        self._circ_helper.circ = circuit

        sub_circs = []

        instrs = []
        qset = set()
        for instr in self._circ_helper.instructions:
            qs = set()
            for q in self._circ_helper.get_instr_qubits(instr):
                if q >= self._nl:
                    qs.add(q)

            if len(qset | qs) <= (self._np - self._nl):
                qset = qset | qs
                instrs.append(instr)
            else:
                sub_circ = self._circ_helper.gen_sub_circ(instrs, self._nl, self._np)
                sub_circs.append(sub_circ)
                logging.info(
                    "Find sub-circuit: {}, qubits: {}".format(sub_circ.circ, qset)
                )
                # FIXME: Here the instr's qubits size may exceed
                # (self._np - self._nl)
                instrs = [instr]
                qset = qs
        if instrs:
            sub_circ = self._circ_helper.gen_sub_circ(instrs, self._nl, self._np)
            sub_circs.append(sub_circ)
        logging.info("Find sub-circuit: {}, qubits: {}".format(sub_circ.circ, qset))
        return sub_circs


class DependencyMatrix:
    """To assist the Uniq partitioning algorithm

   
    A two-dimensional matrix is used to analyze the dependencies between quantum
    gates using a dynamic programming method. Based on these dependencies, a sub-circuit
    containing the maximum number of quantum gates that meet the specified requirements is generated.
    We define `op[i][j]` as the process of grouping all operators that involve qubit `j`
    are dependent on the first `i` quantum gates.

   Attributes:
        gate_num (int): Number of quantum gates in the circuit.
        qubit_num (int): Number of qubits in the circuit.
        result_bit (list): A 2D list storing qubit dependencies.
        result_op (list): A 2D list storing operator dependencies.
    """

    def __init__(
        self,
        qubit_num: int,
        gate_num: int,
    ) -> None:
        """Dependency matrix class constructorInitializes the dependency matrix.

        Instantiate a dependency matrix class based on the given number of qubits and
        quantum gates

         Args:
            qubit_num (int): Number of qubits in the circuit.
            gate_num (int): Number of quantum gates in the circuit.
        """
        self.gate_num = gate_num
        self.qubit_num = qubit_num

    def preprocessing_single_quantum_circuits(self, gate_index: int, gate_target: any):
        """
    Process a single quantum gate, adding it to the dependency matrix.

    Fill in the row of the dependency matrix corresponding to the quantum gate.
    For the qubit that the quantum gate acts on, combine the quantum gate sets
    of all target bits in the previous row, add them to the current quantum gate,
    and put them into the dependency matrix. Record the qubits that these quantum
    gates act on.

    Args:
        gate_index (int): An integer representing the index of the quantum gate being processed.
        gate_target (int or list): An integer or list representing the qubits that the quantum gate acts on.
    """
        if isinstance(gate_target, int):
            gate_target = [gate_target]
        for j in range(self.qubit_num):
            self.result_bit[gate_index + 1][j] += self.result_bit[gate_index][j]
            self.result_op[gate_index + 1][j] += self.result_op[gate_index][j]
            if j in gate_target:
                self.result_op[gate_index + 1][j].append(gate_index + 1)
                for k in gate_target:
                    self.result_bit[gate_index + 1][j] += self.result_bit[gate_index][k]
                    self.result_op[gate_index + 1][j] += self.result_op[gate_index][k]
                self.result_bit[gate_index + 1][j] = list(
                    set(self.result_bit[gate_index + 1][j])
                )
                self.result_op[gate_index + 1][j] = list(
                    set(self.result_op[gate_index + 1][j])
                )

    def preprocessing_quantum_circuits(self, ops: list):
        """Processes all quantum gates and adds them to the dependency matrix.
        Given a set of quantum gates, use the preprocessing_single_quantum_circuits function
        to put them all into the dependency matrix

        Args:
            ops (list): A list of quantum gate operations.
        """
        self.result_bit = [
            [[] for _ in range(self.qubit_num)] for _ in range(self.gate_num + 1)
        ]
        self.result_op = [
            [[] for _ in range(self.qubit_num)] for _ in range(self.gate_num + 1)
        ]
        for i in range(self.qubit_num):
            self.result_bit[0][i].append(i)
        for i in range(self.gate_num):
            self.preprocessing_single_quantum_circuits(i, ops[i].pos)

    def select_subcircuit(self, active_qubit_num: int) -> (List[int], int):
        """Find sub-lines that meet the requirements from the dependency matrix

        Given an active qubit, which is the maximum number of qubits in the desired
        subcircuit, find the set of quantum gates that is smaller than the active
        qubit and contains the most quantum gates from the dependency matrix.
        Returns a list containing the numbers of all quantum gates and the number
        of qubits these quantum gates act on.

        Args:
            active_qubit_num (int): The number of active qubits in the sub-circuit.

        Returns:
            List[int]: A list of gate indices forming the sub-circuit.
            int: The number of qubits in the sub-circuit.
        """
        qubit_num_subcircuit = 0
        gate_num_subcircuit = 0
        gate_list = []
        for i in range(self.gate_num):
            for j in range(self.qubit_num):
                if (
                    len(self.result_op[i + 1][j]) >= gate_num_subcircuit
                    and len(self.result_bit[i + 1][j]) <= active_qubit_num
                ):
                    gate_list = self.result_op[i + 1][j]
                    qubit_num_subcircuit = len(self.result_bit[i + 1][j])
                    gate_num_subcircuit = len(self.result_op[i + 1][j])
        return gate_list, qubit_num_subcircuit


class UniQPartitioner(BasePartitioner):
    """Partitioner using the UniQ algorithm.

    References:
        [1] https://ieeexplore.ieee.org/abstract/document/10045784/
    """

    def run(self, circuit: Any) -> List[QdaoCircuit]:
        """
        Runs the UniQ partitioning algorithm on the given circuit.

        Args:
            circuit (Any): The quantum circuit to be partitioned.

        Returns:
            List[QdaoCircuit]: A list of partitioned sub-circuits.
        """
        self._circ_helper.circ = circuit
        ops = []
        ops += self._circ_helper.instructions
        active = self._np
        m = self._circ_helper.circ.num
        sub_circs = []
        while len(ops) > 0:
            need_qubit = active
            instrs = []
            while need_qubit > 0 and len(ops) > 0:
                task = DependencyMatrix(m, len(ops))
                task.preprocessing_quantum_circuits(ops)
                # Since there is a gap between the number of qubits
                # selected in a single sub-circuit and the number of
                # active qubits required, generating a sub-circuit
                # requires multiple selections to minimize the number
                # of sub-circuits.
                gate_list, qubit_num_subcircuit = task.select_subcircuit(need_qubit)
                if qubit_num_subcircuit == 0:
                    break
                need_qubit -= qubit_num_subcircuit
                for i in range(len(ops), -1, -1):
                    if i + 1 in gate_list:
                        instrs.append(ops[i])
                        ops.pop(i)
            sub_circ = self._circ_helper.gen_sub_circ(instrs, self._nl, self._np)
            sub_circs.append(sub_circ)
        logging.info("Find sub-circuit: {}".format(sub_circ.circ))
        return sub_circs


PARTITIONERS = {
    "baseline": BaselinePartitioner,
    "static": StaticPartitioner,
    "uniq": UniQPartitioner,
}


INITIALIZERS = {"qiskit": QiskitCircuitWrapper, "quafu": QuafuCircuitHelper}


class PartitionerProvider:
    """
    Provides partitioner instances based on configuration.
    """
    @classmethod
    def get_partitioner(
        cls,
        name: str,
        **configs,
    ):
        return PARTITIONERS[name](**configs)


class CircuitHelperProvider:
    @classmethod
    def get_helper(cls, backend_name: str, **props):
        """
        Returns a circuit helper instance based on the specified backend.

        Args:
            backend (str): The backend to use (e.g., 'qiskit', 'quafu').

        Returns:
            Any: An instance of a circuit helper.
        """
        return INITIALIZERS[backend_name](**props)
