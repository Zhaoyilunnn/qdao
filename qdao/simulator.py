"""Simulator provider"""

from qdao.qiskit.simulator import QiskitSimulator
from qdao.quafu.simulator import QuafuSimulator


class QdaoSimObj:
    def __init__(self, *objs, **options) -> None:
        self._objs = objs
        self._circ = objs[-1]
        self._run_options = options

    @property
    def circ(self):
        return self._circ

    @property
    def objs(self):
        return self._objs

    @property
    def run_options(self):
        return self._run_options


SIMS = {"qiskit": QiskitSimulator, "quafu": QuafuSimulator}


class SimulatorProvider:
    @classmethod
    def get_simulator(cls, backend_name: str, **kwargs):
        return SIMS[backend_name](**kwargs)
