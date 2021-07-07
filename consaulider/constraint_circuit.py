from typing import List, TypeVar, Generic, Optional, Dict

import pickle

from dataclasses import dataclass

import itertools

from functools import reduce

from pysat.formula import IDPool
from pysat.solvers import Solver, Minisat22

import aiger


from constraint import Constraint
from id_pool import IDs
from aiger_utils import all_, any_

T = TypeVar("T")


@dataclass
class ConstraintCircuit(Generic[T]):
    circuit: aiger.AIG = None
    pool: IDs[T] = IDs()

    def dump(self, filepath):
        with open(filepath, "wb") as f:
            pickle.dump(
                {"circuit": self.circuit.aig, "pool": dict(self.pool.obj2id)}, f
            )

    def parse(self, filepath):
        with open(filepath, "rb") as f:
            d = pickle.load(f)
            self.circuit = aiger.BoolExpr(d["circuit"])
            self.pool.load(d["pool"])
