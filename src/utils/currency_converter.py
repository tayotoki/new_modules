from enum import Enum
from typing import Any

import requests

from src.settings import CONVERTER_API_URL, CONVERTER_API_KEY


class CurrencyType(Enum):
    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"


def rouble_converter(operation: dict[str, Any]) -> float:
    amount_info = operation["operationAmount"]
    currency = amount_info["currency"]["code"]
    amount = float(amount_info["amount"])
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
                    return res_json["result"]
        except requests.exceptions.RequestException:
            pass
