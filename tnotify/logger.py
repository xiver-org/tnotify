from typing import Any


class Logger:
    def __init__(self, logger: Any, log_level: str | None) -> None:
        self.__update_cfg(logger, log_level)

    def config(self, logger: Any, log_level: str | None) -> None:
        self.__update_cfg(logger, log_level)

    def __update_cfg(self, logger: Any, log_level: str | None) -> None:
        self.__logger = logger

        if logger is False:
            self.log = lambda *arg, **kwargs: ...

        elif logger is None:
            self.log = self.__log_with_print

            self.__log_levels = {
                'FATAL': 1,
                'ERROR': 2,
                'WARN' : 3,
                'INFO' : 4,
                'DEBUG': 5,
                'TRACE': 6,
            }
            self.__log_level: int = self.__log_levels[log_level]

        else:
            self.log = self.__log_with_logger


    def __log_with_print(self, type: str, message: str) -> None:
        if self.__check_log_level(type):
            print(f'[{type}]: {message}')

    def __log_with_logger(self, type: str, message: str) -> None:
        if self.__check_log_level(type):
            self.__logger.__getattribute__(type.lower())(message)

    def __check_log_level(self, level: str) -> bool:
        _level = self.__log_levels[level]
        if _level <= self.__log_level:
            return True
        return False


logger = Logger(None, 'INFO')
