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


class Model:
    def __init__(self, table: str, columns: t.Dict[str, t.Union[str, t.Type]]) -> None:
        self.table = table
        self.columns = columns
        self.logger = logging.getLogger("fortuna-orm")

    def create(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def select(self):
        pass

    def insert(self):
        pass

    def drop(self):
        pass

    def alter(self):
        pass

    def truncate(self):
        pass

    def describe(self):
        pass

    def show(self):
        pass

    def execute(self):
        pass

    def execute_many(self):
        pass

    def execute_script(self):
        pass

    def execute_file(self):
        pass

    def execute_sql(self):
        pass

    def execute_query(self):
        pass

    def execute_queries(self):
        pass

    def execute_transaction(self):
        pass

    def execute_transactions(self):
        pass

    def execute_procedure(self):
        pass

    def execute_function(self):
        pass

    def execute_trigger(self):
        pass

    def execute_event(self):
        pass

    def execute_view(self):
        pass

    def execute_index(self):
        pass

    def execute_sequence(self):
        pass

    def execute_table(self):
        pass

    def execute_schema(self):
        pass

    def execute_database(self):
        pass

    def execute_user(self):
        pass

    def execute_role(self):
        pass

    def execute_privilege(self):
        pass

    def execute_constraint(self):
        pass

    def execute_trigger(self):
        pass

    def execute_event(self):
        pass

    def execute_view(self):
        pass

    def execute_index(self):
        pass

    def execute_sequence(self):
        pass

    def execute_table(self):
        pass

    def execute_schema(self):
        pass

    def execute_database(self):
        pass

    def execute_user(self):
        pass

    def execute_role(self):
        pass

    def execute_privilege(self):
        pass

    def execute_constraint(self):
        pass

    def execute_trigger(self):
        pass

    def execute_event(self):
        pass

    def execute_view(self):
        pass

    def execute_index(self):
        pass

    def execute_sequence(self):
        pass
