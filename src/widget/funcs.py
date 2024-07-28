import re
from typing import Optional

from dateutil import parser

from src.masks.constants import InvoiceType

from .utils import mask_all_data


def mask_account_card(card_info: str) -> Optional[str]:
    """Возвращает замаскированные данные карты/счета"""

    invoice_pattern = re.compile(r"^Сч(?:е|ё)т (?P<number>\d{20})$")
    card_pattern = re.compile(r".*(?P<number>\d{16})$")

    matches = [re.match(pattern, card_info) for pattern in [invoice_pattern, card_pattern]]

    match matches:
        case [re.Match() as number, None]:
            type_ = InvoiceType.INVOICE
            return mask_all_data(info=card_info, match_obj=number, type_=type_)

        case [None, re.Match() as number]:
            type_ = InvoiceType.CARD
            return mask_all_data(info=card_info, match_obj=number, type_=type_)

    return None  # требование mypy


def get_date(datetime_: str) -> str:
    parsed: str = parser.parse(datetime_).strftime("%d.%m.%Y")
    return parsed
