import sys

sys.path.insert(0, "C:\\Users\\max1ne\\fortuna-backend")
from web_symphony import WebSymphony
from v1.routes import v1
from dotenv import load_dotenv
import os

load_dotenv()

server = WebSymphony()

server.context.config.set_database(
    "postgres",
    os.environ.get("DB_USER"),
    os.environ.get("PASSWORD"),
    os.environ.get("DB_HOST"),
    5432,
    os.environ.get("DB_NAME"),
)


@server.before_serving
def before_serving():
    server.context.database.connect()


@server.endpoint("/", server.methods.GET)
def index(request):
    return {"message": "This is index endpoint."}


@server.endpoint("/about", server.methods.GET)
def about(request):
    users = server.context.database.execute("SELECT * FROM users")
    return {"message": "This is about endpoint.", "path": request.path, "users": users}


server.register_module(v1)

if __name__ == "__main__":
    server.run("localhost", 5000)
