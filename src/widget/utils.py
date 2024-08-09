import re

from src.masks.constants import InvoiceType
from src.masks.funcs import get_mask_account, get_mask_card_number


def mask_all_data(info: str, match_obj: re.Match, type_: InvoiceType) -> str:
    """Замена открытого номера карты/счета в маскированный"""

    number: str = match_obj.group("number")
    masked_number: str = ""

    if type_ == InvoiceType.INVOICE:
        masked_number = get_mask_account(number=number)
    elif type_ == InvoiceType.CARD:
        masked_number = get_mask_card_number(number=number)

    info = " ".join(info.split()[:-1] + [masked_number])

    return info
