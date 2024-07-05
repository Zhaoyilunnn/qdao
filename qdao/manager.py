import concurrent.futures
import logging
import multiprocessing as mp
import os
from threading import Thread
from typing import List
from mpi4py import MPI
import logging
import numpy as np

from qdao.executor import (
    AsyncIoExecutor,
    BatchParallelExecutor,
    ConstantPoolParallelExecutor,
    ParallelExecutor,
    PoolParallelExecutor,
)
from qdao.circuit import (
    BasePartitioner,
    CircuitHelperProvider,
    QdaoCircuit,
    StaticPartitioner,
)
from qdao.util import *

print_statistics = safe_import("qutils", "print_statistics")
time_it = safe_import("qutils", "time_it")


class SvManager:
    """Statevector data access manager"""

    def __init__(
        self,
        num_qubits: int = 6,
        num_primary: int = 4,
        num_local: int = 2,
        is_parallel: bool = False,
        sv_location="disk",
    ) -> None:
        """
        Args:
            num_qubits (int): Number of qubits in the target circuit
            num_primary (int): Number of qubits that reside in primary storage (i.e., host memory)
            num_local (int): Number of qubits that reside in secondary storage (i.e., disk).
                Note that this defines the size of minimum storage unit.
        """
        self._nq, self._np, self._nl = num_qubits, num_primary, num_local
        print("qubit")
        self._chunk_idx = 0
        self._chunk = np.zeros(1 << num_primary, dtype=np.complex128)
        self._is_parallel = is_parallel
        self._executor = BatchParallelExecutor()
        comm = MPI.COMM_WORLD
        self._rank = comm.Get_rank()
        self.previous_subcircuit_qset: list = []
        # Save statevector in memory
        self._global_sv = []

        # Storage Location Setting
        # you can choose memory or disk
        # self._sv_location = 'memory'
        self._sv_location = sv_location

        if not os.path.isdir("data"):
            os.mkdir("data")

    @property
    def num_qubits(self):
        return self._np

    @property
    def num_primary(self):
        return self._np

    @property
    def num_local(self):
        return self._nl

    @property
    def chunk_idx(self):
        return self._chunk_idx

    @chunk_idx.setter
    def chunk_idx(self, idx):
        self._chunk_idx = idx

    @property
    def chunk(self):
        return self._chunk

    @chunk.setter
    def chunk(self, data: np.ndarray):
        self._chunk = data

    def _get_global_qubits(self, org_qubits: List[int]):
        glob_q = []
        for org_q in org_qubits:
            if org_q >= self._nl:
                glob_q.append(org_q - self._nl)
        return glob_q

    def _num_primary_groups(self, num_lg: int):
        return 1 << (self._np - self._nl - num_lg)

    def _get_start_group_id(self, num_primary_groups: int, chunk_idx: int):
        return chunk_idx * num_primary_groups

    def _init_single_su(self, i):
        # Init a storage unit
        su = np.zeros(1 << self._nl, dtype=np.complex128)
        if i == 0:
            su[0] = 1.0

        if self._sv_location == "disk":
            fn = generate_secondary_file_name(i)
            np.save(fn, su)
        else:
            self._global_sv.append(su)

    @time_it
    def initialize(self):
        # Calc number of storage units
        num_sus = 1 << (self._nq - self._nl)
        init_single_su_params = [[i] for i in range(num_sus)]
        if self._is_parallel:
            self._executor.execute(self._init_single_su, init_single_su_params)
        else:
            for i in range(num_sus):
                self._init_single_su(i)

    def _load_single_su(self, isub: int, fn: str):
        # Populate to current chunk

        if self._sv_location == "disk":
            vec = np.load(fn)
        else:
            vec = self._global_sv[isub]

        chk_start = isub << self._nl
        chk_end = (isub << self._nl) + (1 << self._nl)
        self._chunk[chk_start:chk_end] = vec

    @time_it
    def load_sv(self, org_qubits: List[int]):
        """Load a `chunk` of statevector into memory
        Reference: sim-beta/statevector/src/statevector.cpp
        TODO: detailed description
        """
        # if len(org_qubits) <= self._nl:
        if len(org_qubits) < self._nl:
            raise ValueError(
                "Number of qubits in a sub-circuit "
                "should be larger than local qubits"
            )

        global_qubits = self._get_global_qubits(org_qubits)
        LGDIM = len(global_qubits)  # Logical global qubits' size
        isub = 0
        num_prim_grps = self._num_primary_groups(LGDIM)

        start_group_id = self._get_start_group_id(num_prim_grps, self._chunk_idx)
        end_group_id = start_group_id + num_prim_grps

        load_single_su_params = []
        for gid in range(start_group_id, end_group_id):
            inds = indexes(global_qubits, gid)
            for idx in range(1 << LGDIM):
                isub = (1 << LGDIM) * (gid - start_group_id) + idx

                assert (isub << self._nl) + (1 << self._nl) <= (1 << self._np)

                fn = generate_secondary_file_name(inds[idx])
                load_single_su_params.append((isub, fn))
        if self._is_parallel:
            self._executor.execute(self._load_single_su, load_single_su_params)
        else:
            for isub, fn in load_single_su_params:
                self._load_single_su(isub, fn)

        return self._chunk

    def _store_single_su(self, isub: int, fn: str):
        # Save corresponding slice to secondary storage
        chk_start = isub << self._nl
        chk_end = (isub << self._nl) + (1 << self._nl)

        if self._sv_location == "disk":
            np.save(fn, self._chunk[chk_start:chk_end])
        else:
            self._global_sv[isub] = self._chunk[chk_start:chk_end]
            # np.save(fn, self._chunk[chk_start:chk_end])
            # print(self._chunk[chk_start:chk_end])

    @time_it
    def store_sv(self, org_qubits: List[int]):
        # if len(org_qubits) <= self._nl:
        if len(org_qubits) < self._nl:
            raise ValueError(
                "Number of qubits in a sub-circuit should be larger than local qubits"
            )
        global_qubits = self._get_global_qubits(org_qubits)
        LGDIM = len(global_qubits)  # Logical global qubits' size
        isub = 0
        num_prim_grps = self._num_primary_groups(LGDIM)
        start_group_id = self._get_start_group_id(num_prim_grps, self._chunk_idx)
        end_group_id = start_group_id + num_prim_grps
        store_single_su_params = []
        for gid in range(start_group_id, end_group_id):
            inds = indexes(global_qubits, gid)
            for idx in range(1 << LGDIM):
                isub = (1 << LGDIM) * (gid - start_group_id) + idx
                assert (isub << self._nl) + (1 << self._nl) <= (1 << self._np)
                fn = generate_secondary_file_name(inds[idx])
                store_single_su_params.append((isub, fn))
                # self._store_single_su(isub, fn)

        # with mp.Pool(mp.cpu_count()) as pool:
        #    pool.starmap(self._store_single_su, store_single_su_params)
        #    pool.close()
        #    pool.join()
        if self._is_parallel:
            # executor = ParallelExecutor(self._store_single_su, store_single_su_params)
            # executor.execute()
            self._executor.execute(self._store_single_su, store_single_su_params)
        else:
            for isub, fn in store_single_su_params:
                self._store_single_su(isub, fn)

    @time_it
    def is_initial_state(self):
        return len(self.previous_subcircuit_qset) == 0

    # todo error
    @time_it
    def distributed_send_status_vector(self, sub_circ: QdaoCircuit):
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()
        
        all_src = get_dest(
            self._nq, sub_circ.real_qubits, self.previous_subcircuit_qset, rank
        )
        all_dest = get_dest(
            self._nq, self.previous_subcircuit_qset, sub_circ.real_qubits, rank
        )
        logging.debug("The qubit acted on by the previous subcircuit")
        logging.debug(self.previous_subcircuit_qset)
        logging.debug("The qubit that the current subcircuit acts on")
        logging.debug(sub_circ.real_qubits)
        pack_size = 1 << get_pack_size(
            sub_circ.real_qubits, self.previous_subcircuit_qset
        )
        all_tag = get_tag(all_dest)
        buffer = []
        for i in range(len(all_dest)):
            if all_dest[i] != rank:
                logging.debug(
                    "Process {} sends its own status [{},{}] to process {}".format(
                        rank, i * pack_size, (i + 1) * pack_size, all_dest[i]
                    )
                )
                logging.debug(
                    "The size of a single packet is {} bytes".format(
                        self._chunk[i * pack_size : (i + 1) * pack_size].nbytes
                    )
                )
                comm.Isend(
                    self._chunk[i * pack_size : (i + 1) * pack_size],
                    dest=all_dest[i],
                    tag=all_tag[i],
                )
            else:
                logging.debug(
                    "Process {} sends its own status [{},{}] to process {}".format(
                        rank, i * pack_size, (i + 1) * pack_size, all_dest[i]
                    )
                )
                logging.debug(
                    "Process {} receives its own status [{},{}] from process {}".format(
                        rank, i * pack_size, (i + 1) * pack_size, all_src[i]
                    )
                )
                buffer.append(self._chunk[i * pack_size : (i + 1) * pack_size])
        for i in range(len(all_src)):
            if all_src[i] == rank:
                self._chunk[i * pack_size : (i + 1) * pack_size] = buffer.pop(0)

    @time_it
    def distributed_receive_status_vector(self, sub_circ: QdaoCircuit):
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()
        all_src = get_dest(
            self.num_qubits, sub_circ.real_qubits, self.previous_subcircuit_qset, rank
        )
        all_req = []
        pack_size = 1 << get_pack_size(
            sub_circ.real_qubits, self.previous_subcircuit_qset
        )

        all_tag = get_tag(all_src)
        for i in range(len(all_src)):
            if all_src[i] != rank:
                logging.debug(
                    "Process {} receives its own status [{},{}] from process {}".format(
                        rank, i * pack_size, (i + 1) * pack_size, all_src[i]
                    )
                )
                logging.debug(
                    "The size of a single packet is {} bytes".format(
                        self._chunk[i * pack_size : (i + 1) * pack_size].nbytes
                    )
                )
                all_req.append(
                    comm.Irecv(
                        self._chunk[i * pack_size : (i + 1) * pack_size],
                        source=all_src[i],
                        tag=all_tag[i],
                    )
                )
        for req in all_req:
            req.Wait()
        logging.debug("All data of process {} is ready".format(rank))
        self.previous_subcircuit_qset = sub_circ.real_qubits
        # breakpoint()


SvManager.print_statistics = print_statistics
