import copy
import logging
from typing import List, Optional

import numpy as np
import cirq

# from . import qsim

# from qsimcirq.qsim_circuit import (_translate_ControlledGate, QSimCircuit
#                                 )
from qdao.circuit import QdaoCircuit

from cirq.circuits import Circuit

# Frontend cirq
# Backend qsim

# import cirq.ops.gate_operation as qsim_op
from cirq.ops.gate_operation import GateOperation


# qsim_op ->QuantumGate
# qsim_op.gate ->qsim_gate
# gate_kind = _cirq_gate_kind(qsim_gate)


class QsimCircuitHelper:
    def __init__(self, circ: Optional[Circuit] = None) -> None:
        self._circ = circ or None
        self._circ.num = 0
        self._circ.itrs = []

    @property
    def circ(self):
        return self._circ

    @circ.setter
    def circ(self, circ: Circuit):
        self._circ = circ

    @property
    def num_qubits(self):
        if not isinstance(self._circ, Circuit):
            raise ValueError("Please set circ")

        self._circ.num = 0
        for i in self._circ.moments:
            print(i.operations)
            for j in i.qubits:
                print(j)
                self._circ.num += 1

        return self._circ.num

    @property
    def instructions(self):
        if not isinstance(self._circ, Circuit):
            raise ValueError("Please set circ")
        # FIXME: temporarily remove barrier like this
        # Needs better impl
        # TODO: For random circuit, no need to remove barrier
        # since it is not in the gate set. For qasm bench, needs better implementations

        # Return an iterator of an instruction []
        # Example:
        # [cirq.H(cirq.LineQubit(0)), cirq.H(cirq.LineQubit(1)),
        #  cirq.H(cirq.LineQubit(2)), cirq.CZ(cirq.LineQubit(1), cirq.LineQubit(2))]
        self._circ.itrs = []
        for i in self._circ.all_operations():
            self._circ.itrs.append(i)

        return self._circ.itrs

    def get_instr_qubits(self, instruction: GateOperation):
        # QuantumGate: gate class
        # instruction.pos: operation's behavior
        return instruction.qubits

    def init_circ_from_sv(self, sv: np.ndarray):
        from qdao.simulator import QdaoSimObj

        if not isinstance(self._circ, Circuit):
            raise ValueError("Please set circ")
        return QdaoSimObj(sv, self._circ)

    def gen_sub_circ(
        self, instrs: List[GateOperation], num_local: int, num_primary: int
    ):
        """Generate a sub circuit based on a list of circuit instructions
        We assume there's no conditional instructions and no measurement
        instructions

        Args:
            instrs (List[QuantumGate]): A list of instructions
        Return:
            QdaoCircuit
        """

        if not isinstance(self._circ, Circuit):
            raise ValueError("Please set self._circ")

        # 1. Get the set of qubits
        qset = set(range(num_local))

        # instrs: a series of gates
        # [XGate, XGate, CXGate, RYGate, RXGate, RZGate, CZGate]

        for instr in instrs:
            for q in self.get_instr_qubits(instr):
                # q: q(0) q(1)
                # q.x index of q
                qset.add(q.x)

        # Size of sub-circ is fixed at num_primary
        sub_circ = cirq.Circuit()
        # sub_qubits: corresponds to operations in a sub_circ
        sub_qubits = cirq.LineQubit.range(num_primary)

        # Sorting []
        real_qubits = sorted(list(qset))

        assert len(real_qubits) <= num_primary

        qubit_map = {q: i for i, q in enumerate(real_qubits)}

        for instr in instrs:
            # Check whether current circuit exceeds num_primary
            bind = False
            new_instr = copy.deepcopy(instr)
            new_pos = [qubit_map[q.x] for q in instr.qubits]
            # num_primary limitaion
            # 0~(num_primary-1)
            for x in new_pos:
                if x > (num_primary - 1):
                    bind = True
                    break
            # Out of bound
            if bind:
                break

            new_instr.pos = new_pos

            # Add an op
            sub_circ.append(new_instr)

            logging.debug(
                "New_instr::pos::{}, real_qubits::{}".format(new_pos, real_qubits)
            )

        # logging.debug(sub_circ.draw_circuit())
        logging.info("\nGenerated sub-circ, real_qubits::{}".format(real_qubits))

        return QdaoCircuit(sub_circ, real_qubits)
