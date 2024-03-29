import typing as t
from .base import SQLClass


class MySQL(SQLClass):
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
