import typing as t
import logging
from .db import PostgreSQL, MySQL, SQLite
import importlib.util
import sys
from colored import Fore, Style
import string
from .exceptions import FormattingNotAllowedError


class ORM:
    def __init__(
        self,
        engine: t.Union[
            t.Literal["postgres"],
            t.Literal["mysql"],
            t.Literal["sqlite"],
        ],
        username: t.Optional[str] = None,
        password: t.Optional[str] = None,
        host: t.Optional[str] = None,
        port: t.Optional[int] = None,
        database: t.Optional[str] = None,
        connection: t.Optional[t.Any] = None,
    ) -> None:
        """Database engine for the ORM.

        Args:
            engine (t.Union[ t.Literal[&#39;postgres&#39;], t.Literal[&#39;mysql&#39;], t.Literal[&#39;sqlite&#39;], ]): _description_
        """
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self._engine = engine
        self.logger = logging.getLogger("fortuna-orm")
        self._connect_string = None
        self.connection = connection

    @property
    def engine(self) -> str:
        if self._engine == "postgres":

            return PostgreSQL(
                self.host,
                self.port,
                self.username,
                self.password,
                self.database,
                self.connection,
            )
        elif self._engine == "mysql":
            return MySQL(
                self.host,
                self.port,
                self.username,
                self.password,
                self.database,
                self.connection,
            )
        return SQLite(self.database)

    def _check_installed(self, package: str) -> None:
        if importlib.util.find_spec(package) is None:
            self.logger.error(
                f"{Fore.RED}You have tried to connect to a database without having {package} installed. Install it, after you'll be able to connect.{Style.RESET}"
            )
            sys.exit(1)

    def connect(self) -> t.Any:
        """Initialize the connection to the database.

        Returns:
            t.Any: Connection object

        """

        if self._engine == "postgres":
            self._check_installed("psycopg2")
        elif self._engine == "mysql":
            self._check_installed("mysql-connector-python")
        elif self._engine == "sqlite":
            self._check_installed("sqlite3")
        elif self._engine == "cassandra":
            self._check_installed("cassandra-driver")
        self.connection = self.engine.connect()
        return self.connection

    def execute(self, query: str, *args, **kwargs) -> t.Any:
        """Execute a query.

        Args:
            query (str): The query to be executed.

        Returns:
            t.Any: The result of the query.

        """
        return self.engine.execute(query, *args, **kwargs)

    def execute_many(self, query: str, data: t.List[t.Tuple]) -> t.Any:
        """Execute a query with many data.

        Args:
            query (str): The query to be executed.
            data (t.List[t.Tuple]): The data to be inserted.

        Returns:
            t.Any: The result of the query.

        """
        return self.engine.execute_many(query, data)
