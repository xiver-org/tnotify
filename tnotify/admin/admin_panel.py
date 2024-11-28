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

        self.__dispatcher.callback_query.register(
            self._callback, lambda x: x.data.endswith('_btn'), flags={'self': self})

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

    async def __admin_panel_render(self, callback_query: CallbackQuery) -> None:
        self.__logger.log(
            'TRACE',
            f'__admin_panel_render by {callback_query.from_user.full_name} ({callback_query.from_user.id})'
        )
        await self.admin_panel_render(
            callback_query.message, self.__database.get_user_by_id(callback_query.from_user.id))

    def is_inited(self) -> bool:
        return self.__inited

    async def _callback(self, callback_query: CallbackQuery) -> None:
        if not await self.__check_permission_by_callback(callback_query):
            await callback_query.answer('You have no access to this command!')
            return

        code = callback_query.data

        if code.endswith('_remove_user_id_btn'):
            await self.__remove_all_user_permissions(callback_query)
            await callback_query.answer('All user permissions removed!')
            await self.__admin_panel_render(callback_query)
            return

        try:
            await ({
                'add_user_admin_btn': self.__add_users_admin_render,
                'remove_user_admin_btn': self.__remove_users_admin_render,
                'back_to_admin_panel_btn': self.__admin_panel_render,
            }[code])(callback_query)
        except KeyError:
            await self.__bot.send_message(callback_query.from_user.id, 'Unknown command!')
            self.__logger.log('TRACE', f'Unknown command: {callback_query.data}')
        await callback_query.answer()


    async def __check_permission_by_callback(self, callback_query: CallbackQuery) -> bool:
        code = callback_query.data

        code_permission = {
            'change_permission_admin_btn': 'ChangeUserPermissions',
            'add_user_admin_btn': 'AddUser',
            'remove_user_admin_btn': 'RemoveUser',
            'add_admin_admin_btn': 'AddAdmin',
            'remove_admin_admin_btn': 'RemoveAdmin'
        }

        if code.endswith('_remove_user_id_btn'):
            code = 'remove_user_admin_btn'

        called_user = self.__database.get_user_by_id(callback_query.from_user.id)

        if called_user and code_permission[code] in called_user.permissions:
            return True
        else:
            return False

    async def __remove_users_admin_render(self, callback_query: CallbackQuery) -> None:
        self.__logger.log(
            'TRACE',
            f'__remove_users_admin_render by {callback_query.from_user.full_name} ({callback_query.from_user.id})'
        )

        all_users = await self.__database.get_all_tg_users()
        msg = '*Users*\n_Choose user to remove_\n\n'


        c = 1
        ln = len(all_users)
        btns = [list() for _ in range(ln // 4 + 1)]
        for user in all_users:
            btns[c // 4] += [InlineKeyboardButton(text=f'{c}', callback_data=f'{user.id}_remove_user_id_btn')]

            msg += f'{c}) {user.first_name} {user.last_name} (@{user.username})\n'
            c += 1

        btns += [[InlineKeyboardButton(text='< Back', callback_data='back_to_admin_panel_btn')]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=btns)
        await self.__bot.send_message(callback_query.from_user.id, msg, reply_markup=keyboard)

    async def __add_users_admin_render(self, callback_query: CallbackQuery) -> None:
        self.__logger.log(
            'TRACE',
            f'__add_users_admin_render by {callback_query.from_user.full_name} ({callback_query.from_user.id})',
        )

        all_users = await self.__database.get_all_tg_users()
        msg = '*Users*\n\n'

        c = 1
        for user in all_users:
            msg += f'{c}) {user.first_name} {user.last_name} (@{user.username})\n'
            c += 1

        await self.__bot.send_message(callback_query.from_user.id, msg)

    async def __remove_all_user_permissions(self, callback_query: CallbackQuery) -> None:
        self.__database.remove_all_permissions(int(callback_query.data.split('_')[0]))
