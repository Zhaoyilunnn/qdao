import copy
import logging
from typing import List, Optional

import numpy as np
from quafu.circuits.quantum_circuit import (
    ControlledGate,
    QuantumCircuit,
    QuantumGate,
    SingleQubitGate,
)



class QuafuCircuitHelper:
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
        """Get the number of qubits in the original circuit"""
        if not isinstance(self._circ, QuantumCircuit):
            raise ValueError("Please set circ")
        return self._circ.num

    @property
    def instructions(self):
        if not isinstance(self._circ, QuantumCircuit):
            raise ValueError("Please set circ")
        # FIXME: temporarily remove barrier like this
        # Needs better impl
        # TODO: For random circuit, no need to remove barrier
        # since it is not in the gate set. For qasm bench, needs better implementations

        # Return a gate sequence []
        return self._circ.gates

    def get_instr_qubits(self, instruction: QuantumGate):
        if isinstance(instruction, SingleQubitGate):
            return [instruction.pos]
        return instruction.pos

    def init_circ_from_sv(self, sv: np.ndarray):
        from qdao.simulator import QdaoSimObj

        if not isinstance(self._circ, QuantumCircuit):
            raise ValueError("Please set circ")
        return QdaoSimObj(sv, self._circ)

    def gen_sub_circ(
        self,
        instrs: List[QuantumGate],
        num_local: int,
        num_primary: int
    ):
        """Generate a sub circuit based on a list of circuit instructions
        We assume there's no conditional instructions and no measurement
        instructions

        Args:
            instrs (List[QuantumGate]): A list of instructions
        Return:
            QdaoCircuit
        """
        if not isinstance(self._circ, QuantumCircuit):
            raise ValueError("Please set self._circ")

        from qdao.circuit import QdaoCircuit

        # 1. Get the set of qubits
        qset = set(range(num_local))

        # instrs: a series of gates
        # [XGate, XGate, CXGate, RYGate, RXGate, RZGate, CZGate]

        for instr in instrs:
            for q in self.get_instr_qubits(instr):
                qset.add(q)

        # Fix qbit
        sub_circ = QuantumCircuit(num_primary)
        # Sorting []
        real_qubits = sorted(list(qset))

        assert len(real_qubits) <= num_primary

        qubit_map = {q: i for i, q in enumerate(real_qubits)}

        for instr in instrs:
            new_instr = copy.deepcopy(instr)
            if isinstance(instr, SingleQubitGate):
                new_pos = qubit_map[instr.pos]
            else:
                new_pos = [qubit_map[q] for q in instr.pos]
                if isinstance(instr, ControlledGate):
                    new_ctrls = [qubit_map[q] for q in instr.ctrls]
                    new_targs = [qubit_map[q] for q in instr.targs]
                    new_instr.ctrls = new_ctrls
                    new_instr.targs = new_targs

            new_instr.pos = new_pos
            sub_circ.add_gate(new_instr)
            logging.debug(
                "New_instr::pos::{}, real_qubits::{}".format(new_pos, real_qubits)
            )

        # logging.debug(sub_circ.draw_circuit())
        logging.info(
            "\nGenerated sub-circ, real_qubits::{}".format(real_qubits))
        return QdaoCircuit(sub_circ, real_qubits)
