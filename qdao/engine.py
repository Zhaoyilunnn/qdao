import logging
from time import time
from typing import Any, Optional
from mpi4py import MPI
import numpy as np

from qdao.circuit import (
    BasePartitioner,
    CircuitHelperProvider,
    QdaoCircuit,
    StaticPartitioner,
)
from qiskit import QuantumCircuit
from qdao.manager import SvManager
from qdao.simulator import SimulatorProvider
from qdao.util import generate_secondary_file_name, safe_import

time_it = safe_import("qutils", "time_it")
print_statistics = safe_import("qutils", "print_statistics")


class Engine:
    """Engine to execute a quantum circuit"""

    def __init__(
        self,
        partitioner: Optional[BasePartitioner] = None,
        manager: Optional[SvManager] = None,
        circuit: Any = None,
        num_primary: int = 4,
        num_local: int = 2,
        is_parallel: bool = False,
        backend="qiskit",
        sv_location="disk",
        **backend_args
    ) -> None:
        if isinstance(partitioner, BasePartitioner):
            self._part = partitioner
        else:
            self._part = StaticPartitioner(
                np=num_primary, nl=num_local, backend=backend
            )

        # Get circuit simulator
        self._sim = SimulatorProvider.get_simulator(backend, **backend_args)

        # Get circuit init helper based on backend name
        # This is used to init a circuit from statevector
        self._circ_helper = CircuitHelperProvider.get_helper(backend)

        self._circ = circuit
        self._circ_helper.circ = circuit
        self._nq = self._circ_helper.num_qubits

        if isinstance(manager, SvManager):
            self._manager = manager
        else:
            self._manager = SvManager(
                num_qubits=self._nq,
                num_primary=num_primary,
                num_local=num_local,
                is_parallel=is_parallel,
                sv_location=sv_location,
            )

        self._np, self._nl = num_primary, num_local
        self._num_chunks = 1 << (self._nq - self._np)

        # FIXME: Put initialize to run
        # self._initialize()

    @property
    def num_chunks(self):
        return self._num_chunks

    @time_it
    def _preprocess(self, sub_circ: QdaoCircuit, ichunk: int):
        """Preprocessing before running a sub-simulation
        Args:
            sub_circ (VirtualCircuit):
            ichunk (int): For each sub-circuit, we need to
                simulate chunk by chunk, (num_chunks = 1<<(nq-np))
        """
        self._manager.chunk_idx = ichunk
        sv = self._manager.load_sv(sub_circ.real_qubits)
        logging.debug("loaded sv: {}".format(sv))
        # todo
        self._circ_helper.circ = sub_circ.circ
        return self._circ_helper.init_circ_from_sv(sv)

    @time_it
    def _postprocess(self, sub_circ: QdaoCircuit, ichunk: int, sv: np.ndarray) -> None:
        """Postprocessing after running a sub-simulation
        Args:
            sub_circ (VirtualCircuit):
            ichunk (int): For each sub-circuit, we need to
                simulate chunk by chunk, (num_chunks = 1<<(nq-np))
            sv (np.ndarray): Statevector result of simulation
        """
        self._manager.chunk_idx = ichunk
        self._manager.chunk = sv
        self._manager.store_sv(sub_circ.real_qubits)

    @time_it
    def _run(self, sub_circ: QdaoCircuit) -> None:
        """Run single sub-circuit
        Args:
            sub_circ (VirtualCircuit): Sub circuit with
                metadata recording the mapping between
                virtual and real qubits
        """
        for ichunk in range(self._num_chunks):
            simobj = self._preprocess(sub_circ, ichunk)
            st = time()
            sv = self._sim.run(simobj)
            assert sv.shape[0] == (1 << self._np)
            logging.info("Partial simulation consumes time: {}".format(time() - st))
            self._postprocess(sub_circ, ichunk, sv)

    @time_it
    def _initialize(self):
        """
        Init storage units to "|000...0>"
        """
        self._manager.initialize()

    def run(self):
        """Run simulation
        1. Partition the circuit into sub-circuits
        2. For each sub-circuit, run for 1<<(nq-np) times of
           simulations. Each simulation will init from a
           different part of statevector
        """
        # sub_circs = self._part.run(self._circ)
        # logging.info("Number of sub-circuits: {}".format(len(sub_circs)))
        # self._initialize()
        # for sub_circ in sub_circs:
        #     self._run(sub_circ)
        #     # self.debug(sub_circ)
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()
        sub_circs = self._part.run(self._circ)
        logging.info("Number of sub-circuits: {}".format(len(sub_circs)))
        print("Number of sub-circuits: {}".format(len(sub_circs)))
        for index, sub_circ in enumerate(sub_circs):
            print("Start executing the {}-th subcirc".format(index))
            logging.debug(
                "Rank {} start executing the {}-th subcirc".format(rank, index)
            )
            # breakpoint()
            sv = self._distributed_prepare_state(sub_circ)
            self._distributed_run(sv)
        self._gather_state_vectors()

    @time_it
    def _distributed_prepare_state(self, subcirc: QdaoCircuit) -> None:
        # todo
        # 将当前节点的状态向量从上一个子线路的状态转化成当前
        # 子线路的状态，如果上一个状态是初始状态，则不需要太
        # 多操作，如果上一个状态是子线路则通过通信将其初始化
        self._circ_helper.circ = subcirc.circ
        if self._manager.is_initial_state():
            self._manager.previous_subcircuit_qset = subcirc.real_qubits
        if not self._manager.is_initial_state():
            self._manager.distributed_send_status_vector(subcirc)
            self._manager.distributed_receive_status_vector(subcirc)
        return self._circ_helper.init_circ_from_sv(self._manager._chunk)

    @time_it
    def _distributed_run(self, sub_circ: QdaoCircuit) -> None:
        """Distributed execution of quantum circuits
        Args:
            sub_circ (VirtualCircuit): Multiple subcircuit with
                metadata recording the mapping between
                virtual and real qubits
        """
        sv = self._sim.run(sub_circ)
        self._manager._chunk = sv
        # TODO
        # 将当前节点初始化的状态向量进行子线路中的运算

    @time_it
    def _gather_state_vectors(self) -> None:
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()
        print("rank" + str(rank))

        print("rank" + str(rank))
        print(self._manager._chunk)


Engine.print_statistics = print_statistics
