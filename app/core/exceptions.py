class AppException(Exception):
    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code


class InvalidInputException(AppException):

    def __init__(self, message="Invalid input"):
        super().__init__(
            message=message,
            error_code="INVALID_INPUT",
            status_code=400
        )