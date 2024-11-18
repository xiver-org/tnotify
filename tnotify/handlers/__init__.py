from .commands import commands_router
from .echo import echo_handler  # noqa:F401
from .router import handlers_router

__all__ = ('handlers_router',)

handlers_router.include_router(commands_router)
