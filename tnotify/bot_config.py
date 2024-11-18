from typing import Any

__all__ = ('BotConfig', 'MessageConfig')

__exception_template = """
*!EXCEPTION!*

__{filename}:{function_name}:{line_number}__ *{message}*

_All info about exception in pinned file_

`Message by tnotify`
"""

__info_message_template = """
*Info*

{message}

`Message by tnotify`
"""


class MessageConfig:
    def __init__(
        self,
        exception_template: str = __exception_template,
        info_template: str = __info_message_template,
    ) -> None:
        self.exception_template = exception_template
        self.info_template      = info_template


class BotConfig:
    def __init__(
        self,
        bot_token: str,
        logger: Any = None,
        log_level: str | None = 'INFO',

        message_config: MessageConfig = MessageConfig(),  # noqa: B008
    ) -> None:
        self.bot_token = bot_token
        self.logger = logger
        self.log_level = log_level
        self.message_config = message_config
