from .exceptions_parser import ExceptionsParser

__all__ = ('ExceptionDriver',)

class ExceptionDriver:
    def __init__(self, lru_cache_maxsize: int = 256):  # noqa: ANN204
        self.__exceptions_parser = ExceptionsParser()
        self.lru_cache_maxsize = lru_cache_maxsize

        self.__cache = {}

    def parse(self, exception: BaseException) -> dict:
        if exception in self.__cache:
            return self.__cache[exception]

        self.__cache[exception] = self.__exceptions_parser.parse(exception)
        return self.__cache[exception]
