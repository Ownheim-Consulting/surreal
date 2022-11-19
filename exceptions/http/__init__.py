from models.http.http_error_response import HttpErrorResponse

class BadRequestParameters(HttpErrorResponse):
    def __init__(self, message=None, name='BAD_REQUEST_PARAMETERS') -> None:
        super().__init__(400, name, message)

class ResourceNotFound(HttpErrorResponse):
    def __init__(self, message=None, name='RESOURCE_NOT_FOUND') -> None:
        super().__init__(404, name, message)

class InternalServerError(HttpErrorResponse):
    def __init__(self, message=None, name='INTERNAL_SERVER_ERROR') -> None:
        super().__init__(500, name, message)
