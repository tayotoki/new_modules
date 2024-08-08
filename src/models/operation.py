from dataclasses import dataclass

from ..processing.constants import StateType


@dataclass
class Currency:
    name: str
    code: str


@dataclass
class OperationAmount:
    amount: str
    currency: Currency


@dataclass
class Operation:
    id: int
    state: StateType
    date: str
    description: str
    from_: str
    to: str
    operation_amount: OperationAmount
