from .server import HTTPServer
from .methods import Methods
from .ctx import AppContext


class Module(HTTPServer):
    def __init__(self, name, import_name, context=None, **kwargs) -> None:
        self.name = name
        self.import_name = import_name
        self.routes = []
        self.context = context
        self.methods = Methods()

    def endpoint(self, path: str, method: Methods):
        def decorator(func):
            self.routes.append((path, method, func))
            return func

        return decorator

    def _set_context(self, context: AppContext):
        """This method is used to set the context of the module, it is called by the WebSymphony class.
        It should not be called manually.

        You can use the context to access the database, cache, and other resources. So, it is important not to set manually.
        All modules are automatically set by the WebSymphony class to share the same context.

        Args:
            context (AppContext): _description_

        Returns:
            _type_: _description_
        """
        self.context = context
        return self
