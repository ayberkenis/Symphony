import orjson

class FormData:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.form = self.parse_form()

    def parse_form(self) -> dict:
        return self.data.decode()
    
    def __repr__(self) -> str:
        return f"<FormData {self.form}>"
    
    def __str__(self) -> str:
        return f"{self.form}"
    
    