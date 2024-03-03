import socket
import select
import logging
from .methods import BaseMethod, Methods
from .request import IncomingRequest
from .response import OutgoingResponse
from .exceptions import NotFoundError, MethodNotAllowedError, ServerError
import traceback
from colored import Fore, Style
from typing import Union
from .ctx import AppContext
from .monitor import timer


class HTTPServer:
    def __init__(
        self, host: str, port: int, app: callable = None, context: AppContext = None
    ) -> None:
        self.host = host
        self.port = port
        self.app = app
        self.context = context
        self.logger = logging.getLogger("fortuna")
        if not self.logger.hasHandlers():
            self.logger.addHandler(logging.StreamHandler())
        self.initialize_socket()
        self.while_serving_methods = []
        self.before_serving_methods = []

    @timer
    def initialize_socket(self):
        """Initialize the server socket."""

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def serve_forever(self):
        for method in self.before_serving_methods:
            method()
        try:
            self._serve_forever()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.logger.error(f"An unexpected error occurred: {e}")
            print(traceback.format_exc())
            if self.socket:
                self.socket.close()
        finally:
            print("Server has been terminated.")
            if self.socket:
                self.socket.close()

    def while_serving(self, func: callable) -> None:
        """Register a function to be called while serving.
        This is useful for running background tasks while the server is running and serving.

        This is method is defined as a decorator in the WebSymphony class.

        Args:
            func (callable): The function to be called.

        """
        self.while_serving_methods.append(func)

    def before_serving(self, func: callable) -> None:
        """Register a function to be called before serving.
        This is useful for running background tasks before the server starts serving.

        This is method is defined as a decorator in the WebSymphony class.

        Args:
            func (callable): The function to be called.

        """
        self.before_serving_methods.append(func)

    def _serve_forever(self):
        with self.socket as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(
                Fore.GREEN
                + f"Serving HTTP on {self.host} port {self.port} (http://{self.host}:{self.port}/) ..."
                + Style.RESET
            )

            while True:
                try:
                    # Use select to wait for incoming connections with a timeout
                    ready_to_read, _, _ = select.select([server_socket], [], [], 1.0)
                    if ready_to_read:
                        client_connection, client_address = server_socket.accept()
                        with client_connection:
                            request = client_connection.recv(1024).decode()
                            response = self.handle_request(request)
                            try:
                                for method in self.while_serving_methods:
                                    method()

                                if isinstance(response, OutgoingResponse):
                                    client_connection.sendall(response.__bytes__())
                                elif isinstance(response, bytes):
                                    client_connection.sendall(response)
                                else:
                                    if response is None:
                                        pass
                                    else:
                                        raise TypeError(
                                            f"Expected bytes or OutgoingResponse, but got {type(response)}"
                                        )
                            except Exception as e:
                                print(traceback.format_exc())
                                client_connection.sendall(
                                    ServerError(details=str(e)).__bytes__()
                                )
                            finally:
                                client_connection.shutdown(socket.SHUT_WR)
                                client_connection.close()

                except KeyboardInterrupt:
                    print("\nShutting down the server.")
                    self.logger.info("Shutting down the server.")
                    self.socket.close()
                    break  # Exit the while loop to stop the server

    @timer
    def handle_request(self, request: str) -> Union[OutgoingResponse, bytes]:
        """Handle the incoming request and return the response.

        Args:
            request (str): The raw HTTP request as a string.

        Returns:
            Union[OutgoingResponse, bytes]: The response to send back to the client.
        """
        # Parse the incoming request string into an IncomingRequest object.
        if len(request) != 0:
            try:

                parsed_request = IncomingRequest(request)

            except Exception as e:
                self.logger.error(f"Error parsing request: {traceback.format_exc()}")
                return ServerError(details="Failed to parse request")

            # Extract the method and path from the parsed request.
            method = parsed_request.method
            method = Methods().get_method(method)
            path = parsed_request.path

            if (path, method) in self.context.routes:
                try:
                    handler = self.context.routes[(path, method)]
                    response_data = handler(parsed_request)
                    return OutgoingResponse(status=200, data=response_data)
                except Exception as e:
                    self.logger.error(
                        f"Error handling request: {traceback.format_exc()}"
                    )
                    return ServerError(
                        details="An error occurred while handling the request"
                    )
            else:
                # Return a NotFoundError for unregistered paths or MethodNotAllowedError if the method is not allowed.
                if any(
                    (path, m) in self.context.routes for m in Methods().all_methods()
                ):
                    return MethodNotAllowedError()
                else:
                    return NotFoundError()

    @timer
    def _handle_response(self, response: dict) -> OutgoingResponse:
        return OutgoingResponse(data=response)

    @timer
    def add_route(self, path: str, method: BaseMethod, handler: callable) -> None:
        self.context.routes[(path, method)] = handler

    def add_routes(self, routes: dict) -> None:
        for path, method, handler in routes:
            self.add_route(path, method, handler)

    def close(self) -> None:
        self.socket.close()
