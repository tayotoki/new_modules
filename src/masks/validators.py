from typing import Any, Optional

from .constants import InvoiceType


class InvoiceValidator:
    """Валидатор номеров карт и счетов"""

    def __init__(self, number: str | int, type_: InvoiceType) -> None:
        self.number = number
        self.type = type_
        self.len_check = self._len_check()
        self._validated_data: Optional[str | int] = None

    def _validate(self) -> str:
        """Валидация номера карты/счета"""

        match self._validated_data:
            case None:
                self._validated_data = self.number
                return self._validate()
            case int():
                self._validated_data = str(self.number)
                return self._validate()
            case str() | bytes():
                if not self._validated_data.isnumeric():
                    raise ValueError(
                        f"Номер карты/счета содержит нечисловые значения: "
                        f"{[symbol for symbol in self._validated_data if not symbol.isdigit()]}"
                    )
                if len(self._validated_data) != self.len_check:
                    raise ValueError(
                        f"Непредвидимая длина счета/карты: {len(self._validated_data)}, \n"
                        f"ожидается {self.len_check} для типа {self.type.name}"
                    )
            case _:
                raise TypeError(f"Неправильный тип номера {self.number.__class__}")

        return self._validated_data

    @property
    def validated_data(self) -> str:
        return self._validate()

    @validated_data.setter
    def validated_data(self, value: Any) -> None:
        self._validated_data = value

    def _len_check(self) -> Optional[int]:
        match self.type:
            case InvoiceType.CARD:
                return 16
            case InvoiceType.INVOICE:
                return 20
