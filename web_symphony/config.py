from .ctx import AppContext


class AppConfig(dict):
    def __init__(self, context: AppContext) -> None:
        self.context = context
        self.config = {}

    def add(self, key: str, value) -> None:
        self.config[key] = value

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
