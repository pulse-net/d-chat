"""
Command is the first part of the standard format of message, this
holds information about the intent of the message.
"""
from enum import Enum


class Command(Enum):
    """
    Enum of all possible commands.
    """

    LEDGER_ENTRY: int = 0
    MSG: int = 1
    STOP_SEND: int = 2
