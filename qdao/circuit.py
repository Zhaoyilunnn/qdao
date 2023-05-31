"""
This module provides methods to partition original circuit
into sub-circuits.
"""
import logging
from typing import Any, List

from qdao.qiskit.circuit import QiskitCircuitHelper
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

        return sub_circs


PARTITIONERS = {"baseline": BaselinePartitioner, "static": StaticPartitioner}


INITIALIZERS = {"qiskit": QiskitCircuitHelper, "quafu": QuafuCircuitHelper}


class PartitionerProvider:
    @classmethod
    def get_partitioner(
        cls,
        part_name: str,
        **configs,
    ):
        return PARTITIONERS[part_name](**configs)


class CircuitHelperProvider:
    @classmethod
    def get_helper(cls, backend_name: str, **props):
        return INITIALIZERS[backend_name](**props)
