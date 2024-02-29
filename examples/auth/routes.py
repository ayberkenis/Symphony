from web_symphony import Module

server = Module('auth', __name__)

@server.endpoint('/auth', server.methods.GET)
def auth(request):
    return {'message': 'This is auth endpoint in microservice.'}

