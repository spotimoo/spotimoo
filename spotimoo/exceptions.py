class IncorrectRequest(Exception):
    """Raises when we got request error."""

    def __init__(self, status_code: int) -> None:
        super().__init__(f"Incorrect request: {status_code}")
        self.status_code = status_code
