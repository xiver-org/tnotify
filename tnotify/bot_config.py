from typing import Any

__all__ = ('BotConfig', 'MessageConfig', 'DatabaseConfig',)

exception_template = """
*!EXCEPTION!*

__{filename}:{function_name}:{line_number}__ *{message}*

Extra info: `{extra_info}`

_All info about exception in pinned file_

`Message by tnotify`
"""

info_message_template = """
*Info*

{message}

Extra info: `{extra_info}`

`Message by tnotify`
"""


class MessageConfig:
    def __init__(
        self,
        exception_template: str = exception_template,
        info_template: str = info_message_template,
    ) -> None:
        self.exception_template = exception_template
        self.info_template      = info_template


class DatabaseConfig:
    def __init__(
        self,
        sqlite_db_path: str,
    ) -> None:
        self.sqlite_db_path = sqlite_db_path


class BotConfig:
    def __init__(
        self,
        bot_token: str,
        logger: Any = None,
        log_level: str | None = 'INFO',
        master_id: int | None = None,

        message_config: MessageConfig = MessageConfig(),  # noqa: B008
        database_config: DatabaseConfig = DatabaseConfig('tnotify_db.sqlite3'),  # noqa: B008
    ) -> None:
        self.bot_token = bot_token
        self.logger = logger
        self.log_level = log_level
        self.master_id = master_id

        self.message_config = message_config
        self.database_config = database_config
