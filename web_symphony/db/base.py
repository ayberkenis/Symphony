import typing as t


class SQLClass:
    def __init__(
        self,
        host: t.Optional[str] = None,
        port: t.Optional[int] = None,
        username: t.Optional[str] = None,
        password: t.Optional[str] = None,
        database: t.Optional[str] = None,
    ) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    def connect(self) -> t.Any:
        pass

    def execute(self, query: str) -> t.Any:
        pass
