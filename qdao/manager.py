"""
Statevector Manager Module
==========================

This module provides an `SvManager` class to manage the statevector data access
and storage for quantum circuit simulations. The statevectors can be stored in 
memory or on disk, and the class supports both serial and parallel execution 
for initializing, loading, and storing statevector chunks.

Modules:
--------

- concurrent.futures: Provides a high-level interface for asynchronously executing callables.
- logging: Provides a flexible framework for emitting log messages from Python programs.
- multiprocessing: Supports spawning processes using an API similar to the threading module.
- os: Provides a portable way of using operating system dependent functionality.
- threading: Constructs higher-level threading interfaces.
- typing: Provides runtime support for type hints.
- numpy: Provides support for large, multi-dimensional arrays and matrices.
- qdao.executor: Contains executor classes for parallel execution.
- qdao.util: Provides utility functions for safe import and file name generation.

Classes:
--------

- SvManager: Manages statevector storage and retrieval.

Attributes:
-----------

- print_statistics: A function to print execution statistics.
- time_it: A decorator to measure the execution time of methods.
"""
import concurrent.futures
import logging
import multiprocessing as mp
import os
from threading import Thread
from typing import List

import numpy as np

from qdao.executor import (
    AsyncIoExecutor,
    BatchParallelExecutor,
    ConstantPoolParallelExecutor,
    ParallelExecutor,
    PoolParallelExecutor,
)
from qdao.util import *

print_statistics = safe_import("qutils", "print_statistics")
time_it = safe_import("qutils", "time_it")


class SvManager:
    """
    Statevector data access manager.

    This class handles the initialization, loading, and storing of statevector chunks
    for quantum circuit simulations. Statevectors can be stored in memory or on disk,
    and the operations can be performed either serially or in parallel.

    Attributes:
        _nq (int): Number of qubits in the target circuit.
        _np (int): Number of qubits in primary storage (host memory).
        _nl (int): Number of qubits in secondary storage (disk).
        _chunk_idx (int): Index of the current chunk.
        _chunk (np.ndarray): Current chunk of the statevector.
        _is_parallel (bool): Indicates if operations should be parallelized.
        _executor (BatchParallelExecutor): Executor for parallel operations.
        _global_sv (List[np.ndarray]): List of statevector chunks in memory.
        _sv_location (str): Location of statevector storage ('memory' or 'disk').
    """

    def __init__(
        self,
        num_qubits: int = 6,
        num_primary: int = 4,
        num_local: int = 2,
        is_parallel: bool = False,
        sv_location="disk",
    ) -> None:
        """
        Initializes the SvManager with the specified parameters.

        Args:
            num_qubits (int): Number of qubits in the target circuit.
            num_primary (int): Number of qubits in primary storage.
            num_local (int): Number of qubits in secondary storage.
            is_parallel (bool): Indicates if operations should be parallelized.
            sv_location (str): Location of statevector storage ('memory' or 'disk').
        """
        self._nq, self._np, self._nl = num_qubits, num_primary, num_local
        self._chunk_idx = 0
        self._chunk = np.zeros(1 << num_primary, dtype=np.complex128)
        self._is_parallel = is_parallel
        self._executor = BatchParallelExecutor()

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
