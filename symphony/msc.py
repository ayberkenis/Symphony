import logging
import multiprocessing
from .server import HTTPServer
from .ctx import AppContext
from .methods import Methods

class Module(HTTPServer):
    def __init__(self, name, import_name, **kwargs) -> None:
        self.name = name
        self.import_name = import_name
        self.routes = []
        self.methods = Methods()

    def endpoint(self, path: str, method: Methods):
        def decorator(func):
            self.routes.append((path, method, func))
            return func
        return decorator