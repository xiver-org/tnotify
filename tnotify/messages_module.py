import asyncio
from typing import Any

from aiogram import Bot

from .bot_config import MessageConfig
from .database import DataBase
from .exceptions_driver import ExceptionsDriver

__all__ = ('MessagesModule',)

class MessagesModule:
    def __init__(
        self,
        bot: Bot,
        database: DataBase,
        logger: Any,
        config: MessageConfig,
    ) -> None:
        self.__bot = bot
        self.__config = config
        self.__database = database
        self.__logger = logger

        self.__exceptions_driver = ExceptionsDriver()

    def exception(self, ex: BaseException, extra_info: str | None = None) -> None:
        parsed_ex = self.__exceptions_driver.parse(ex)
        parsed_ex["extra_info"] = extra_info

        def parse_dict(d: dict) -> dict:
            a = {}
            for key, value in d.items():
                if isinstance(value, dict):
                    for k, v in parse_dict(value).items():
                        a[k] = v
                else:
                    a[key] = value

            return a

        ready_dict = parse_dict(parsed_ex)

        message = self.__config.exception_template

        for k, v in ready_dict.items():
            try:
                message = message.format(**{k: v})
            except Exception:
                pass

        # loop = asyncio.get_running_loop()
        for user in self.__database.get_users_with_perm(['GetNotifyExceptions']):
            # try:
            # loop.run_until_complete()
            asyncio.to_thread(self.__bot.send_message(user.id, message))
            # except Exception as e:
            #     self.__logger.log("ERROR", f"Fail while sending message to {user.id}: {e}")

        self.__logger.log("TRACE", "End of broadcast")
