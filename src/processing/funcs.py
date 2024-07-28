from typing import Any

from dateutil import parser


def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрация данных по указанному состоянию"""

    filtered_data = [
        operation for operation in operations
        if operation.get("state") == state
    ]

    return filtered_data


def sort_by_date(operations: list[dict[str, str | Any]], reverse: bool = True) -> list[dict]:
    """Сортировка операций по дате"""

    try:
        sorted_data = sorted(
            operations,
            key=lambda operation: parser.parse(operation.get("data")),  # type: ignore[arg-type]
            reverse=reverse
        )
        return sorted_data
    except parser.ParserError:
        return operations
