from .response import OutgoingResponse

class NotFoundError(OutgoingResponse):
    def __init__(self):
        super().__init__(data={"message": "Resource or endpoint not found."}, status=404)
    
class MethodNotAllowedError(OutgoingResponse):
    def __init__(self):
        super().__init__(data={"message": "Method not allowed.",}, status=405)

class ServerError(OutgoingResponse):
    def __init__(self, details: str = None):
        super().__init__(data=
                         {
                            "message": "An error occurred while processing the request.", 
                            'details': details if details else None
                          }, status=500)

