from typing import List, TypeVar, Generic, Optional, Dict

from dataclasses import dataclass

T = TypeVar("T")


@dataclass
class Constraint(Generic[T]):
    column: str
    value: T

    def __repr__(self):
        return f"{self.column} == {self.value}"

    def __str__(self):
        return f"{self.column} == {self.value}"

    def __hash__(self):
        return hash(repr(self))
