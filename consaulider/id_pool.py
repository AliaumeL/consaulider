from typing import List, TypeVar, Generic, Optional, Dict

import itertools

from pysat.formula import IDPool

import aiger

from aiger_utils import all_, any_
from constraint import Constraint

T = TypeVar("T")


class IDs(IDPool, Generic[T]):
    """
    An id pool to link constraints
    of the form " column_name == value "
    to unique identifiers in the circuit representation
    """

    def __init__(self):
        IDPool.__init__(self, start_from=1)
        self.constraints = {}

    def id(self, constraint: Constraint[T]) -> int:
        values = self.constraints.setdefault(constraint.column, set())
        values.add(constraint.value)
        return IDPool.id(self, constraint)

    def load(self, d: Dict[Constraint[T], int]):
        self.restart(start_from=max(d.values()))

        for k, v in d.items():
            self.id2obj[v] = k
            self.obj2id[k] = v

    def atom(self, column: str, value: T) -> int:
        return aiger.atom(str(self.id(Constraint(column, value))))

    def unatom(self, atom: int) -> Constraint[T]:
        pass

    def uniqueness(self, columns: Optional[List[str]] = None):
        if columns is None:
            uniqueness = [
                (col, u, w)
                for col, values in self.constraints.items()
                for (u, w) in itertools.combinations(values, 2)
            ]
        else:
            uniqueness = [
                (col, u, w)
                for col in columns
                for (u, w) in itertools.combinations(self.constraints.get(col, []), 2)
            ]

        return all_(
            ~(self.atom(col, u) & self.atom(col, w)) for (col, u, w) in uniqueness
        )
