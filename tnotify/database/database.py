import json
import sqlite3
from typing import Any

from aiogram import Bot
from aiogram.types import ChatFullInfo

from tnotify.bot_config import DatabaseConfig

from .types import User

__all__ = ('DataBase',)

class DataBase:
    def __init__(self, logger: Any, bot: Bot, db_config: DatabaseConfig) -> None:
        self.__config = db_config
        self.__logger = logger
        self.__bot = bot

        # Connect to database
        self.__connection = sqlite3.connect(self.__config.sqlite_db_path, check_same_thread=False)
        self.__cursor = self.__connection.cursor()

    def init_database(self) -> None:
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY NOT NULL,
                permissions STRING NOT NULL
            )
        """)

    def add_user(self, user_id: int, permissions: list) -> User:
        try:
            self.__logger.log('TRACE', f'Adding user {user_id}')
            self.__cursor.execute(
                """
                INSERT INTO users(id, permissions)
                VALUES(?, ?)
                """,
                (user_id, json.dumps(permissions))
            )
            self.__connection.commit()
            self.__logger.log('TRACE', f'Added user {user_id}')
        except sqlite3.IntegrityError:
            self.__logger.log('TRACE', f'User {user_id} already exists')

        self.__cursor.execute(
            """
            SELECT * FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        return self.__parse_user(self.__cursor.fetchone())

    def get_users_with_perm(self, permissions: list[str]) -> list[User]:
        self.__cursor.execute(
            f"""
            SELECT * FROM users
            WHERE {' OR '.join([f"permissions LIKE '%{i}%'"for i in permissions])}
            """
        )
        users: list[User] = []
        for unparsed_user in self.__cursor.fetchall():
            users.append(self.__parse_user(unparsed_user))

        return users

    def get_user_by_id(self, user_id: int) -> User:
        self.__cursor.execute(
            """
            SELECT * FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        return self.__parse_user(self.__cursor.fetchone())

    def get_all_users(self) -> list[User]:
        self.__cursor.execute(
            """
            SELECT * FROM users
            """
        )
        users: list[User] = []
        for unparsed_user in self.__cursor.fetchall():
            users.append(self.__parse_user(unparsed_user))

        return users

    async def get_all_tg_users(self) -> list[ChatFullInfo]:
        users = self.get_all_users()
        return [await self.__bot.get_chat(user.id) for user in users]

    def __exit__(self) -> None:
        self.__connection.close()

    def __parse_user(self, info: Any) -> User:
        user_id, permissions = info[0], json.loads(info[1])
        return User(user_id, permissions)
