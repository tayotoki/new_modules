import pytest

from src.decorators.log import log


def test_log(caplog, tmp_path):
    test_file_name = tmp_path / "test_log.txt"

    @log()
    def _func_non_file(a, b):
        return a / b

    @log(test_file_name)
    def _func_with_file(a, b):
        return a / b

    with pytest.raises(Exception):
        _func_non_file(1, 0)
        assert "Ошибка" in caplog.text
    caplog.clear()

    _func_non_file(1, 1)
    assert "ок" in caplog.text

    _func_with_file(1, 1)
    with open(tmp_path / test_file_name, "r") as file:
        assert "ок" in file.read()
    caplog.clear()

    with pytest.raises(Exception):
        _func_with_file(1, 0)
        with open(tmp_path / test_file_name, "r") as file:
            assert "Ошибка" in file.read()
