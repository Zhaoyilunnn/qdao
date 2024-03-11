from typing import List, Optional

import numpy as np
from qiskit.circuit import CircuitInstruction, QuantumCircuit

from qdao.base_circuit_wrapper import BaseCircWrapper

# from .initializer import initialize
#
# QuantumCircuit.initialize = initialize


class QiskitCircuitWrapper(BaseCircWrapper):
    def __init__(self, circ: Optional[QuantumCircuit] = None) -> None:
        self._circ = circ or None

    @property
    def circ(self):
        return self._circ

    @circ.setter
    def circ(self, circ: QuantumCircuit):
        self._circ = circ

    @property
    def num_qubits(self):
        if not isinstance(self._circ, QuantumCircuit):
            raise ValueError("Please set circ")
        return self._circ.num_qubits

    @property
    def instructions(self):
        if not isinstance(self._circ, QuantumCircuit):
            raise ValueError("Please set circ")
        return self._circ.data

    def get_instr_qubits(self, instruction: CircuitInstruction):
        for q in instruction.qubits:
            yield q._index

    def init_circ_from_sv(self, sv: np.ndarray):
        """Initialize qiskit QuantumCircuit from given statevector

        Comments:
            1. Currently qiskit QuantumCircuit.initialize will
               append an initialize instruction at the end of
               the circuit, we need create a new instance and
               init from statevector at the begining
        """
        from qdao.simulator import QdaoSimObj

        from .data_preparation.initializer import Initialize

        if not isinstance(self._circ, QuantumCircuit):
            raise ValueError("Please set circ before initializing from sv!")

        nq = self._circ.num_qubits
        circ = QuantumCircuit(nq)
        # FIXME: To test the performance of qiskit, do not initialize
        circ.append(Initialize(sv), range(nq))
        circ.compose(self._circ, inplace=True)
        return QdaoSimObj(sv, circ)

    def gen_sub_circ(
        self, instrs: List[CircuitInstruction], num_local: int, num_primary: int
    ):
        """Generate a sub circuit based on a list of circuit instructions
        We assume there's no conditional instructions and no measurement
        instructions

        Args:
            instrs (List[CircuitInstruction]): A list of instructions
        Return:
            QdaoCircuit
        """
        if not isinstance(self._circ, QuantumCircuit):
            raise ValueError("Please set self._circ")

        from qdao.circuit import QdaoCircuit

        # 1. Get the set of qubits
        qset = set(range(num_local))
        for instr in instrs:
            for q in instr.qubits:
                qset.add(q._index)

        sub_circ = QuantumCircuit(num_primary)

        real_qubits = sorted(list(qset))

        assert len(real_qubits) <= num_primary

        qubit_map = {
            self._circ.qubits[q]: sub_circ.qubits[i] for i, q in enumerate(real_qubits)
        }

        for instr in instrs:
            op = instr.operation.copy()
            if len(instr.clbits) > 0:
                raise NotImplementedError(
                    "Currently not support measure/control operations"
                )
            qubits = [qubit_map[q] for q in instr.qubits]
            sub_instr = CircuitInstruction(op, qubits=qubits)
            sub_circ.append(sub_instr)

        sub_circ.save_state()
        return QdaoCircuit(sub_circ, real_qubits)
