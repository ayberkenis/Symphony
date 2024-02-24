from typing import Any


class IncomingRequest:
    def __init__(self, request: str) -> None:
        self.method, self.path, self._ = request.split(' ', 2)
        self.headers = {}
        self.body = ''
        self.parse_headers(request)
        self.parse_body(request)

    def parse_headers(self, request: str) -> None:
        headers, self.body = request.split('\r\n\r\n', 1)
        for header in headers.split('\r\n')[1:]:
            key, value = header.split(': ', 1)
            self.headers[key] = value
    
    def parse_body(self, request: str) -> None:
        if 'Content-Length' in self.headers:
            length = int(self.headers['Content-Length'])
            self.body = self.body[:length]
        
    def __repr__(self) -> str:
        return f"<IncomingRequest {self.method} {self.path} {self.headers}>"
    
    def __str__(self) -> str:
        return f"{self.method} {self.path} {self.headers}"
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self