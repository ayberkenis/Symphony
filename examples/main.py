from symphony import FortunaAPI
from v1.routes import v1

server = FortunaAPI()

@server.endpoint('/', server.methods.GET)
def index(request):
    return {'message': 'This is index endpoint.'}

@server.endpoint('/about', server.methods.GET)
def about(request):
    return {'message': 'This is about endpoint.', 'path': request.path}


server.register_module(v1)

if __name__ == "__main__":
    server.run('localhost', 5000)