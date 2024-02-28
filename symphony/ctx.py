from typing import Any
import logging
from .methods import Methods

class AppContext:
    def __init__(self) -> None:
        self.logger = logging.getLogger('fortuna')
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