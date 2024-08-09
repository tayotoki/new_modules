from copy import deepcopy
from string import ascii_uppercase
from typing import Any, Optional

from src.models.operation import Operation


class OperationConverter:
    """
    Конвертер json данных в датакласс операции
    """

    MODEL = Operation

    def __init__(self, operation: dict[str, Any]) -> None:
        self._model: Optional[Operation] = None
        self.operation = operation

    @property
    def model(self) -> Operation:
        if self._model is None:
            operation = self._from_camel_to_snake(self.operation)
            self._model = self.MODEL(**operation)
        return self._model

    def _from_camel_to_snake(self, dict_: dict) -> dict[str, Any]:
        """
        Рекурсивное изменение ключей словаря из camelCase в snake_case
        """

        operation_copy = deepcopy(dict_)
        for key, value in operation_copy.items():
            if isinstance(value, dict):
                self._from_camel_to_snake(value)
            else:
                if intersection := (set(key) & set(ascii_uppercase)):
                    for char in key:
                        if char in intersection:
                            key = key.replace(char, f"_{char.lower()}")
                        self.operation.update({key: value})
                if key == "from":
                    self.operation["from_"] = self.operation.pop("from")
        return self.operation
