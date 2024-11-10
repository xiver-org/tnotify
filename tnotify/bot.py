import asyncio
import multiprocessing
from typing import Any

from aiogram import Bot as AIOBot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .bot_funcs import setup_handlers
from .logger import Logger

loop = asyncio.get_event_loop()

class Bot:
    def __init__(self, bot_token: str, logger: Any = None, log_level: str | None = 'INFO') -> None:
        self.__logger = Logger(logger, log_level)

        self.__dp = Dispatcher()
        self.__bot = AIOBot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

        self.__polling_process = None

        self.__handlers = setup_handlers(self.__dp, self.__logger)

    def start_polling(self) -> None:
        if self.__polling_process is None:
            self.__polling_process = multiprocessing.Process(
                target=self.__start_async_start_polling,
                daemon=True,
            )
            self.__polling_process.start()

    def start_without_polling(self) -> None:
        pass

    def __start_async_start_polling(self) -> None:
        self.__loop = asyncio.get_event_loop()
        self.__loop.run_until_complete(self.__async_start_polling())

    async def __async_start_polling(self) -> None:
        self.__logger.log('INFO', 'Bot starting')
        await self.__dp.start_polling(self.__bot)
