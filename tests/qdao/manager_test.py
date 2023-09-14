import random

from time import time
import numpy as np

from qiskit.compiler import transpile

from qdao.manager import SvManager
from qdao.util import DATA_DIR
from tests.qdao import QdaoBaseTest


class TestSvManager(QdaoBaseTest):
    _sv_dao = SvManager()

    def test_load_sv_continuous(self):
        vec0 = np.random.rand(4) + 1j * np.random.rand(4)
        vec1 = np.random.rand(4) + 1j * np.random.rand(4)
        vec2 = np.random.rand(4) + 1j * np.random.rand(4)
        vec3 = np.random.rand(4) + 1j * np.random.rand(4)
        print(vec0)
        print(vec1)
        print(vec2)
        print(vec3)
        np.save(DATA_DIR + "/sv0.npy", vec0)
        np.save(DATA_DIR + "/sv1.npy", vec1)
        np.save(DATA_DIR + "/sv2.npy", vec2)
        np.save(DATA_DIR + "/sv3.npy", vec3)

        self._sv_dao.load_sv([0, 1, 2])
        print(self._sv_dao._chunk)
        np.testing.assert_array_equal(self._sv_dao._chunk[0:4], vec0)
        np.testing.assert_array_equal(self._sv_dao._chunk[4:8], vec1)
        np.testing.assert_array_equal(self._sv_dao._chunk[8:12], vec2)
        np.testing.assert_array_equal(self._sv_dao._chunk[12:16], vec3)

    def test_load_sv_interleave(self):
        vec0 = np.random.rand(4) + 1j * np.random.rand(4)
        vec1 = np.random.rand(4) + 1j * np.random.rand(4)
        vec2 = np.random.rand(4) + 1j * np.random.rand(4)
        vec3 = np.random.rand(4) + 1j * np.random.rand(4)
        print(vec0)
        print(vec1)
        print(vec2)
        print(vec3)
        np.save(DATA_DIR + "/sv0.npy", vec0)
        np.save(DATA_DIR + "/sv1.npy", vec1)
        np.save(DATA_DIR + "/sv2.npy", vec2)
        np.save(DATA_DIR + "/sv3.npy", vec3)

        self._sv_dao.load_sv([0, 1, 3])
        print(self._sv_dao._chunk)
        np.testing.assert_array_equal(self._sv_dao._chunk[0:4], vec0)
        np.testing.assert_array_equal(self._sv_dao._chunk[4:8], vec2)
        np.testing.assert_array_equal(self._sv_dao._chunk[8:12], vec1)
        np.testing.assert_array_equal(self._sv_dao._chunk[12:16], vec3)

    def test_save_sv_continuous(self):
        vec = np.random.rand(16) + 1j * np.random.rand(16)
        self._sv_dao._chunk = vec
        self._sv_dao.store_sv([0, 1, 2])
        vec0 = np.load(DATA_DIR + "/sv0.npy")
        vec1 = np.load(DATA_DIR + "/sv1.npy")
        vec2 = np.load(DATA_DIR + "/sv2.npy")
        vec3 = np.load(DATA_DIR + "/sv3.npy")
        np.testing.assert_array_equal(self._sv_dao._chunk[0:4], vec0)
        np.testing.assert_array_equal(self._sv_dao._chunk[4:8], vec1)
        np.testing.assert_array_equal(self._sv_dao._chunk[8:12], vec2)
        np.testing.assert_array_equal(self._sv_dao._chunk[12:16], vec3)

    def test_save_sv_interleave(self):
        vec = np.random.rand(16) + 1j * np.random.rand(16)
        self._sv_dao._chunk = vec
        self._sv_dao.store_sv([0, 1, 3])
        vec0 = np.load(DATA_DIR + "/sv0.npy")
        vec1 = np.load(DATA_DIR + "/sv1.npy")
        vec2 = np.load(DATA_DIR + "/sv2.npy")
        vec3 = np.load(DATA_DIR + "/sv3.npy")
        np.testing.assert_array_equal(self._sv_dao._chunk[0:4], vec0)
        np.testing.assert_array_equal(self._sv_dao._chunk[8:12], vec1)
        np.testing.assert_array_equal(self._sv_dao._chunk[4:8], vec2)
        np.testing.assert_array_equal(self._sv_dao._chunk[12:16], vec3)

    def test_load_save_large(self, nq):
        NQ = int(nq)
        NP = NQ - 2
        qubits = list(range(NQ - 10)) + sorted(
            random.sample(range(NQ - 10, NQ), NP - NQ + 10)
        )
        print("qubits::\t{}".format(qubits))
        vec = np.random.rand(1 << NP) + 1j * np.random.rand(1 << NP)

        sv_dao = SvManager(
            num_qubits=NQ, num_primary=NP, num_local=NQ - 10, is_parallel=False
        )
        sv_dao.chunk = vec

        print("store_sv::start::NQ::\t{}".format(NQ))
        st = time()
        sv_dao.store_sv(qubits)
        print("store_sv::time::\t{}".format(time() - st))

        print("load_sv::start::NQ::\t{}".format(NQ))
        st = time()
        sv_dao.load_sv(qubits)
        print("load_sv::time::\t{}".format(time() - st))

        sv_dao = SvManager(
            num_qubits=NQ, num_primary=NP, num_local=NQ - 10, is_parallel=True
        )
        sv_dao.chunk = vec

        print("store_sv::start::NQ::\t{}".format(NQ))
        st = time()
        sv_dao.store_sv(qubits)
        print("store_sv::time::\t{}".format(time() - st))

        print("load_sv::start::NQ::\t{}".format(NQ))
        st = time()
        sv_dao.load_sv(qubits)
        print("load_sv::time::\t{}".format(time() - st))
