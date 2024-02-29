from .ctx import AppContext
from .methods import Methods
from .server import HTTPServer

class ForunaMeta:
    def __init__(self) -> None:
        self.context = AppContext()
        self.host: str = 'localhost'
        self.port: int = 5000
        self.base_port = 29000
        self.methods = Methods()
        self.server = HTTPServer(self.host, self.port, self, self.context)
