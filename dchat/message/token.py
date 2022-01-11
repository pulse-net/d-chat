from enum import Enum


class Token(Enum):
    END = 0

    def __str__(self) -> str:
        return f"<{self.name}>"