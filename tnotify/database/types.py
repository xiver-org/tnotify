__all__ = ('User',)

class User:
    id: int
    permissions: list

    def __init__(self, id: int, permissions: list) -> None:
        self.id = id
        self.permissions = permissions
