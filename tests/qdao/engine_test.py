import os
from time import time

import numpy as np
import pytest
from qiskit import QuantumCircuit, qiskit
from qiskit.compiler import transpile
from qiskit.qasm2 import dumps
from qiskit.quantum_info import Statevector

from constants import *
from qdao.circuit import BaselinePartitioner
from qdao.engine import Engine
from qdao.simulator import QdaoSimObj
from qdao.util import retrieve_sv
from tests.qdao import QdaoBaseTest


class TestEngine(QdaoBaseTest):
    def setup_method(self):
        if not os.path.exists("qcs"):
            os.system(f"git clone {QCS_URL} qcs")

    def run_qiskit_diff_test(
        self,
        circ: QuantumCircuit,
        NQ: int,
        NP: int,
        NL: int,
        mode: str = "QDAO",
        is_parallel: bool = True,
        is_diff: bool = True,
        sv_location: str = "disk",
        device: str = "CPU",
    ):
        if mode == "QDAO":
            engine = Engine(
                circuit=circ,
                num_primary=NP,
                num_local=NL,
                backend="qiskit",
                is_parallel=is_parallel,
                sv_location=sv_location,
                device=device,
            )
        elif mode == "BASELINE":
            engine = Engine(
                circuit=circ,
                num_primary=NP,
                num_local=NL,
                backend="qiskit",
                partitioner=BaselinePartitioner(np=NP, nl=NL, backend="qiskit"),
                is_parallel=is_parallel,
            )
        else:
            raise ValueError(
                f"Unsupported mode::{mode}, should be either QDAO or BASELINE"
            )

        st = time()
        engine.run()
        print("Qdao runs:\t{}".format(time() - st))
        # print(sv)
        engine.print_statistics()
        engine._manager.print_statistics()

        if is_diff:
            circ.save_state()
            st = time()
            try:
                self._sv_sim.set_options(method="statevector")
                self._sv_sim.set_options(device=device)
                sv_org = self._sv_sim.run(circ).result().get_statevector().data
            except Exception:
                pass
            print("Qiskit runs: {}".format(time() - st))

    def test_run_qiskit_any_qasm(
        self, nq, np, nl, mode, qasm, parallel, diff, sv_location, device
    ):
        NQ, NP, NL = self.get_qdao_params(nq, np, nl)
        parallel = True if int(parallel) == 1 else False
        diff = True if int(diff) == 1 else False

        print("\n::::::::::::::::::Config::::::::::::::::::\n")
        print("NQ::\t{}".format(NQ))
        print("NP::\t{}".format(NP))
        print("NL::\t{}".format(NL))
        print("\n::::::::::::::::::Config::::::::::::::::::\n")

        try:
            circ = qiskit.circuit.QuantumCircuit.from_qasm_file(
                QCS_BENCHMARKS_DIR + qasm
            )
        except Exception as e:
            raise ValueError(f"Cannot load qasm file {qasm}: {e}")
        circ = transpile(circ, self._sv_sim)
        self.run_qiskit_diff_test(
            circ,
            NQ,
            NP,
            NL,
            mode,
            is_parallel=parallel,
            is_diff=diff,
            sv_location=sv_location,
            device=device,
        )

    def test_run_qiskit_random(self, nq):
        NQ = int(nq)
        NP = NQ - 2
        NL = NQ - 10

        circ = self.get_qiskit_circ("random", num_qubits=NQ, depth=9, measure=False)
        circ = transpile(circ, self._sv_sim)

        engine = Engine(circuit=circ, num_primary=NP, num_local=NL, is_parallel=True)
        st = time()
        engine.run()
        print("Qdao runs: {}".format(time() - st))
        sv = retrieve_sv(NQ, num_local=NL)
        engine.print_statistics()
        engine._manager.print_statistics()

        circ.save_state()
        st = time()
        sv_org = self._sv_sim.run(circ).result().get_statevector().data
        print("Qiskit runs: {}".format(time() - st))
        assert Statevector(sv).equiv(Statevector(sv_org))

    def run_quafu_diff_test(
        self,
        circ: QuantumCircuit,
        NQ: int,
        NP: int,
        NL: int,
        mode: str = "QDAO",
        is_parallel: bool = True,
        is_diff: bool = True,
    ):
        """Run test from qiskit QuantumCircuit
        Args:
            circ: Qiskit quantum circuit
            NQ: number of qubits,
            NP: number of qubits in a compute unit
            NL: number of qubits in a storage unit
            mode: "QDAO" or "BASELINE"
            is_parallel: Whether enable parallel load/store
            is_diff: Whether run diff test, if set False, only run QDAO
        """
        from quafu.circuits.quantum_circuit import QuantumCircuit

        quafu_circ = QuantumCircuit(1)
        quafu_circ.from_openqasm(dumps(circ))
        # quafu_circ = qasm_to_circuit(dumps(circ))
        # print("\nOriginal Circ")
        # quafu_circ.draw_circuit()

        if mode == "QDAO":
            engine = Engine(
                circuit=quafu_circ,
                num_primary=NP,
                num_local=NL,
                backend="quafu",
                is_parallel=is_parallel,
            )
        elif mode == "BASELINE":
            engine = Engine(
                circuit=quafu_circ,
                num_primary=NP,
                num_local=NL,
                backend="quafu",
                partitioner=BaselinePartitioner(np=NP, nl=NL, backend="quafu"),
                is_parallel=is_parallel,
            )
        else:
            raise ValueError(
                f"Unsupported mode::{mode}, should be either QDAO or BASELINE"
            )

        st = time()
        engine.run()
        print("Qdao runs:\t{}".format(time() - st))
        # print(sv)
        engine.print_statistics()
        engine._manager.print_statistics()

        if is_diff:
            from quafu.simulators.simulator import simulate

            st = time()
            init_sv = np.zeros(1 << NQ, dtype=np.complex128)
            init_sv[0] = 1
            sv_org = simulate(
                quafu_circ, psi=init_sv, output="state_vector"
            ).get_statevector()
            print("Quafu runs:\t{}".format(time() - st))
            # print(sv_org)

            if NQ < 26:
                sv = retrieve_sv(NQ, num_local=NL)
                assert Statevector(sv).equiv(Statevector(sv_org))

    def get_qdao_params(self, nq, np, nl):
        nq = int(nq)
        np = int(np)
        nl = int(nl)

        NQ = nq if nq > 0 else 12
        NP = np if np > 0 else NQ - 2  # Normally set 2
        NL = nl if nl > 0 else NQ - 10  # Normally set 10

        return NQ, NP, NL

    def test_run_quafu_any_qasm(self, nq, np, nl, mode, qasm, parallel, diff):
        """
        Basic test to run random circuits and
        compare performance between
        1. Qdao on top of quafu
        2. Quafu
        """
        NQ, NP, NL = self.get_qdao_params(nq, np, nl)
        parallel = True if int(parallel) == 1 else False
        diff = True if int(diff) == 1 else False

        print("\n::::::::::::::::::Config::::::::::::::::::\n")
        print("NQ::\t{}".format(NQ))
        print("NP::\t{}".format(NP))
        print("NL::\t{}".format(NL))
        print("\n::::::::::::::::::Config::::::::::::::::::\n")

        try:
            circ = qiskit.circuit.QuantumCircuit.from_qasm_file(
                QCS_BENCHMARKS_DIR + qasm
            )
        except Exception as e:
            raise ValueError(f"Cannot load qasm file {qasm}: {e}")
        circ = transpile(circ, self._sv_sim)

        self.run_quafu_diff_test(
            circ, NQ, NP, NL, mode=mode, is_parallel=parallel, is_diff=diff
        )

    def test_run_quafu_random_single_vs_qiskit_with_init(self, nq):
        NQ = int(nq)

        from qdao.qiskit.utils import random_circuit

        circ = random_circuit(NQ, NQ, measure=False)
        circ = transpile(circ, self._sv_sim)

        from quafu.circuits.quantum_circuit import QuantumCircuit

        quafu_circ = QuantumCircuit(1)
        quafu_circ.from_openqasm(dumps(circ))
        # quafu_circ = qasm_to_circuit(dumps(circ))

        from quafu.simulators.simulator import simulate

        st = time()
        init_sv = np.zeros(1 << NQ, dtype=np.complex128)
        init_sv[0] = 1
        sv_quafu = simulate(
            quafu_circ, psi=init_sv, output="state_vector"
        ).get_statevector()
        print("Quafu runs: {}".format(time() - st))

        st = time()
        init_sv = np.zeros(1 << NQ, dtype=np.complex128)
        init_sv[0] = 1

        init_circ = qiskit.circuit.QuantumCircuit(NQ)
        init_circ.initialize(init_sv, range(NQ))
        init_circ.compose(circ, inplace=True)
        init_circ.save_state()
        self._sv_sim.set_options(fusion_enable=False)
        sv_qiskit = self._sv_sim.run(init_circ).result().get_statevector()

        # FIXME(zhaoyilun): when testing small circuits, uncomment this
        assert sv_qiskit.equiv(Statevector(sv_quafu))
        # print(sv_quafu)
        # print(sv_qiskit.data)

        print("Qiskit runs: {}".format(time() - st))
