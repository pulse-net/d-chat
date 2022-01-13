"""
Tokens are sent in between messages, these are generally
used for separating messages.
"""
from enum import Enum


class Token(Enum):
    """
    Enum of all possible tokens.
    """

    END: int = 0

    def __str__(self) -> str:
        """
        Returns the string representation of the token.
        :return: The string representation of the token.
        """
        return f"<{self.name}>"
