import typing as t
from .base import SQLClass
from psycopg2 import connect, OperationalError, extensions
from psycopg2.extras import RealDictCursor
from colored import Fore, Style
import sys
import orjson


class PostgreSQL(SQLClass):
    def __init__(
        self,
        host: t.Optional[str] = None,
        port: t.Optional[int] = None,
        username: t.Optional[str] = None,
        password: t.Optional[str] = None,
        database: t.Optional[str] = None,
        connection: t.Optional[t.Any] = None,
    ) -> None:
        super().__init__(host, port, username, password, database, connection)
        self.connection = self.connect()

    def connect(self) -> t.Any:
        try:
            self.connection = connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                database=self.database,
                cursor_factory=RealDictCursor,
            )
            print(
                f"{Fore.GREEN}Connected to the database: {self.database}{Style.RESET}"
            )
            return self.connection
        except OperationalError as e:
            print(
                f"\n{Fore.RED}Are you sure that credentials you supplied to config is correct? {Style.RESET}\n\nError connecting to the database: {e}\n"
            )
            sys.exit(1)

    def execute(self, query: str) -> str:
        if not self.connection:
            raise ValueError("You need to connect to the database first.")
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        results = cursor.fetchall()
        cursor.close()
        # Serialize the list of dictionaries (rows) directly with orjson
        return orjson.dumps(results).decode("UTF-8")

    def close(self) -> None:
        self.connection.close()
        return None
