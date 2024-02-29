import typing as t
from .base import SQLClass
from psycopg2 import connect, OperationalError
from colored import Fore, Style
import sys


class PostgreSQL(SQLClass):
    def __init__(
        self,
        host: t.Optional[str] = None,
        port: t.Optional[int] = None,
        username: t.Optional[str] = None,
        password: t.Optional[str] = None,
        database: t.Optional[str] = None,
    ) -> None:
        super().__init__(host, port, username, password, database)

    def connect(self) -> t.Any:
        try:
            return connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                database=self.database,
            )
        except OperationalError as e:
            print(
                f"\n{Fore.RED}Are you sure that credentials you supplied to config is correct? {Style.RESET}\n\nError connecting to the database: {e}\n"
            )
            sys.exit(1)
        finally:
            print(
                f"{Fore.GREEN}Connected to the database: {self.database}{Style.RESET}"
            )

    def execute(self, query: str) -> t.Any:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return cursor.fetchall()

    def close(self) -> None:
        conn = self.connect()
        conn.close()
        return None
