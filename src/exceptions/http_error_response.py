class HttpErrorResponse(Exception):
    def __init__(self, code=None, name=None, message=None):
        super.__init__()
        if code is not None:
            self.code = code
        self.name = name
        self.message = message

    def to_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "message": self.message
        }

class BadRequestParameters(HttpErrorResponse):
    def __init__(self, message=None, code=400, name="BAD_REQUEST_PARAMETERS"):
        self.code = code
        self.message = message
        self.name = name
        super(HttpErrorResponse, self).__init__(self, code, name, message)

class ResourceNotFound(HttpErrorResponse):
    def __init__(self, message=None, code=404, name="RESOURCE_NOT_FOUND"):
        self.code = code
        self.message = message
        self.name = name
        super(HttpErrorResponse, self).__init__(self, code, name, message)

class InternalServerError(HttpErrorResponse):
    def __init__(self, message=None, code=500, name="INTERNAL_SERVER_ERROR"):
        self.code = code
        self.message = message
        self.name = name
        super(HttpErrorResponse, self).__init__(self, code, name, message)
