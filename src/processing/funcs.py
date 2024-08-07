from typing import Any

from dateutil import parser

from .constants import StateType


def filter_by_state(operations: list[dict], state: StateType | Any = StateType.EXECUTED) -> list[dict]:
    """Фильтрация данных по указанному состоянию"""

    filtered_data = [
        operation for operation in operations
        if operation.get("state") == getattr(state, "value", None)
    ]

    return filtered_data


def sort_by_date(operations: list[dict[str, str | Any]], reverse: bool = True) -> list[dict]:
    """Сортировка операций по дате"""

    try:
        sorted_data = sorted(
            operations,
            key=lambda operation: parser.parse(operation.get("date")),  # type: ignore[arg-type]
            reverse=reverse
        )
        return sorted_data
    except parser.ParserError:
        return operations
