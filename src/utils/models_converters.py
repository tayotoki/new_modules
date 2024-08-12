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
        self._camel_operation = operation
        self._snake_operation = self._camel_operation

    @property
    def model(self) -> Operation:
        """Получение python объекта из json-объекта операции"""

        if self._model is None:
            operation = self._from_camel_to_snake(self._camel_operation)
            self._model = self.MODEL(**operation)
        return self._model

    def _from_camel_to_snake(
        self, dict_: dict, base_snake_dict: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Рекурсивное изменение ключей словаря из camelCase в snake_case
        """
        snake_dict = base_snake_dict or self._camel_operation

        for key, value in dict_.items():
            if isinstance(value, dict):
                self._from_camel_to_snake(value, snake_dict[key])
        new_keys = [
            self.convert_string_to_snake_case(key) for key in snake_dict
        ]
        old_keys = deepcopy(list(snake_dict.keys()))
        for new_key, old_key in zip(new_keys, old_keys):
            if new_key == old_key == "from":
                new_key = "from_"
            snake_dict[new_key] = snake_dict.pop(old_key)

        return self._camel_operation

    @staticmethod
    def convert_string_to_snake_case(string: str) -> str:
        snake_string: str = ""
        if intersection := (set(string) & set(ascii_uppercase)):
            for char in intersection:
                snake_string += string.replace(char, f"_{char.lower()}")
        return snake_string if snake_string else string
