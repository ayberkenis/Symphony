import orjson

class OutgoingResponse:
    def __init__(self, data: dict, **kwargs) -> None:
        self.data = data
        self.status = kwargs.get('status', 200)
        self.headers = kwargs.get('headers', {'Content-Type': 'application/json'})
        self.body = orjson.dumps(self.data)

    def __bytes__(self) -> bytes:
        return self.build_response()

    def build_response(self) -> bytes:
        response_line = f"HTTP/1.1 {self.status} {'OK' if self.status == 200 else 'Not Found'}\r\n"
        headers = ''.join(f"{key}: {value}\r\n" for key, value in self.headers.items())
        headers += f"Content-Length: {len(self.body)}\r\n\r\n"
        return response_line.encode() + headers.encode() + self.body

