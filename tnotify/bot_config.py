from typing import Any


__all__ = ('BotConfig',)

class BotConfig:
    def __init__(
        self,
        bot_token: str,
        logger: Any = None,
        log_level: str | None = 'INFO',
    ) -> None:
        self.bot_token = bot_token
        self.logger = logger
        self.log_level = log_level