from collections.abc import Generator, Sequence

from .constants import InvoiceType
from .validators import InvoiceValidator


def get_mask_card_number(number: int | str) -> str:
    """Возвращает номер карты в виде xxxx xx** **** xxxx"""

    def get_chunks(obj: Sequence, size: int) -> Generator[Sequence, None, None]:
        """Делит объект, поддерживающий индексы, на чанки"""

        for i in range(0, len(obj), size):
            yield obj[i : i + size]  # noqa

    validated_number = InvoiceValidator(number, InvoiceType.CARD).validated_data
    chunked_card_numbers: list = []
    chunked_card_numbers.extend(get_chunks(validated_number, 4))

    masked_number = " ".join(
        [part if i in [0, 3] else f"{part[:2]}**" if i == 1 else "****" for i, part in enumerate(chunked_card_numbers)]
    )

    return masked_number


def get_mask_account(number: str | int) -> str:
    """Возвращает номер счета в виде **xxxx"""

    validated_number = InvoiceValidator(number, InvoiceType.INVOICE).validated_data

    return "**" + validated_number[-4:]
