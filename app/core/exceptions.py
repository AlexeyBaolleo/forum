class AppException(Exception):
    def __init__(
        self,
        detail: str,
        status_code: int = 400,
        error_code: str = "APP_ERROR",
    ) -> None:
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code

class LevelNotFoundException(AppException):
    def __init__(self, detail: str = "Level not found. Check your request") -> None:
        super().__init__(
            detail=detail,
        )