from models.http.response_model import ResponseModel

class HttpErrorResponse(Exception, ResponseModel):
    def __init__(self, code=None, name=None, message=None) -> None:
        super().__init__()
        self.code = code
        self.name = name
        self.message = message

    def __repr__(self) -> str:
        return f'HttpErrorResponse(code={self.code}, name={self.name}, message={self.message})'

    def to_dict(self) -> dict[str, any]:
        return {
            'code': self.code,
            'name': self.name,
            'message': self.message
        }

