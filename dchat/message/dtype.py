"""
DType describes the part of the intent that is being
sent.
"""
from enum import Enum


class DType(Enum):
    """
    Enum for the different types of messages.
    """

    LEDGER_IP: int = 0
    LEDGER_NICKNAME: int = 1
    LEDGER_TIMESTAMP: int = 2
    LEDGER_DADDR: int = 3
    MSG: int = 4
    NONE: int = 5
