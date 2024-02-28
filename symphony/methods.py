import typing


class BaseMethod:
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return self.__class__.__name__

class Methods:
    def __init__(self) -> None:
        self.GET = GET
        self.POST = POST
        self.PUT = PUT
        self.DELETE = DELETE
        self.PATCH = PATCH
        self.OPTIONS = OPTIONS
        self.HEAD = HEAD
        self.TRACE = TRACE
        self.CONNECT = CONNECT
        self.ANY = ANY
        self.ALL = ALL
        self.WS = WS
        self.WSS = WSS
        self.Middleware = Middleware
        self.ErrorMiddleware = ErrorMiddleware
        self.Static = Static
        self.File = File
        self.Directory = Directory
        self.Redirect = Redirect
        self.View = View

    def get_method(self, method: str) -> BaseMethod:
        return getattr(self, method.upper())        

    def all_methods(self) -> typing.List[str]:
        return [method for method in self.__dict__ if not method.startswith('_')]


class GET(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class POST(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class PUT(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class DELETE(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class PATCH(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class OPTIONS(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class HEAD(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class TRACE(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class CONNECT(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class ANY(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class ALL(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class WS(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class WSS(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class Middleware(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class ErrorMiddleware(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class Static(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class File(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class Directory(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class Redirect(BaseMethod):
    def __init__(self) -> None:
        super().__init__()

class View(BaseMethod):
    def __init__(self) -> None:
        super().__init__()
