import sqlite3
from typing import Any
import json

from tnotify.bot_config import DatabaseConfig

from .types import User

__all__ = ('DataBase',)

class DataBase:
    def __init__(self, logger: Any, db_config: DatabaseConfig) -> None:
        self.__config = db_config
        self.__logger = logger

        # Connect to database
        self.__connection = sqlite3.connect(self.__config.sqlite_db_path)
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

    def __exit__(self) -> None:
        self.__connection.close()
    
    def __parse_user(self, info: Any) -> User:
        user_id, permissions = info[0], json.loads(info[1])
        return User(user_id, permissions)
