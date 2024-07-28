from typing import Any, Optional

from .constants import InvoiceType


class InvoiceValidator:
    """Валидатор номеров карт и счетов"""

    def __init__(self, number: str | int, type_: InvoiceType) -> None:
        self.number = number
        self.type = type_
        self.len_check = self._len_check()
        self._validated_data: Optional[str] = None

    def validate(self) -> str:
        """Валидация номера карты/счета"""

        match self.validated_data:
            case None:
                self.validated_data = self.number
                return self.validate()
            case int():
                self.validated_data = str(self.number)
                return self.validate()
            case str():
                if not self.validated_data.isalnum():
                    raise ValueError(
                        f"Номер карты/счета содержит нечисловые значения: "
                        f"{[symbol for symbol in self.validated_data if not symbol.isdigit()]}"
                    )
                if len(self.validated_data) != self.len_check:
                    raise ValueError(
                        f"Непредвидимая длина счета/карты: {len(self.validated_data)}, \n"
                        f"ожидается {self.len_check} для типа {self.type.name}"
                    )
            case _:
                raise TypeError(f"Неправильный тип номера {self.number.__class__}")

        return self.validated_data

    @property
    def validated_data(self) -> str:
        if self._validated_data is None:
            return self.validate()
        return self._validated_data

    @validated_data.setter
    def validated_data(self, value: Any) -> None:
        self._validated_data = value

    def _len_check(self) -> Optional[int]:
        match self.type:
            case InvoiceType.CARD:
                return 16
            case InvoiceType.INVOICE:
                return 20
