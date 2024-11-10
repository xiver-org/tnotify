from typing import Callable

from aiogram import Dispatcher, Bot

__all__ = ('misc',)


class Misc:
    def setup(self, dispatcher: Dispatcher, bot: Bot, logger: Callable) -> None:
        self.dispatcher: Dispatcher = dispatcher
        self.bot: Bot = bot
        self.logger: Callable = logger
        


misc = Misc()
