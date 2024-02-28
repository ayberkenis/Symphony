### Fortuna HTTP

#### This is the HTTP Rest API Server for Fortuna

This has been developed to serve HTTP request for Fortuna API. It probably will be open-sourced.

- Extremely Fast
- Minimal dependencies
- Deploy in seconds

```py
server = FortunaAPI()

@server.endpoint('/', server.methods.POST)
def index(request):
    return 'YES'

# this will return below

# {'message': 'YES'}
```

##

### Automatically Add Microservices

All folders in the current working directory are imported as routes and all routes have their own microservices.

### Deployment

It has been developed for special needs. Uvicorn ASGI will be used to deploy the App to production.
