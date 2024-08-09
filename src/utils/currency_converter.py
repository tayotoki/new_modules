import logging
from enum import Enum
from typing import TypeVar

import requests

from src.settings import CONVERTER_API_KEY, CONVERTER_API_URL

NestedDict = TypeVar("NestedDict", bound=dict[str, dict[str, dict[str, str]]])

logger = logging.getLogger(__name__)


class CurrencyType(Enum):
    """Типы валюты"""

    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"


def rouble_converter(operation: NestedDict) -> float | None:
    """
    Если транзакция выполнена в USD или EUR
    возвращает сумму, конвертированную в рубли
    """

    amount_info = operation["operationAmount"]
    currency = amount_info["currency"]["code"]
    amount = amount_info["amount"]
    if currency in [CurrencyType.EUR.value, CurrencyType.USD.value]:
        try:
            params = {
                "amount": amount,
                "from": currency,
                "to": CurrencyType.RUB.value,
            }
            headers = {
                "apikey": CONVERTER_API_KEY,
            }
            response: requests.Response = requests.get(
                url=CONVERTER_API_URL,
                params=params,
                headers=headers,
            )
            if response.status_code == 200:
                res_json = response.json()

                if res_json["success"] is True:
                    converted_amount: float = res_json["result"]
                    return converted_amount
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True)
    return None  # требование mypy
