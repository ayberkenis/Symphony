from typing import Any
import logging
from .methods import Methods
from .orm import ORM
from .config import AppConfig


class AppContext:
    def __init__(self) -> None:
        self.logger = logging.getLogger("fortuna")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        self.microservices = set()
        self.routes = {}
        self.middlewares = []
        self.error_middlewares = []
        self.static_files = {}
        self.websocket_routes = {}
        self.websocket_middlewares = []
        self.methods = Methods()
        self.config = AppConfig()

    @property
    def database(self) -> ORM:
        engine = self.config.get("engine")
        username = self.config.get("username")
        password = self.config.get("password")
        host = self.config.get("host")
        port = self.config.get("port")
        database = self.config.get("database")

        return ORM(engine, username, password, host, port, database)

    def add_microservice(self, name: str, microservice: Any) -> None:
        self.microservices.add(microservice)
        self.logger.info(f"- Added microservice {name}")

    def add_route(self, path: str, method, handler: callable) -> None:
        self.routes[(path, method)] = handler
        self.logger.info(f"- Added route {path}")

    def add_middleware(self, middleware: Any) -> None:
        self.middlewares.append(middleware)

    def add_error_middleware(self, middleware: Any) -> None:
        self.error_middlewares.append(middleware)

    def add_static_file(self, path: str, file_path: str) -> None:
        self.static_files[path] = file_path

    def add_websocket_route(self, path: str, func: Any) -> None:
        self.websocket_routes[path] = func

    def add_websocket_middleware(self, middleware: Any) -> None:
        self.websocket_middlewares.append(middleware)

    def __repr__(self) -> str:
        return f"<AppContext {self.microservices} {self.routes} {self.middlewares} {self.error_middlewares} {self.static_files} {self.websocket_routes} {self.websocket_middlewares}>"

    def __str__(self) -> str:
        return f"{self.microservices} {self.routes} {self.middlewares} {self.error_middlewares} {self.static_files} {self.websocket_routes} {self.websocket_middlewares}"
