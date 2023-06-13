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

# 前端 cirq
# 后端 qsim

# import cirq.ops.gate_operation as qsim_op
from cirq.ops.gate_operation import GateOperation


# qsim_op ->QuantumGate
# qsim_op.gate ->qsim_gate
#gate_kind = _cirq_gate_kind(qsim_gate)

class QsimCircuitHelper:

    def __init__(
        self,
        circ: Optional[Circuit] = None
    ) -> None:
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

        # 返回一个操作的迭代序列 []
        # 示例：
        # [cirq.H(cirq.LineQubit(0)), cirq.H(cirq.LineQubit(1)),
        #  cirq.H(cirq.LineQubit(2)), cirq.CZ(cirq.LineQubit(1), cirq.LineQubit(2))]
        self._circ.itrs = []
        for i in self._circ.all_operations():
            self._circ.itrs.append(i)

        return self._circ.itrs

    def get_instr_qubits(self, instruction: GateOperation):
        # QuantumGate 一个gate类
        # instruction.pos拿到量子门的操作行为
        return instruction.qubits

    def init_circ_from_sv(self, sv: np.ndarray):
        from qdao.simulator import QdaoSimObj
        if not isinstance(self._circ, Circuit):
            raise ValueError("Please set circ")
        return QdaoSimObj(sv, self._circ)

    def gen_sub_circ(
        self,
        instrs: List[GateOperation],
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

        if not isinstance(self._circ, Circuit):
            raise ValueError("Please set self._circ")

        # 1. Get the set of qubits
        qset = set(range(num_local))

        # instrs一系列gate
        # [XGate, XGate, CXGate, RYGate, RXGate, RZGate, CZGate]

        for instr in instrs:
            for q in self.get_instr_qubits(instr):
                # q的内容: q(0) q(1)
                # q.x q的编号
                qset.add(q.x)

        # 子电路的大小已经定死 num_primary
        sub_circ = cirq.Circuit()
        # sub_qubits 后续需要联系操作添加到sub_circ
        sub_qubits = cirq.LineQubit.range(num_primary)

        # 排序列表 []
        real_qubits = sorted(list(qset))

        assert len(real_qubits) <= num_primary

        qubit_map = {
            q: i
            for i, q in enumerate(real_qubits)
        }

        for instr in instrs:
            # 超出子电路的大小时，做一个跳出
            bind = False
            new_instr = copy.deepcopy(instr)
            new_pos = [qubit_map[q.x] for q in instr.qubits]
            # num_primary的大小约束
            # 0~(num_primary-1)
            for x in new_pos:
                if x > (num_primary-1):
                    bind = True  
                    break
            # 超出范围
            if bind:
                break  

            new_instr.pos = new_pos

            # 添加操作
            sub_circ.append(new_instr)

            logging.debug("New_instr::pos::{}, real_qubits::{}".format(
                new_pos, real_qubits))

        # logging.debug(sub_circ.draw_circuit())
        logging.info(
            "\nGenerated sub-circ, real_qubits::{}".format(real_qubits))

        return QdaoCircuit(sub_circ, real_qubits)
