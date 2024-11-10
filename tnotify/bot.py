import asyncio
import multiprocessing
from typing import Any

from aiogram import Bot as AIOBot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .bot_funcs import setup_handlers
from .logger import Logger


class Bot:
    def __init__(self, bot_token: str, logger: Any = None, log_level: str | None = 'INFO') -> None:
        self.__logger = Logger(logger, log_level)

        self.__dp = Dispatcher()
        self.__bot = AIOBot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

        self.__polling_process = None

        setup_handlers(self.__dp, self.__logger)

    def start_polling(self, event_loop: asyncio.BaseEventLoop) -> None:
        self.__loop = event_loop
        if self.__polling_process is None:
            self.__polling_process = multiprocessing.Process(
                target=self.__start_async_start_polling,
                daemon=True,
            )
            self.__polling_process.start()

    def start_without_polling(self) -> None:
        pass

    def __start_async_start_polling(self) -> None:
        self.__loop.run_until_complete(self.start_polling_async())

    async def start_polling_async(self) -> None:
        self.__logger.log('INFO', 'Bot starting')
        await self.__dp.start_polling(self.__bot)
