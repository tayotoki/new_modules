from copy import deepcopy
from typing import Any, Optional

from src.models.operation import Operation
from string import ascii_uppercase


class OperationConverter:
    MODEL = Operation

    def __init__(self, operation: dict[str, Any]):
        self._model: Optional[Operation] = None
        self.operation = operation

    @property
    def model(self):
        if self._model is None:
            operation = self._from_camel_to_snake()
            self._model = self.MODEL(**operation)
        return self._model

    def _from_camel_to_snake(self) -> dict[str, Any]:
        operation_copy = deepcopy(self.operation)
        for key, value in operation_copy.items():
            if isinstance(value, dict):
                self._from_camel_to_snake()
            else:
                if intersec := (set(key) & set(ascii_uppercase)):
                    for char in key:
                        if char in intersec:
                            key = key.replace(char, f"_{char.lower()}")
                        self.operation.update({key: value})
                if key == "from":
                    self.operation["from_"] = self.operation.pop("from")
        return self.operation
