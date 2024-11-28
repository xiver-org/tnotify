import asyncio
import json
from io import BytesIO
from typing import Any

from aiogram import Bot, types

from .bot_config import MessageConfig
from .database import DataBase
from .exceptions_driver import ExceptionsDriver

__all__ = ('MessagesModule',)

class MessagesModule:
    def __init__(
        self,
        bot: Bot,
        database: DataBase,
        logger: Any,
        loop: asyncio.BaseEventLoop,
        config: MessageConfig,
    ) -> None:
        self.__bot = bot
        self.__config = config
        self.__database = database
        self.__loop = loop
        self.__logger = logger

        self.__exceptions_driver = ExceptionsDriver()

    async def exception(self, ex: BaseException, extra_info: str | None = None, pin_full_log: bool = True) -> None:
        parsed_ex = await self.__exceptions_driver.parse(ex)
        parsed_ex["extra_info"] = extra_info

        async def __parse_dict(d: dict) -> dict:
            a = {}
            for key, value in d.items():
                a[key] = value

                if isinstance(value, dict):
                    for k, v in (await __parse_dict(value)).items():
                        a[k] = v
                elif isinstance(value, list):
                    for i in value:
                        for k, v in (await __parse_dict(i)).items():
                            a[k] = v

            return a

        ready_dict = await __parse_dict(parsed_ex)

        message = self.__config.exception_template

        try:
            message = message.format(**ready_dict)
        except KeyError as ex:
            message = await self.__iternal_error_message(
                ex, "Bot.message.exception", "While formatting exception message")
            self.__logger.log("ERROR", f'Internal error: {ex.__repr__()} in Bot.message.exception')

        tasks: list[asyncio.Task] = []
        for user in self.__database.get_users_with_perm(['GetNotifyExceptions']):
            try:
                file_data = json.dumps(parsed_ex, indent=4).encode('utf-8') if pin_full_log else None


                async def __send(
                    self: MessagesModule, user: Any, message: bytes, file_data: None | BytesIO = None
                ) -> types.Message:
                    msg = await self.__bot.send_message(
                        chat_id=user.id,
                        text=message,
                    )
                    if file_data:
                        await self.__bot.send_document(
                            chat_id=msg.chat.id,
                            document=types.BufferedInputFile(file_data, filename="exception_data.json"),
                            reply_to_message_id=msg.message_id,
                            disable_notification=True
                        )
                    return msg


                tasks += [self.__loop.create_task(__send(self, user, message, file_data))]
            except Exception as e:
                self.__logger.log("ERROR", f"Fail while sending message to {user.id}: {e}")

        for i in tasks:
            i.add_done_callback(lambda x: self.__logger.log("TRACE", f"Message sent to {x.result().chat.id}"))

        self.__logger.log("TRACE", "End of broadcast")

    async def __iternal_error_message(self, ex: BaseException, where: str, _while: str) -> str:
        return f"""
*! Internal error:* `{ex.__repr__()}`
*? Catched in:* `{where}`
*? While:* `{_while}`
"""
