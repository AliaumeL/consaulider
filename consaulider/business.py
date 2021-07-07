from typing import List, TypeVar, Generic, Optional, Dict

import pickle

from dataclasses import dataclass

import itertools

from functools import reduce

from pysat.formula import IDPool
from pysat.solvers import Solver, Minisat22

import aiger


import pandas as pd


from constraint import Constraint
from id_pool import IDs
from aiger_utils import all_, any_

T = TypeVar("T")


def df_to_circuit(df: pd.DataFrame, id_pool: IDs):
    columns = list(df.columns)

    rows = [
        all_([id_pool.atom(col, row[col]) for col in columns])
        for _, row in df.iterrows()
    ]

    otherwise = all_(
        ~id_pool.atom(col, row[col]) for _, row in df.iterrows() for col in columns
    )

    circuit = (any_(rows) | otherwise) & id_pool.uniqueness()
    return circuit


def pre_model_to_circuit(pre_model: Dict, id_pool: IDs):

    assumptions = all_(
        any_(id_pool.atom(k, v) for v in values)
        for k, values in pre_model.items()
        if isinstance(values, list) and len(values) > 0
    )

    return assumptions & id_pool.uniqueness()
