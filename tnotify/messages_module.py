from aiogram import Bot

from .bot_config import MessageConfig


__all__ = ('MessagesModule',)

class MessagesModule:
    def __init__(self, bot: Bot, config: MessageConfig) -> None:
        self.__bot = bot
        self.__config = config
