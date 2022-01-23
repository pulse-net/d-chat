"""
DType describes the part of the intent that is being
sent.
"""
from enum import Enum


class DType(Enum):
    """
    Enum for the different types of messages.
    """

    LEDGER_IP = 0
    LEDGER_NICKNAME = 1
    LEDGER_TIMESTAMP = 2
    LEDGER_DADDR = 3
    MSG = 4
    NONE = 5
