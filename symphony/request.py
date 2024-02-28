from typing import Any
from .methods import Methods
from .body import JSONBody

class IncomingRequest:
    def __init__(self, request: str) -> None:
        self.request = request
        self.method, self.path, self._ = request.split(' ', 2)
        self.headers = {}
        self.parse_headers(request)

    @property
    def body(self) -> JSONBody:
        return JSONBody(self.parse_body(self.request))

    def parse_headers(self, request: str) -> None:
        """Parse the headers from the request string."""
        # Split the request into headers and body parts
        parts = request.split('\r\n\r\n' if '\r\n' in request else '\n\n', 1)
        header_lines = parts[0].split('\r\n' if '\r\n' in request else '\n')[1:]  # Exclude the request line
        for line in header_lines:
            key, value = line.split(': ', 1)
            self.headers[key] = value

    
    def parse_body(self, request: str) -> None:
        """Parse the body from the request string."""
        # Split the request into headers and body parts
        parts = request.split('\r\n\r\n' if '\r\n' in request else '\n\n', 1)
        # Check if there is a body part after the headers
        if len(parts) > 1:
            return parts[1]
        
    def __repr__(self) -> str:
        return f"<IncomingRequest {self.method} {self.path} >"
    
    def __str__(self) -> str:
        return f"{self.method} {self.path} {self.headers}"
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self