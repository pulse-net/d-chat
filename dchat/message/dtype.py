from enum import Enum


class DType(Enum):
    LEDGER_IP = 0
    LEDGER_NICKNAME = 1
    LEDGER_TIMESTAMP = 2
    LEDGER_DADDR = 3
    MSG = 4
    NONE = 5
