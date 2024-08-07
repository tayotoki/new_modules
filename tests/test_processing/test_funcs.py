import pytest

from src.processing.constants import StateType
from src.processing.funcs import filter_by_state, sort_by_date


@pytest.fixture
def transactions_info_state_date():
    return [
        {
            'id': 41428829,
            'state': 'EXECUTED',
            'date': '2019-07-03T18:35:29.512364'
        },
        {
            'id': 939719570,
            'state': 'EXECUTED',
            'date': '2018-06-30T02:08:58.425572'
        },
        {
            'id': 594226727,
            'state': 'CANCELED',
            'date': '2018-09-12T21:27:25.241689'
        },
        {
            'id': 615064591,
            'state': 'CANCELED',
            'date': '2018-10-14T08:21:33.419441'
        }
    ]


def test_filter_by_state(transactions_info_state_date):
    assert len(filter_by_state(transactions_info_state_date, state=StateType.EXECUTED)) == 2
    assert len(filter_by_state(transactions_info_state_date, state=StateType.CANCELED)) == 2
    assert len(filter_by_state(transactions_info_state_date, state="")) == 0


def test_sort_by_date(transactions_info_state_date):
    expected_ids = [939719570, 594226727, 615064591, 41428829]
    result_desc = sort_by_date(transactions_info_state_date)
    assert [operation["id"] for operation in result_desc] == expected_ids[::-1]
    result_asc = sort_by_date(transactions_info_state_date, reverse=False)
    assert [operation["id"] for operation in result_asc] == expected_ids
