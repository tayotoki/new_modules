from unittest import mock

import pytest

from src.masks.constants import InvoiceType
from src.masks.funcs import get_mask_account, get_mask_card_number


@pytest.fixture
def card_numbers():
    return {
        "integer": 1111222233334444,
        "string": "1111222233334444",
        "integer_bad_len": 111122223333444,
        "string_bad_len": "111122223333444",
        "string_non_numeric": "1111ffff33334444",
        "bad_type": 10.594,
    }


@pytest.fixture
def invoice_numbers():
    return {
        "integer": 11112222333344445555,
        "string": "11112222333344445555",
        "integer_bad_len": 1111222233334444555,
        "string_bad_len": "1111222233334444555",
        "string_non_numeric": "1111222233334444aaaa",
        "bad_type": 10.594,
    }


@pytest.fixture
def mock_validator():
    """Возвращает мок-объект класса валидатора"""

    validator_patcher = mock.patch(
        "src.masks.validators.InvoiceValidator",
        autospec=True,
    )
    ValidatorMock = validator_patcher.start()  # noqa
    yield ValidatorMock
    validator_patcher.stop()


class MockSideEffects:
    """Мок-ошибки при вызове мок-класса"""

    @classmethod
    def side_effect_type(cls):
        raise TypeError

    @classmethod
    def side_effect_non_numeric(cls):
        raise ValueError

    @classmethod
    def side_effect_wrong_card_len(cls):
        raise ValueError


def test_get_mask_card_number(card_numbers, mock_validator):
    for test_case, value in card_numbers.items():
        if test_case in ["integer", "string"]:
            mocked_instance = mock_validator(value, InvoiceType.CARD)
            mocked_instance.validated_data = str(value)
            assert get_mask_card_number(value) == "1111 22** **** 4444"
        elif test_case == "bad_type":
            mock_validator.side_effect = MockSideEffects.side_effect_type
            with pytest.raises(TypeError):
                get_mask_card_number(value)
        elif test_case in ["integer_bad_len", "string_bad_len"]:
            mock_validator.side_effect = MockSideEffects.side_effect_wrong_card_len
            with pytest.raises(ValueError):
                get_mask_card_number(value)
        elif test_case == "string_non_numeric":
            mock_validator.side_effect = MockSideEffects.side_effect_non_numeric
            with pytest.raises(ValueError):
                get_mask_card_number(value)

        mock_validator.assert_called()


def test_get_mask_account(invoice_numbers, mock_validator):
    for test_case, value in invoice_numbers.items():
        if test_case in ["integer", "string"]:
            mocked_instance = mock_validator(value, InvoiceType.INVOICE)
            mocked_instance.validated_data = str(value)
            assert get_mask_account(value) == "**5555"
        elif test_case == "bad_type":
            mock_validator.side_effect = MockSideEffects.side_effect_type
            with pytest.raises(TypeError):
                get_mask_account(value)
        elif test_case in ["integer_bad_len", "string_bad_len"]:
            mock_validator.side_effect = MockSideEffects.side_effect_wrong_card_len
            with pytest.raises(ValueError):
                get_mask_account(value)
        elif test_case == "string_non_numeric":
            mock_validator.side_effect = MockSideEffects.side_effect_non_numeric
            with pytest.raises(ValueError):
                get_mask_account(value)

        mock_validator.assert_called()
