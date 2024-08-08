import pytest

from src.widget.funcs import mask_account_card, get_date


@pytest.mark.parametrize(
    "number,expected_result",
    [
        ("Visa Platinum 1111222233334444", "Visa Platinum 1111 22** **** 4444"),
        ("Счет 11112222333344445555", "Счет **5555"),
        ("", None)
    ]
)
def test_mask_account_card(number, expected_result):
    assert mask_account_card(number) == expected_result


@pytest.mark.parametrize(
    "string_date,handled_date",
    [
        ("2023-10-01T15:30:00", "01.10.2023"),
        ("March 5, 2021", "05.03.2021"),
        ("12/09/2020", "09.12.2020"),
        ("2022-12-31", "31.12.2022"),
        ("01-01-2000 10:00 AM", "01.01.2000"),
        ("July 4, 1776 14:00", "04.07.1776"),
        ("2023.11.15 17:30:00", "15.11.2023"),

    ]
)
def test_get_date(string_date, handled_date):
    assert get_date(string_date) == handled_date
