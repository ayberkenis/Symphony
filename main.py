from core import FortunaAPI

server = FortunaAPI()

@server.endpoint('/', server.methods.POST)
def index(request):
    print(request)
    return {'message': 'This is index'}


if __name__ == "__main__":
    server.run('localhost', 5000)