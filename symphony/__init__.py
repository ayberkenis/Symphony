import logging
from .server import HTTPServer
from .request import IncomingRequest
from .response import OutgoingResponse
from .methods import Methods, BaseMethod
from .reload import Reloader
from .ctx import AppContext
from .msc import Module
import importlib.util
import sys
import os

sys.path.insert(0, os.getcwd())

class FortunaAPI:
    def __init__(self, reload: bool =False) -> None:
        self.logger = logging.getLogger('fortuna')
        self.context = AppContext()
        self.host: str = 'localhost'
        self.port: int = 5000
        self.server: HTTPServer = HTTPServer(self.host, self.port, self, self.context)
        self.methods = Methods()
        self.reloader = Reloader(self.server, reload)
        self.base_port = 29000

    def __call__(self, environ, start_response):
        request = IncomingRequest(environ)
        response = self.handle_request(request)
        start_response(response.status, response.headers)
        return [response.body]

    def endpoint(self, path: str, method: BaseMethod):
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
            self.logger.info('Server has been terminated.')
            self.server.socket.close()
