import sqlite3

from tnotify.bot_config import DatabaseConfig

from .types import User

__all__ = ('DataBase',)

class DataBase:
    def __init__(self, db_config: DatabaseConfig) -> None:
        self.__config = db_config

        # Connect to database
        self.__connection = sqlite3.connect(self.__config.sqlite_db_path)
        self.__cursor = self.__connection.cursor()

    def init_database(self) -> None:
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY NOT NULL,
                permissions JSON NOT NULL
            )
        """)

    def add_user(self, user_id: int, permissions: list) -> User:
        self.__cursor.execute(
            """
            INSERT INTO users(id, permissions)
            VALUES(?, ?)
            """,
            (user_id, permissions)
        )
        self.__connection.commit()

        self.__cursor.execute(
            """
            SELECT * FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        user = User(*self.__cursor.fetchone())
        return user

    def __exit__(self) -> None:
        self.__connection.close()
