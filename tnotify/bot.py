import asyncio
from threading import Thread
from typing import Any

from aiogram import Bot as AIOBot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .bot_config import BotConfig
from .database import DEFAULT_MASTER_PERMISSIONS, DataBase
from .handlers import handlers_router
from .logger import logger as _logger
from .messages_module import MessagesModule

__all__ = ('Bot',)

class Bot:
    def __init__(self, config: BotConfig) -> None:
        self.__config = config

        self.__logger = _logger
        self.__logger.config(self.__config.logger, self.__config.log_level)

        self.__database = DataBase(self.__logger, self.__config.database_config)
        self.__database.init_database()
        if self.__config.master_id:
            self.__logger.log('TRACE', 'Master getted')
            self.__database.add_user(self.__config.master_id, DEFAULT_MASTER_PERMISSIONS)
            self.__logger.log('INFO', 'Master added')

        self.__loop = None
        self.__loop_thread = None

        self.__dp = Dispatcher()
        self.__bot = AIOBot(token=self.__config.bot_token,
                            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))

        # Include routers
        self.__dp.include_router(handlers_router)

        self.__dp.resolve_used_update_types()

        self.__started = False

        self.message = MessagesModule(self.__bot, self.__database, self.__config.message_config)

    def start_polling(self) -> None:
        if self.__started is False:
            self.__logger.log('INFO', 'Bot starting')
            self.__started = True
            self.__loop_thread = Thread(target=self.__dp.run_polling(self.__bot), daemon=False)
            self.__loop_thread.start()
            self.__logger.log('INFO', 'Bot started')

        else:
            self.__logger.log('ERROR', 'Bot already started! Close befor start')

    def stop_polling(self) -> None:
        # cleanup routers
        def cleanup_sub_routers(router: Any) -> None:
            if router._parent_router is not None:
                router._parent_router = None

            for __router in router.sub_routers:
                cleanup_sub_routers(__router)
        cleanup_sub_routers(self.__dp)

        if self.__started is True:
            asyncio.run_coroutine_threadsafe(self.__dp.stop_polling(), self.__loop)

            self.__loop.stop()

            self.__logger.log('TRACE', 'Loop stopped')

        else:
            self.__logger.log('ERROR', 'Bot not started!')
            return

        self.__started = False

        self.__loop_thread.join()
        self.__logger.log('INFO', 'Bot closed')

    def __exit__(self, *args: Any) -> None:
        self.__logger.log('TRACE', 'Bot.__exit__ called')
        self.stop_polling()
