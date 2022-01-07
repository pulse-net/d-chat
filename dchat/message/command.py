from enum import Enum


class Command(Enum):
    LEDGER_ENTRY = 0
    MSG = 1
    END_MSG = 2
    STOP_SEND = 3