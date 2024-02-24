### Fortuna HTTP

#### This is the HTTP Rest API Server for Fortuna

```py

server = FortunaAPI()

@server.endpoint('/', server.methods.POST)
def index(request):
    return 'YES'

# this will return below

# {'message': 'YES'}

```
