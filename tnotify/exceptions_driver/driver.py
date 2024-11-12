from functools import lru_cache

from .exceptions_parser import ExceptionsParser


__all__ = ('ExceptionDriver',)

class ExceptionDriver:
    def __init__(self, lru_cache_maxsize: int = 256):  # noqa: ANN204
        self.__exceptions_parser = ExceptionsParser()
        self.lru_cache_maxsize = lru_cache_maxsize

    @lru_cache(maxsize=256)
    def parse(self, exception: BaseException) -> dict:
        _parsed_ex = self.__exceptions_parser.parse(exception)
        return _parsed_ex
