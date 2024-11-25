from .exceptions_parser import ExceptionsParser

__all__ = ('ExceptionsDriver',)

class ExceptionsDriver:
    def __init__(self, lru_cache_maxsize: int = 256):  # noqa: ANN204
        self.__exceptions_parser = ExceptionsParser()
        self.lru_cache_maxsize = lru_cache_maxsize

        self.__cache = {}

    async def parse(self, exception: BaseException) -> dict:
        if exception in self.__cache:
            return self.__cache[exception]

        self.__cache[exception] = await self.__exceptions_parser.parse(exception)
        return self.__cache[exception]
