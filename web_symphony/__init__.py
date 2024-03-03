import logging

import orjson
from .server import HTTPServer
from .request import IncomingRequest
from .response import OutgoingResponse
from .methods import Methods, BaseMethod
from .reload import Reloader
from .ctx import AppContext
from .msc import Module
from .config import AppConfig
import typing as t
import sys
import os
from .utils import jsoned

sys.path.insert(0, os.getcwd())


class WebSymphony:
    def __init__(
        self, host: str = "localhost", port: int = 9000, reload: bool = False
    ) -> None:
        self.logger = logging.getLogger("fortuna")
        self.context = AppContext()
        self.host = host
        self.port = port
        self.server: HTTPServer = HTTPServer(self.host, self.port, self, self.context)
        self.methods = Methods()
        self.reloader = Reloader(self.server, reload)
        self.base_port = 29000

    def __call__(self, environ, start_response):
        request = IncomingRequest(environ)
        response = self.handle_request(request)
        start_response(response.status, response.headers)
        return [response.body]

    def endpoint(self, path: str, method: BaseMethod) -> dict:
        """This decorator is used to register a function as a route.

        Args:
            path (str): Path of the route
            method (BaseMethod): HTTP method of the route
        """

        def decorator(func):
            self.context.add_route(path, method, func)
            return func

        return decorator

    def register_module(self, module: Module):
        """This method is used to register a module to the application.

        Args:
            module (Module): Module to be registered
        """
        for rule, f, options in module.routes:
            self.context.add_route(rule, f, options)
        module._set_context(self.context)

    def before_serving(self, func):
        """Register a function to be called before serving.
        This is useful for running background tasks before the server starts serving.

        This is a decorator method.

        Args:
            func (callable): The function to be called.
        """
        self.logger.info(f"Registering before serving method: {func.__name__}")
        self.server.before_serving(func)

    def while_serving(self, func):
        """Register a function to be called while serving.
        This is useful for running background tasks while the server is running and serving.

        This is a decorator method.

        Args:
            func (callable): The function to be called.
        """

        def decorator(func):
            self.server.while_serving(func)
            return func

        return decorator

    def run(self, host: str = None, port: int = None):
        """This method is used to start the server.

        Args:
            host (str, optional): Hostname to run symphony on. Defaults to None.
            port (int, optional): Port to run symphony on. Defaults to None.
        """
        try:
            self.host = host if host else self.host
            self.port = port if port else self.port
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.logger.info("Server has been terminated.")
            self.server.socket.close()
