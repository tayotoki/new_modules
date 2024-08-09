from unittest import mock

import pytest

from src.utils.currency_converter import rouble_converter


@pytest.fixture
def single_transaction():
    return {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589",
    }


@mock.patch("requests.get")
def test_rouble_converter(mock_requests, single_transaction):
    mock_requests.return_value.json.return_value = {"success": True, "result": 10000}
    mock_requests.return_value.status_code = 200
    assert rouble_converter(single_transaction) == 10000
    mock_requests.assert_called_once()
