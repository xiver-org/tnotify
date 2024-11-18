from typing import Any

from aiogram.filters import CommandStart
from aiogram.types import Message

from tnotify.logger import logger

from .router import commands_router

__all__ = ('commands_router',)

@commands_router.message(CommandStart())
async def start_handler(message: Message) -> Any:
    """
    This handler receives messages with `/start` command
    """
    logger.log('INFO', f'Takes start command from {message.from_user.full_name}')
    await message.answer(f"Hello, *{message.from_user.full_name}*\\!")
