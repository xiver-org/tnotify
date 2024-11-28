from aiogram.filters import Command
from aiogram.types import Message

from tnotify.admin import admin_panel

from .router import handlers_router

__all__ = ('admin_handler',)

@handlers_router.message(Command('admin'))
async def admin_handler(message: Message) -> None:
    await admin_panel(message)
