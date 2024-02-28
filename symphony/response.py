import orjson
from colored import Fore, Style

class OutgoingResponse:
    def __init__(self, data: dict, **kwargs) -> None:
        self.data = data
        self.status = kwargs.get('status', 200)
        self.headers = kwargs.get('headers', {'Content-Type': 'application/json', 'Connection': 'close'})
        self.headers['server'] = 'Fortuna'

    @property
    def body(self) -> bytes:
        # Updated serialization logic to handle various data types more robustly
        try:
            # Attempt to directly serialize known serializable types
            if isinstance(self.data, (bytes, str, dict)):
                print(f"{Fore.RED}An object in your response has been directly serialized, this might make your code unsafe. To change this behaviour, set `SERIALIZATION='manual'` :{Style.RESET} \n {Fore.GREEN}{self.data}{Style.RESET}\n\n")
                return orjson.dumps(self.data if isinstance(self.data, dict) else self.data.encode() if isinstance(self.data, str) else self.data)
            else:
                # For objects or other data types, use a custom serialization approach
                return orjson.dumps(self.object_to_dict(self.data))
        except TypeError:
            # Fallback serialization if direct serialization fails
            return orjson.dumps(str(self.data))

    def object_to_dict(self, obj) -> dict:
        """
        Custom method to convert objects to a dictionary by iterating over
        their attributes and handling non-serializable attributes.
        """
        
        if hasattr(obj, '__dict__'):
            return {key: self.object_to_dict(value) if hasattr(value, '__dict__') or isinstance(value, list) else value for key, value in obj.__dict__.items()}
        elif isinstance(obj, list):
            return [self.object_to_dict(item) if hasattr(item, '__dict__') or isinstance(item, list) else item for item in obj]
        else:
            return obj

    def __bytes__(self) -> bytes:
        return self.build_response()

    def build_response(self) -> bytes:
        response_line = f"HTTP/1.1 {self.status} {'OK' if self.status == 200 else 'Not Found'}\r\n"
        headers = ''.join(f"{key}: {value}\r\n" for key, value in self.headers.items())
        headers += f"Content-Length: {len(self.body)}\r\n\r\n"
        return response_line.encode() + headers.encode() + self.body

