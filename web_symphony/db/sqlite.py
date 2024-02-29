import typing as t


class SQLite:
    def __init__(
        self,
        database: t.Optional[str] = None,
    ) -> None:
        self.database = database

    def connect(self) -> t.Any:
        pass

    def execute(self, query: str) -> t.Any:
        pass
