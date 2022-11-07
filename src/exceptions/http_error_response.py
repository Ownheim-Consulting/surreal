class HttpErrorResponse(Exception):
    def __init__(self, code=None, name=None, message=None) -> None:
        super.__init__()
        self.code = code
        self.name = name
        self.message = message

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "name": self.name,
            "message": self.message
        }

class BadRequestParameters(HttpErrorResponse):
    def __init__(self, message=None) -> None:
        super(HttpErrorResponse, self).__init__(self, 400, "BAD_REQUEST_PARAMETERS", message)

class ResourceNotFound(HttpErrorResponse):
    def __init__(self, message=None) -> None:
        super(HttpErrorResponse, self).__init__(self, 404, "RESOURCE_NOT_FOUND", message)

class InternalServerError(HttpErrorResponse):
    def __init__(self, message=None) -> None:
        super(HttpErrorResponse, self).__init__(self, 500, "INTERNAL_SERVER_ERROR", message)
