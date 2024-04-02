"""
This module provides methods to partition original circuit
into sub-circuits.
"""

import logging
import copy
from typing import Any, List

from qdao.qiskit.circuit import QiskitCircuitWrapper
from qdao.quafu.circuit import QuafuCircuitHelper


class QdaoCircuit:
    def __init__(self, circ: Any, real_qubits: List[int]) -> None:
        self._circ = circ
        self._real_qubits = real_qubits

    @property
    def circ(self) -> Any:
        return self._circ

    @circ.setter
    def circ(self, circ: Any):
        self._circ = circ

    @property
    def real_qubits(self) -> List[int]:
        return self._real_qubits


class BasePartitioner:
    """Base class of circuit partition"""

    def __init__(self, np=4, nl=2, backend="qiskit") -> None:
        self._np = np
        self._nl = nl
        self._circ_helper = CircuitHelperProvider.get_helper(backend)

    @property
    def np(self):
        return self._np

    @np.setter
    def np(self, n):
        self._np = n

    @property
    def nl(self):
        return self._nl

    @nl.setter
    def nl(self, n):
        self._nl = n

    def run(self, circuit: Any) -> List[QdaoCircuit]:
        sub_circs = []

        return sub_circs


class BaselinePartitioner(BasePartitioner):
    """This mimic the naive implementation"""

    def run(self, circuit: Any) -> List[QdaoCircuit]:
        # Set cicuit of circuit helper
        self._circ_helper.circ = circuit

        sub_circs = []

        qset = set()
        for instr in self._circ_helper.instructions:
            # Each instruction forms a new sub-circuit
            sub_circ = self._circ_helper.gen_sub_circ([instr], self._nl, self._np)
            sub_circs.append(sub_circ)
            logging.info("Find sub-circuit: {}, qubits: {}".format(sub_circ.circ, qset))
        print("----------BaselinePartitioner-----------")
        print("num of sub-circuits:" + str(len(sub_circs)))
        return sub_circs


class StaticPartitioner(BasePartitioner):
    """Static partitioner which traverse the operations in original order"""

    def run(self, circuit: Any) -> List[QdaoCircuit]:
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
        print("----------StaticPartitioner-----------")
        print("num of sub-circuits:" + str(len(sub_circs)))
        return sub_circs


class dptask:
    """To assist the Uniq partitioning algorithm"""

    def __init__(self, qubitNum: int, gateNum: int):
        self.gateNum = gateNum
        self.qubitNum = qubitNum

    def addGate(self, gateIndex: int, gatePos):
        if isinstance(gatePos, int):
            gatePos = [gatePos]
        for j in range(self.qubitNum):
            self.result_bit[gateIndex + 1][j] += self.result_bit[gateIndex][j]
            self.result_op[gateIndex + 1][j] += self.result_op[gateIndex][j]
            if j in gatePos:
                self.result_op[gateIndex + 1][j].append(gateIndex + 1)
                if len(gatePos) == 2:
                    a = [x for x in gatePos if x != j][0]
                    self.result_bit[gateIndex + 1][j] += self.result_bit[gateIndex][a]
                    self.result_bit[gateIndex + 1][j] = list(
                        set(self.result_bit[gateIndex + 1][j])
                    )
                    self.result_op[gateIndex + 1][j] += self.result_op[gateIndex][a]
                    self.result_op[gateIndex + 1][j] = list(
                        set(self.result_op[gateIndex + 1][j])
                    )

    def createTask(self, ops):
        self.result_bit = [
            [[] for _ in range(self.qubitNum)] for _ in range(self.gateNum + 1)
        ]
        self.result_op = [
            [[] for _ in range(self.qubitNum)] for _ in range(self.gateNum + 1)
        ]
        for i in range(self.qubitNum):
            self.result_bit[0][i].append(i)
        for i in range(self.gateNum):
            self.addGate(i, ops[i].pos)

    def selectSubCircuit(self, numSubcircuit: int) -> (list[int], int):
        """Find sub-lines that meet the requirements from the array in
        preprocessing. The return value is the number of bits representing
        the sub-circuit. When a sub-circuit that fails to obtain enough
        qubits is selected at one time, the return value can be used for
        the next selection."""
        numQubit = 0
        numOp = 0
        opList = []
        bitList = []
        for i in range(self.gateNum):
            for j in range(self.qubitNum):
                if (
                    len(self.result_op[i + 1][j]) >= numOp
                    and len(self.result_bit[i + 1][j]) <= numSubcircuit
                ):
                    opList = self.result_op[i + 1][j]
                    bitList = self.result_bit[i + 1][j]
                    numQubit = len(self.result_bit[i + 1][j])
                    numOp = len(self.result_op[i + 1][j])
        return (opList, numQubit)


class UniQPartitioner(BasePartitioner):
    """Partitioner in UniQ"""

    def run(self, circuit: Any) -> List[QdaoCircuit]:
        self._circ_helper.circ = circuit
        ops = copy.deepcopy(self._circ_helper.instructions)
        active = self._np
        m = self._circ_helper.circ.num
        sub_circs = []
        while len(ops) != 0:
            needQubit = active
            instrs = []
            while needQubit != 0 and len(ops) != 0:
                task = dptask(m, len(ops))
                task.createTask(ops)
                opList, numQubit = task.selectSubCircuit(needQubit)
                if numQubit == 0:
                    break
                needQubit -= numQubit
                for i in range(len(ops), -1, -1):
                    if i + 1 in opList:
                        instrs.append(ops[i])
                        ops.pop(i)
            sub_circ = self._circ_helper.gen_sub_circ(instrs, self._nl, self._np)
            sub_circs.append(sub_circ)
        print("----------UniqPartitioner-----------")
        print("num of sub-circuits:" + str(len(sub_circs)))
        return sub_circs


PARTITIONERS = {"baseline": BaselinePartitioner, "static": StaticPartitioner}


INITIALIZERS = {"qiskit": QiskitCircuitWrapper, "quafu": QuafuCircuitHelper}


class PartitionerProvider:
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
        return INITIALIZERS[backend_name](**props)
