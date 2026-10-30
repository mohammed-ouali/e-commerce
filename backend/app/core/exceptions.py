from fastapi import status


class DomainException(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    title = "Domain Error"
    default_message = "A domain error occurred."

    def __init__(self, message: str | None = None) -> None:
        self.message = (
            message if message is not None else self.default_message
        )
        super().__init__(self.message)