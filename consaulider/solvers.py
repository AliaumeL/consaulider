from typing import List, TypeVar, Generic, Optional, Dict

import pickle

from dataclasses import dataclass

import itertools

from functools import reduce

from pysat.formula import IDPool
from pysat.solvers import Solver, Minisat22

import aiger
from aiger_cnf import aig2cnf


import pandas as pd


from constraint import Constraint
from id_pool import IDs
from aiger_utils import all_, any_

from business import df_to_circuit, pre_model_to_circuit

from constraint_circuit import ConstraintCircuit


T = TypeVar("T")


def enumerate_models(circuit, id_pool):

    cnf = aig2cnf(circuit)

    def _translate(cube):
        idx2sym = cnf.input2lit
        # ! Careful, Minisat22 uses 1 as the first index !!!
        return [id_pool.obj(int(k)) for k, v in idx2sym.items() if m[v - 1] > 0]

    with Minisat22(bootstrap_with=cnf.clauses) as s:
        for m in s.enum_models():
            yield _translate(m)


def accumulate_models(circuit, id_pool):
    solution = {}
    for model in enumerate_models(circuit, id_pool):
        for constraint in model:
            values = solution.setdefault(constraint.column, set())
            values.add(constraint.value)
    return solution
