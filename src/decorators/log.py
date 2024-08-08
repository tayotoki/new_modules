import datetime
import functools
from collections.abc import Callable
from pathlib import Path
from typing import Any, Optional

import logging

logger = logging.getLogger(__name__)


def write_to_file(filename: Path, message: str, *message_params: Any) -> None:
    """Записывает сообщение в файл"""

    with open(filename, "a") as file:
        file.write(message % message_params)


def configure_logger(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="[%(asctime)s:%(levelname)s] %(message)s",
    )


def log(filename: Optional[Path] = None) -> Callable[..., Any]:
    """Декоратор для логгирования выполнения функций"""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
            configure_logger()
            if isinstance(filename, Path):
                with open(filename, "w") as _:
                    pass

            log_prefix = f"[{datetime.datetime.now(datetime.UTC)}]"
            success_message = "Функция %s - ок\n"
            exception_message = "Ошибка %s при выполнении функции %s c аргументами %s, %s\n"

            try:
                result = func(*args, **kwargs)
                (
                    write_to_file(filename, log_prefix + success_message, func.__name__)
                    if filename is not None
                    else logger.info(success_message % func.__name__)
                )
                return result
            except Exception as e:
                (
                    write_to_file(filename, log_prefix + exception_message, e, func.__name__, args, kwargs)
                    if filename is not None
                    else logger.error(
                        exception_message %
                        (e, func.__name__, args, kwargs)
                    )
                )
                raise
        return wrapper
    return decorator
