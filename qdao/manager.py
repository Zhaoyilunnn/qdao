import concurrent.futures
import logging
import multiprocessing as mp
import os
from threading import Thread
from typing import List

import numpy as np
from qutils.misc import print_statistics, time_it

from qdao.executor import (
    AsyncIoExecutor,
    BatchParallelExecutor,
    ConstantPoolParallelExecutor,
    ParallelExecutor,
    PoolParallelExecutor,
)
from qdao.util import *


class SvManager:
    """Statevector data access manager"""

    def __init__(
        self,
        num_qubits: int = 6,
        num_primary: int = 4,
        num_local: int = 2,
        is_parallel: bool = False,
    ) -> None:
        """
        Args:
            num_qubits (int): Number of qubits in the target circuit
            num_primary (int): Number of qubits that reside in primary storage (i.e., host memory)
            num_local (int): Number of qubits that reside in secondary storage (i.e., disk).
                Note that this defines the size of minimum storage unit.
        """
        self._nq, self._np, self._nl = num_qubits, num_primary, num_local
        self._chunk_idx = 0
        self._chunk = np.zeros(1 << num_primary, dtype=np.complex128)
        self._is_parallel = is_parallel
        self._executor = BatchParallelExecutor()

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
        fn = generate_secondary_file_name(i)
        np.save(fn, su)

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
        vec = np.load(fn)
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
                # self._load_single_su(isub, fn)

        # with mp.Pool(mp.cpu_count()) as pool:
        #    pool.starmap(self._load_single_su, load_single_su_params)
        #    pool.close()
        #    pool.join()
        if self._is_parallel:
            # executor = ParallelExecutor(self._load_single_su, load_single_su_params)
            # executor.execute()
            self._executor.execute(self._load_single_su, load_single_su_params)
        else:
            for isub, fn in load_single_su_params:
                self._load_single_su(isub, fn)

        return self._chunk

    def _store_single_su(self, isub: int, fn: str):
        # Save corresponding slice to secondary storage
        chk_start = isub << self._nl
        chk_end = (isub << self._nl) + (1 << self._nl)
        np.save(fn, self._chunk[chk_start:chk_end])

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

    # @time_it
    # def store_sv(self, org_qubits: List[int]):
    #    if len(org_qubits) <= self._nl:
    #        raise ValueError("Number of qubits in a sub-circuit should be larger than local qubits")

    #    global_qubits = self._get_global_qubits(org_qubits)
    #    LGDIM = len(global_qubits) # Logical global qubits' size
    #    isub = 0
    #    num_prim_grps = self._num_primary_groups(LGDIM)

    #    start_group_id = self._get_start_group_id(num_prim_grps, self._chunk_idx)
    #    end_group_id = start_group_id + num_prim_grps

    #    def save_to_file(gid, inds, idx):
    #        isub = (1<<LGDIM) * (gid-start_group_id) + idx
    #        fn = generate_secondary_file_name(inds[idx])
    #        # Save corresponding slice to secondary storage
    #        chk_start = isub<<self._nl
    #        chk_end = (isub<<self._nl) + (1<<self._nl)
    #        np.save(fn, self._chunk[chk_start: chk_end])

    #        logging.debug("Saving sub chunk: {}, "\
    #                "for group: {}, "\
    #                "inds: {}, "\
    #                "fn: {}, \n"\
    #                "chk_start: {}, "\
    #                "chk_end: {}, "\
    #                "chunk: {}, "\
    #                "chunk_size: {}"\
    #                .format(
    #                    isub,
    #                    gid,
    #                    inds,
    #                    fn,
    #                    chk_start,
    #                    chk_end,
    #                    self._chunk,
    #                    self._chunk.shape[0]
    #                ))

    #    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    #        futures = []
    #        for gid in range(start_group_id, end_group_id):
    #            inds = indexes(global_qubits, gid)
    #            logging.debug("Indexing for group: {}, "\
    #                    "indexes: {}, "\
    #                    "org_qubits: {}, "\
    #                    "global_qubits: {}"\
    #                    .format(
    #                        gid,
    #                        inds,
    #                        org_qubits,
    #                        global_qubits
    #                    ))
    #            for idx in range(1<<LGDIM):
    #                futures.append(executor.submit(save_to_file, gid, inds, idx))

    #        # wait for all threads to complete
    #        for future in concurrent.futures.as_completed(futures):
    #            pass


SvManager.print_statistics = print_statistics
