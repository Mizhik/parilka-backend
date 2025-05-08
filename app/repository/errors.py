class DuplicateError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NotFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
