from typing import Callable

from aiogram import Bot, Dispatcher
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from tnotify.database import DataBase
from tnotify.database.types import User

__all__ = ('AdminPanel',)


class AdminPanel:
    def __init__(self) -> None:
        self.__dispatcher: Dispatcher | None = None
        self.__bot: Bot | None = None
        self.__logger: Callable | None = None
        self.__database: DataBase | None = None

        self.__inited = False

    def setup(self, dispatcher: Dispatcher, bot: Bot, logger: Callable, database: DataBase) -> None:
        self.__dispatcher = dispatcher
        self.__bot = bot
        self.__logger = logger
        self.__database = database

        self.__inited = True

        self.__dispatcher.callback_query.register(self._callback, lambda x: x.data.endswith('admin_btn'), flags={'self': self})

    async def __call__(self, message: Message) -> None:
        user = self.__database.get_user_by_id(message.from_user.id)
        self.__logger.log('TRACE', f'AdminPanel called by user {message.from_user.full_name} ({message.from_user.id})')

        if user and 'AdminPanel' in user.permissions:
            self.__logger.log('INFO', f'{message.from_user.full_name} ({message.from_user.id}) use AdminPanel')
            await self.admin_panel_render(message, user)

        else:
            self.__logger.log(
                'INFO',
                f'{message.from_user.full_name} ({message.from_user.id}) tryed to call AdminPanel! Permission denied.'
            )
            await self.__bot.send_message(message.from_user.id, 'You have no access to this command!')


    async def admin_panel_render(self, message: Message, user: User) -> None:
        change_permission_btn = InlineKeyboardButton(text='Change user permissions',
                                                     callback_data='change_permission_admin_btn')
        add_user_btn = InlineKeyboardButton(text='Add user', callback_data='add_user_admin_btn')
        remove_user_btn = InlineKeyboardButton(text='Remove user', callback_data='remove_user_admin_btn')
        add_admin_btn = InlineKeyboardButton(text='Add admin', callback_data='add_admin_admin_btn')
        remove_admin_btn = InlineKeyboardButton(text='Remove admin', callback_data='remove_admin_admin_btn')

        btns = [[], [], []]

        if 'AddUser'in user.permissions:
            btns[0] += [add_user_btn]
        if 'RemoveUser'in user.permissions:
            btns[0] += [remove_user_btn]
        if 'AddAdmin'in user.permissions:
            btns[1] += [add_admin_btn]
        if 'RemoveAdmin'in user.permissions:
            btns[1] += [remove_admin_btn]
        if 'ChangeUserPermissions'in user.permissions:
            btns[2] += [change_permission_btn]

        keyboard = InlineKeyboardMarkup(inline_keyboard=btns)
        await message.answer('Admin panel', reply_markup=keyboard, reply_to_message_id=message.message_id)

    def is_inited(self) -> bool:
        return self.__inited

    async def _callback(self, callback_query: CallbackQuery) -> None:
        code = callback_query.data
        # if code.isdigit():
        #     code = int(code)
        # if code == 2:
        #     await self.__bot.answer_callback_query(callback_query.id, text='Нажата вторая кнопка')
        # elif code == 'add_user_btn':
        #     await self.__bot.answer_callback_query(
        #         callback_query.id,
        #         text='Нажата кнопка с номером 5.\nА этот текст может быть длиной до 200 символов 😉', show_alert=True)
        # else:
        #     await self.__bot.answer_callback_query(callback_query.id)
        # await self.__bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')

        await ({
            'add_user_admin_btn': self.__users_admin_render,
            'remove_user_admin_btn': self.__users_admin_render
        }[code])(callback_query)


    async def __users_admin_render(self, callback_query: CallbackQuery) -> None:
        code = callback_query.data

        self.__logger.log(
            'TRACE', f'__users_admin_render by {callback_query.from_user.full_name} ({callback_query.from_user.id})')

        called_user = self.__database.get_user_by_id(callback_query.from_user.id)

        if called_user and code in called_user.permissions:

        else:
            await self.__bot.send_message(callback_query.from_user.id, 'You have no access to this command!')
