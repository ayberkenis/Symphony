from .response import OutgoingResponse


class InternalServerError(Exception):
    def __init__(self, message):
        self.message = message


class NotFoundError(OutgoingResponse):
    def __init__(self):
        super().__init__(
            data={"message": "Resource or endpoint not found."}, status=404
        )


class MethodNotAllowedError(OutgoingResponse):
    def __init__(self):
        super().__init__(
            data={
                "message": "Method not allowed.",
            },
            status=405,
        )


class ServerError(OutgoingResponse):
    def __init__(self, details: str = None):
        super().__init__(
            data={
                "message": "Internal Server Error.",
                "details": "An error occurred while processing the request. Please try again later.",
            },
            status=500,
        )


class FormattingNotAllowedError(InternalServerError):
    def __init__(self, message: str = None):
        super().__init__(
            message if message else "Formatting is not allowed in the query string."
        )
