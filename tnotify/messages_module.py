from aiogram import Bot

from .bot_config import MessageConfig
from .database import DataBase
from .exceptions_driver import ExceptionsDriver

__all__ = ('MessagesModule',)

class MessagesModule:
    def __init__(self, bot: Bot, database: DataBase, config: MessageConfig) -> None:
        self.__bot = bot
        self.__config = config
        self.__database = database

        self.__exceptions_driver = ExceptionsDriver()

    def exception(self, ex: BaseException, extra_info: str | None = None) -> None:
        pass
