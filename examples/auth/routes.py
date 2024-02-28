from symphony import FortunaAPI

server = FortunaAPI()

@server.endpoint('/auth', server.methods.GET)
def auth(request):
    return {'message': 'This is auth endpoint in microservice.'}

