from fastapi import HTTPException, status
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

class BaseError(HTTPException):
    def __init__(self, message: str = "An error occured"):
        super().__init__(status_code=self.status_code, detail=message)

class ErrorNotFound(BaseError):
    def __init__(self, message: str = "Not found"):
        self.status_code = HTTP_404_NOT_FOUND
        super().__init__(message)


class LoginFailed(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Error Authorization"
        )


class UserForbidden(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="Error Forbidden"
        )

class DuplicateError(BaseError):
    def __init__(self, message: str = "Found duplicate"):
        self.status_code = HTTP_409_CONFLICT
        super().__init__(message)
