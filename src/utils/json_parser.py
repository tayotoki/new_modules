import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# class JsonParser:
#     def __init__(self, json_file: Path):
#         self.json_file = json_file
#
#     def get_data(self) -> list[dict]:
#         """Возвращает список словарей из json массива объектов"""
#
#         default_result: list = []
#         try:
#             with open(self.json_file, "r", encoding="utf-8") as f:
#                 raw_data = json.load(f)
#                 if not isinstance(raw_data, list):
#                     raise ValueError(
#                         "Неправильная структура файла "
#                         "Ожидается массив объектов, получено: "
#                         "%s" % raw_data.__class__
#                     )
#                 default_result = raw_data
#         except (FileNotFoundError, ValueError) as e:
#             logger.error(
#                 "Исключение в классе %s, метод %s",
#                 self.__class__.__name__, self.get_data.__name__,
#                 exc_info=True
#             )
#         return default_result
#
#     @classmethod
#     def parse_dict(cls, data: dict, result_data: Optional[dict] = None) -> dict | None:
#         """
#         Рекурсивный обходчик словаря, преобразует вложенный словарь в плоский
#         """
#
#         result_data = {} if not result_data else result_data
#
#         for key, value in data.items():
#             if type(value) is dict:
#                 cls.parse_dict(data[key], result_data)
#             else:
#                 result_data.update({key: value})
#
#         return result_data


def parse_json_file(file_path: Path) -> list[dict]:
    """
    Возвращает список словарей из json-файла
    """

    default_result: list = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data: list[dict] = json.load(file)
            if not isinstance(data, list):
                raise TypeError
            default_result = data
    except (FileNotFoundError, TypeError, json.JSONDecodeError) as e:
        logger.error(e, exc_info=True)
    return default_result
