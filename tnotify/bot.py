import multiprocessing
from typing import Any
import asyncio

from aiogram import Bot as AIOBot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

from .logger import Logger


loop = asyncio.get_event_loop()

class Bot:
    def __init__(self, bot_token: str, logger: Any = None, log_level: str | None = 'INFO') -> None:
        self.__logger = Logger(logger, log_level)

        self.__dp = Dispatcher()
        self.__bot = AIOBot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        
        self.__polling_process = None
        
    def start_polling(self) -> None:
        if self.__polling_process is None:
            print(2)
            self.__polling_process = multiprocessing.Process(
                target=self.__start_async_start_polling,
                daemon=True,
            )
            self.__polling_process.start()
            print(3)
    
    def start_without_polling(self) -> None:
        pass
    
    def __start_async_start_polling(self) -> None:
        self.__loop = asyncio.get_event_loop()
        self.__loop.run_until_complete(self.__async_start_polling())
    
    async def __async_start_polling(self) -> None:
        print(4)
        self.__logger.log('INFO', 'Bot starting')
        await self.__dp.start_polling(self.__bot)
        