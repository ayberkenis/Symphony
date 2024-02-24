import logging
from .server import HTTPServer
from .request import IncomingRequest
from .response import OutgoingResponse
from .methods import Methods, BaseMethod



class FortunaAPI:
    def __init__(self) -> None:
        self.routes = {}
        self.middlewares = []
        self.logger = logging.getLogger('fortuna')
        self.server = None
        self.methods = Methods()
        self.queued_routes = []  # Add this line

    def __call__(self, environ, start_response):
        request = IncomingRequest(environ)
        response = self.handle_request(request)
        start_response(response.status, response.headers)
        return [response.body]

    def endpoint(self, path: str, method: BaseMethod):
        def decorator(func):
            if self.server is None:
                self.queued_routes.append((path, method, func))  # Queue the route
            else:
                self.server.add_route(path, method, func)
            return func
        return decorator

    def run(self, host: str, port: int):
        try:
            self.server = HTTPServer(host, port, self)
            for path, method, func in self.queued_routes:  # Process any queued routes
                self.server.add_route(path, method, func)
            self.queued_routes = []  # Clear the queue
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.logger.info('Server has been terminated.')
            self.server.socket.close()