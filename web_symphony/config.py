class AppConfig(dict):
    def __init__(self) -> None:
        self.config = {}

    def add(self, key: str, value) -> None:
        self.config[key] = value

    def set(self, key: str, value) -> None:
        self.add(key, value)

    def get(self, key: str):
        return self.config.get(key)

    def remove(self, key: str) -> None:
        self.config.pop(key)

    def update(self, key: str, value) -> None:
        self.config[key] = value

    def clear(self) -> None:
        self.config.clear()

    def __getitem__(self, key: str):
        return self.get(key)

    def __setitem__(self, key: str, value) -> None:
        self.config[key] = value

    def __delitem__(self, key: str) -> None:
        self.remove(key)

    def __iter__(self):
        return iter(self.config)

    def set_database(
        self,
        engine: str,
        username: str,
        password: str,
        host: str,
        port: int,
        database: str,
    ) -> None:
        self.add("engine", engine)
        self.add("username", username)
        self.add("password", password)
        self.add("host", host)
        self.add("port", port)
        self.add("database", database)
