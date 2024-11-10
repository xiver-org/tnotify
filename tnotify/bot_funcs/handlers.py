from aiogram import Dispatcher, html
from aiogram.filters import CommandStart
from aiogram.types import Message


__all__ = ('setup_handlers',)


def setup_handlers(dispatcher: Dispatcher, logger) -> None:

    @dispatcher.message(CommandStart())
    async def command_start_handler(message: Message) -> None:
        """
        This handler receives messages with `/start` command
        """
        logger.log('INFO', f'Takes start command from {message.from_user.full_name}')
        await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")