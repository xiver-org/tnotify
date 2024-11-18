import asyncio
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from typing import Any

from aiogram import Bot as AIOBot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .handlers import commands_router
from .logger import logger as _logger

__all__ = ('Bot',)

class Bot:
    def __init__(self, bot_token: str, logger: Any = None, log_level: str | None = 'INFO') -> None:
        self.__logger = _logger
        self.__logger.config(logger, log_level)

        self.__loop = None
        self.__loop_thread = None

        self.__dp = Dispatcher()
        self.__bot = AIOBot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

        # Include routers
        self.__dp.include_router(commands_router)

        self.__started = False

    def start_polling(self) -> None:
        if self.__started is False:
            self.__loop = asyncio.get_event_loop()
            self.__loop_thread = Thread(target=self.__start_loop, daemon=False)
            self.__loop_thread.start()
            asyncio.run_coroutine_threadsafe(self.__start_polling(), self.__loop)

        else:
            self.__logger.log('ERROR', 'Bot already started! Close befor start')

    def stop_polling(self) -> None:
        # cleanup routers
        for __router in self.__dp.sub_routers:
            __router._parent_router = None

        if self.__started is True:
            asyncio.run_coroutine_threadsafe(self.__dp.stop_polling(), self.__loop)

            self.__loop.stop()
            # self.__dp.stop_polling()

            self.__logger.log('TRACE', 'Loop stopped')

        else:
            self.__logger.log('ERROR', 'Bot not started!')
            return

        self.__started = False

        self.__logger.log('TRACE', 'Bot stopped')
        self.__loop_thread.join()
        self.__logger.log('TRACE', 'Loop stopped')
        self.__logger.log('INFO', 'Bot closed')

    async def __start_polling(self) -> None:
        if self.__started is True:
            self.__loop.stop()
            self.__logger.log('WARNING', 'Bot already started! Closed.')

        self.__logger.log('INFO', 'Bot starting')
        self.__started = True
        with ThreadPoolExecutor() as executor:
            await self.__loop.run_in_executor(executor, asyncio.run, self.__dp.start_polling(self.__bot))

    def __start_loop(self) -> None:
        """Start the asyncio loop in a separate thread."""
        asyncio.set_event_loop(self.__loop)
        self.__loop.run_forever()

    def __exit__(self, *args: Any) -> None:
        self.stop_polling()
