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

from solvers import enumerate_models, accumulate_models


def possibilities(cc: ConstraintCircuit, pre_model):
    circuit = cc.circuit & pre_model_to_circuit(pre_model, cc.pool)
    complete = circuit & cc.pool.uniqueness()
    return enumerate_models(complete, cc.pool)


def candidate(cc: ConstraintCircuit, pre_model):
    circuit = cc.circuit & pre_model_to_circuit(pre_model, cc.pool)
    complete = circuit & cc.pool.uniqueness()
    return accumulate_models(complete, cc.pool)


def find_example(cc: ConstraintCircuit, sentence):
    for model in enumerate_models(cc.circuit & sentence, cc.pool):
        return model
    raise ValueError(f"The sentence {sentence} is not satisfiable")
