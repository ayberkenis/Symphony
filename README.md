### Fortuna HTTP

#### This is the HTTP Rest API Server for Fortuna

This has been developed to serve HTTP request for Fortuna API. It probably will be open-sourced.

- Extremely Fast
- Minimal dependencies

```py

server = FortunaAPI()

@server.endpoint('/', server.methods.POST)
def index(request):
    return 'YES'

# this will return below

# {'message': 'YES'}

```
