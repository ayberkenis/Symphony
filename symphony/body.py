import orjson
import typing

class JSONBody:
    def __init__(self, body: str) -> None:
        self.body = body
        self.data = self.parse_body()
        print(self.data)

    def parse_body(self) -> dict:
        return orjson.loads(self.body)
    
    def __repr__(self) -> str:
        return f"<JSONBody {self.data}>"
    
    def __str__(self) -> str:
        return f"{self.data}"
    
    def __call__(self) -> dict:
        return self.data
    
    def __dict__(self) -> dict:
        return self.data
    
    def get(self, key: str, default: typing.Any = None) -> typing.Any:
        return self.data.get(key, default)
    
    def values(self) -> list:
        return list(self.data.values())
    
    def keys(self) -> list:
        return list(self.data.keys())
    
    def items(self) -> list:
        return list(self.data.items())
    