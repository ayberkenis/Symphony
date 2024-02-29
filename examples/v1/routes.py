from web_symphony import Module

v1 = Module('v1', __name__)

@v1.endpoint('/mvc', v1.methods.GET)
def index(request):

    return {'message': 'This is MVC module endpoint.', 'path': request}


