import socket
import select
import logging
from .methods import BaseMethod, Methods
from .request import IncomingRequest
from .response import OutgoingResponse
from .exceptions import NotFoundError, MethodNotAllowedError, ServerError
import traceback
from colored import Fore, Back, Style
import os

class HTTPServer:
    def __init__(self, host: str, port: int, app: callable = None) -> None: 
        self.host = host
        self.port = port
        self.app = app
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger = logging.getLogger('fortuna')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        self.routes = {}


    def serve_forever(self):
        try:
            self._serve_forever()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.logger.error(f"An unexpected error occurred: {e}")
            self.socket.close()
        finally:
            print('Server has been terminated.')
            self.socket.close()


    
    def _detect_routes(self):
        """
        Detect routes from the OS.cwd(), all folders in the cwd with routes.py file are considered as routes
        """
        for root, dirs, files in os.walk(os.getcwd()):
            if 'routes.py' in files:
                self.logger.info(f"Detected routes in {root}")
                self._import_routes(os.path.join(root, 'routes.py'))
        
        print(f"{Fore.BLUE}{'_'*40}\n\nDetected routes in {len(self.routes)} files\n{self.routes.keys() if self.routes else 'No routes detected'}\n{'_'*40}{Style.RESET}\n\n")

    def _import_routes(self, path: str):
        """
        Import routes from a file
        """
        try:
            with open(path, 'r') as f:
                exec(f.read(), globals())

            
        except Exception as e:
            self.logger.error(f"Failed to import routes from {path}")
            self.logger.error(e)
            self.logger.error(traceback.format_exc())
            print(f"{Fore.RED}Failed to import routes from {path}{Style.RESET_ALL}")
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
            print(f"{Fore.RED}{traceback.format_exc()}{Style.RESET_ALL}")
            


    def _serve_forever(self):
        self._detect_routes()
        with self.socket as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(Fore.GREEN + f"Serving HTTP on {self.host} port {self.port} (http://{self.host}:{self.port}/) ..." + Style.RESET)

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
                                if isinstance(response, OutgoingResponse):
                                    client_connection.sendall(response.__bytes__())
                                elif isinstance(response, bytes):
                                    client_connection.sendall(response)
                                else:
                                    raise TypeError(f"Expected bytes or OutgoingResponse, but got {type(response)}")
                            except Exception as e:
                                print(e)
                                client_connection.sendall(ServerError(details=str(e)).__bytes__())
                except KeyboardInterrupt:
                    print("\nShutting down the server.")
                    self.logger.info("Shutting down the server.")
                    self.socket.close()
                    break  # Exit the while loop to stop the server
                        

    def _request_parser(self, request: str) -> IncomingRequest:
        return IncomingRequest(request)


    def handle_request(self, request: str) -> OutgoingResponse:
        """Handle the incoming request and return the response.

        Args:
            request (str): The raw HTTP request as a string.

        Returns:
            OutgoingResponse: The response to send back to the client.
        """
        # Parse the incoming request string into an IncomingRequest object.
        parsed_request = self._request_parser(request)
        self.logger.info(parsed_request)

        # Extract the method and path from the parsed request.
        method = parsed_request.method
        path = parsed_request.path
        self.logger.info(f"Method: {method}, Path: {path}")
        # Construct a list of potential handlers based on the path.
        potential_handlers = [(path, method) for method in Methods().all_methods()]
        self.logger.info(f"Potential handlers: {potential_handlers}")
        # Check if the path is registered under any method.
        path_registered = any(handler_key in self.routes for handler_key in potential_handlers)
        self.logger.info(f"Path registered: {path_registered}")
        # If the path is registered, proceed to check the method.
        if path_registered:
            # Construct the handler key for the specific request method.
            handler_key = (path, Methods().get_method(method))

            # If the handler for the specific method exists, proceed to handle the request.
            if handler_key in self.routes:
                handler = self.routes[handler_key]
                return self._handle_response(handler(parsed_request))
            else:
                # If the handler for the method does not exist, return a MethodNotAllowedError.
                return MethodNotAllowedError()
        else:
            # If the path is not registered under any method, return a NotFoundError.
            return NotFoundError()

    
    def _handle_response(self, response: dict) -> OutgoingResponse:
        return OutgoingResponse(data=response)

    def add_route(self, path: str, method: BaseMethod, handler: callable) -> None:
        self.routes[(path, method)] = handler
        self.logger.info(f"Added route {path} {method}")

    def add_routes(self, routes: dict) -> None:
        for path, method, handler in routes:
            self.add_route(path, method, handler)

   
