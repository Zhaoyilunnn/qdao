import copy
import os
from time import time
import numpy as np
from qiskit import QuantumCircuit, qiskit

from qiskit.compiler import transpile
from qiskit.quantum_info import Statevector
from qdao.circuit import BaselinePartitioner
from qdao.simulator import QdaoSimObj

from tests.qdao import QdaoBaseTest
from qdao.engine import Engine
from qdao.util import retrieve_sv

from constants import *
import pytest


class TestEngine(QdaoBaseTest):
    def setup_method(self):
        if not os.path.exists("qcs"):
            os.system(f"git clone {QCS_URL} qcs")

    @pytest.mark.skip(
        reason="turn off automatic detection of this test since it is not necessary"
    )
    def test_pre_postprocessing(self):
        circ = self.get_qiskit_circ("random", num_qubits=8, depth=20, measure=False)
        circ = transpile(circ, self._sv_sim)

        engine = Engine(circuit=circ, num_primary=6, num_local=2)

        sub_circs = engine._part.run(engine._circ)

        sv = engine._sim.run(QdaoSimObj(sub_circs[0].circ))
        engine._postprocess(sub_circs[0], 0, sv)

        obj = engine._preprocess(sub_circs[0], 0)
        print(sub_circs[0].circ)

        assert np.array_equal(sv, obj.objs[0])

    @pytest.mark.skip(
        reason="turn off automatic detection of this test since it is not necessary"
    )
    def test_run_step(self, nq):
        NQ = int(nq)
        NP = NQ
        NL = NQ - 10

        circ = self.get_qiskit_circ("random", num_qubits=NQ, depth=9, measure=False)
        circ = transpile(circ, self._sv_sim)
        circ_sv = copy.deepcopy(circ)
        circ_sv.save_state()
        st = time()
        job = self._sv_sim.run(circ_sv)
        sv0 = job.result().get_statevector()
        print("Qiskit runs: {}".format(time() - st))

        engine = Engine(circuit=circ, num_primary=NP, num_local=NL, is_parallel=True)
        sub_circs = engine._part.run(circ)
        engine._initialize()
        simobj = engine._preprocess(sub_circs[0], 0)
        st = time()
        print("Start running simulation")
        sv1 = engine._sim.run(simobj)
        print("Qiskit runs: {}".format(time() - st))
        print("sub-circs num: {}".format(len(sub_circs)))

        assert sv0.equiv(sv1)

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

    @pytest.mark.skip(
        reason="turn off automatic detection of this test since it is not necessary"
    )
    def test_run_qiskit_random_basic(self, nq, np, nl, mode):
        NQ, NP, NL = self.get_qdao_params(nq, np, nl)

        D = NQ - 3  # depth
        MAX_OP = 2

        print("\n::::::::::::::::::Config::::::::::::::::::\n")
        print("NQ::\t{}".format(NQ))
        print("NP::\t{}".format(NP))
        print("NL::\t{}".format(NL))
        print("D::\t{}".format(D))
        print("\n::::::::::::::::::Config::::::::::::::::::\n")

        from qdao.qiskit.utils import random_circuit

        circ_name = "_".join(
            ["random", str(NQ), str(D), "max_operands", str(MAX_OP), "gen.qasm"]
        )
        if not os.path.exists(QCS_BENCHMARKS_DIR + circ_name):
            circ = random_circuit(NQ, D, max_operands=MAX_OP, measure=False)
            circ = transpile(circ, self._sv_sim)
            with open(QCS_BENCHMARKS_DIR + circ_name, "w") as f:
                f.write(circ.qasm())
        else:
            print(
                "\n:::Reusing existing bench:::::{}::::::::\n".format(
                    QCS_BENCHMARKS_DIR + circ_name
                )
            )
            circ = qiskit.circuit.QuantumCircuit.from_qasm_file(
                QCS_BENCHMARKS_DIR + circ_name
            )

        circ = transpile(circ, self._sv_sim)
        self.run_qiskit_diff_test(circ, NQ, NP, NL, mode)

    @pytest.mark.skip(
        reason="turn off automatic detection of this test since it is not necessary"
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

    @pytest.mark.skip(
        reason="turn off automatic detection of this test since it is not necessary"
    )
    def test_run_quafu_single_random_no_init(self, nq):
        NQ = int(nq)

        circ = self.get_qiskit_circ("random", num_qubits=NQ, depth=9, measure=False)
        circ = transpile(circ, self._sv_sim)
        from quafu.circuits.quantum_circuit import QuantumCircuit

        quafu_circ = QuantumCircuit(1)
        quafu_circ.from_openqasm(circ.qasm())
        # quafu_circ = qasm_to_circuit(circ.qasm())

        from quafu.simulators.simulator import simulate

        st = time()
        sv_wo_init = simulate(quafu_circ, output="state_vector").get_statevector()
        print("Quafu runs: {}".format(time() - st))

        init_sv = np.zeros(1 << NQ, dtype=np.complex128)
        init_sv[0] = 1
        sv_with_init = simulate(
            quafu_circ, psi=init_sv, output="state_vector"
        ).get_statevector()

        print(sv_wo_init)
        print(sv_with_init)
        assert Statevector(sv_wo_init).equiv(Statevector(sv_with_init))

    @pytest.mark.skip(
        reason="turn off automatic detection of this test since it is not necessary"
    )
    def test_run_quafu_random_single(self, nq):
        NQ = int(nq)

        circ = self.get_qiskit_circ("random", num_qubits=NQ, depth=9, measure=False)
        circ = transpile(circ, self._sv_sim)
        from quafu.circuits.quantum_circuit import QuantumCircuit

        quafu_circ = QuantumCircuit(1)
        quafu_circ.from_openqasm(circ.qasm())
        # quafu_circ = qasm_to_circuit(circ.qasm())

        from quafu.simulators.simulator import simulate

        st = time()
        init_sv = np.zeros(1 << NQ, dtype=np.complex128)
        init_sv[0] = 1
        sv_org = simulate(
            quafu_circ, psi=init_sv, output="state_vector"
        ).get_statevector()
        print("Quafu runs: {}".format(time() - st))

    @pytest.mark.skip(
        reason="turn off automatic detection of this test since it is not necessary"
    )
    def test_run_quafu_random_step_by_step(self, nq):
        NQ = int(nq)
        NP = NQ - 2
        NL = NQ - 4
        D = NQ - 3  # depth

        from qdao.qiskit.utils import random_circuit

        circ = random_circuit(NQ, D, max_operands=2, measure=False)
        circ = transpile(circ, self._sv_sim)

        from quafu.circuits.quantum_circuit import QuantumCircuit

        quafu_circ = QuantumCircuit(1)
        quafu_circ.from_openqasm(circ.qasm())
        # quafu_circ = qasm_to_circuit(circ.qasm())
        print("\nOriginal Circ")
        quafu_circ.draw_circuit()

        engine = Engine(
            circuit=quafu_circ,
            num_primary=NP,
            num_local=NL,
            backend="quafu",
            is_parallel=False,
        )

        sub_circs = engine._part.run(engine._circ)
        engine._initialize()

        num_acc_ops = 0
        input_sv = np.zeros(1 << NQ, dtype=np.complex128)
        input_sv[0] = 1
        for sub_circ in sub_circs:
            for ichunk in range(engine._num_chunks):
                simobj = engine._preprocess(sub_circ, ichunk)
                sv = engine._sim.run(simobj)
                engine._postprocess(sub_circ, ichunk, sv)

            sv_expected = retrieve_sv(NQ, num_local=NL)
            print("\n:::::debugging sub-circ::::\n")
            sub_circ.circ.draw_circuit()
            self.debug_run_quafu_circ(
                quafu_circ,
                input_sv,
                sv_expected,
                (num_acc_ops, num_acc_ops + len(sub_circ.circ.gates)),
            )
            num_acc_ops += len(sub_circ.circ.gates)
            input_sv = sv_expected

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
        quafu_circ.from_openqasm(circ.qasm())
        # quafu_circ = qasm_to_circuit(circ.qasm())
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

    @pytest.mark.skip(
        reason="turn off automatic detection of this test since it is not necessary"
    )
    def test_run_quafu_random_basic(self, nq, np, nl, mode, parallel, diff):
        """
        Basic test to run random circuits and
        compare performance between
        1. Qdao on top of quafu
        2. Quafu
        """
        NQ, NP, NL = self.get_qdao_params(nq, np, nl)
        parallel = True if int(parallel) == 1 else False
        diff = True if int(diff) == 1 else False

        D = NQ - 3  # depth
        # D = 2 # depth
        MAX_OP = 2

        print("\n::::::::::::::::::Config::::::::::::::::::\n")
        print("NQ::\t{}".format(NQ))
        print("NP::\t{}".format(NP))
        print("NL::\t{}".format(NL))
        print("D::\t{}".format(D))
        print("\n::::::::::::::::::Config::::::::::::::::::\n")

        from qdao.qiskit.utils import random_circuit

        circ_name = "_".join(
            ["random", str(NQ), str(D), "max_operands", str(MAX_OP), "gen.qasm"]
        )
        if not os.path.exists(QCS_BENCHMARKS_DIR + circ_name):
            circ = random_circuit(NQ, D, max_operands=MAX_OP, measure=False)
            circ = transpile(circ, self._sv_sim)
            with open(QCS_BENCHMARKS_DIR + circ_name, "w") as f:
                f.write(circ.qasm())
        else:
            print(
                "\n:::Reusing existing bench:::::{}::::::::\n".format(
                    QCS_BENCHMARKS_DIR + circ_name
                )
            )
            circ = qiskit.circuit.QuantumCircuit.from_qasm_file(
                QCS_BENCHMARKS_DIR + circ_name
            )

        self.run_quafu_diff_test(
            circ, NQ, NP, NL, mode=mode, is_parallel=parallel, is_diff=diff
        )

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

    @pytest.mark.skip(
        reason="turn off automatic detection of this test since it is not necessary"
    )
    def test_run_quafu_qasm_basic(self, bench, nq):
        """
        Basic test to run random circuits and
        compare performance between
        1. Qdao on top of quafu
        2. Quafu
        """
        NQ = int(nq)
        NP = NQ - 2
        NL = NQ - 10
        print("\n::::::::::::::::::Config::::::::::::::::::\n")
        print("NQ::\t{}".format(NQ))
        print("NP::\t{}".format(NP))
        print("NL::\t{}".format(NL))
        print("bench::\t".format(bench))
        print("\n::::::::::::::::::Config::::::::::::::::::\n")

        qasm_path = QCS_BENCHMARKS_DIR + bench + "-" + str(NQ) + ".qasm"
        if not os.path.exists(qasm_path):
            raise FileNotFoundError("qasm does not exists: ".format(qasm_path))

        circ = qiskit.circuit.QuantumCircuit.from_qasm_file(qasm_path)
        self.run_quafu_diff_test(circ, NQ, NP, NL)

    @pytest.mark.skip(
        reason="turn off automatic detection of this test since it is not necessary"
    )
    def test_run_quafu_random_single_vs_qiskit_with_init(self, nq):
        NQ = int(nq)

        from qdao.qiskit.utils import random_circuit

        circ = random_circuit(NQ, NQ, measure=False)
        circ = transpile(circ, self._sv_sim)

        from quafu.circuits.quantum_circuit import QuantumCircuit

        quafu_circ = QuantumCircuit(1)
        quafu_circ.from_openqasm(circ.qasm())
        # quafu_circ = qasm_to_circuit(circ.qasm())

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
        # assert sv_qiskit.equiv(Statevector(sv_quafu))
        # print(sv_quafu)
        # print(sv_qiskit.data)

        print("Qiskit runs: {}".format(time() - st))

    @pytest.mark.skip(
        reason="turn off automatic detection of this test since it is not necessary"
    )
    def test_run_quafu_bench(self, bench):
        qasm_path = QASMBENCH_LARGE_DIR + "/" + bench + "/" + bench + ".qasm"
        quafu_circ = self.get_quafu_circ_from_qasm(qasm_path)
        NQ = quafu_circ.num
        NP = NQ - 2
        NL = NQ - 10

        engine = Engine(
            circuit=quafu_circ,
            num_primary=NP,
            num_local=NL,
            backend="quafu",
            is_parallel=True,
        )
        engine.run()
        sv = retrieve_sv(NQ, num_local=NL)

        init_sv = np.zeros(1 << NQ, dtype=np.complex128)
        init_sv[0] = 1
        from quafu.simulators.simulator import simulate

        sv_org = simulate(
            quafu_circ, psi=init_sv, output="state_vector"
        ).get_statevector()

        assert Statevector(sv).equiv(Statevector(sv_org))

        qiskit_circ = self.get_qiskit_circ("qasm", qasm_path=qasm_path)
        qiskit_circ.remove_final_measurements()
        qiskit_circ.save_state()
        sv_qiskit = self._sv_sim.run(qiskit_circ).result().get_statevector().data

        assert Statevector(sv_qiskit).equiv(Statevector(sv_org))
