from fastapi import HTTPException, status
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR

class BaseHTTPError(HTTPException):
    def __init__(self, message: str = "An error occured"):
        super().__init__(status_code=self.status_code, detail=message)

class HTTPErrorNotFound(BaseHTTPError):
    def __init__(self, message: str = "Not found"):
        self.status_code = HTTP_404_NOT_FOUND
        super().__init__(message)


class HTTPLoginFailed(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Error Authorization"
        )


class HTTPUserForbidden(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="Error Forbidden"
        )

class HTTPInternalServerError(BaseHTTPError):
    def __init__(self, message: str = "Internal server error"):
        self.status_code = HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(message)

class HTTPDuplicateError(BaseHTTPError):
    def __init__(self, message: str = "Found duplicate"):
        self.status_code = HTTP_409_CONFLICT
        super().__init__(message)

class HTTPBadRequestError(BaseHTTPError):
    def __init__(self, message: str = "Bad request"):
        self.status_code = HTTP_400_BAD_REQUEST
        super().__init__(message)
