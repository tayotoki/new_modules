import functools
import logging
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)


def exc_logger(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: tuple[Any], **kwargs: dict[Any, Any]) -> Any:
        try:
            result = func(*args, **kwargs)
        except (TypeError, ValueError) as e:
            # TODO: добавить логгирование в файл или sentry
            logger.error(f"Ошибка в функции {func.__name__}: " f"{e}")
            raise
        return result

    return wrapper
