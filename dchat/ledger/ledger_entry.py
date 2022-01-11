import time
from typing import Optional

from dchat.utils import constants


class LedgerEntry:
    _current_hex_str = "0" * constants.DADDR_LENGTH

    def __init__(
        self,
        ip_address: str,
        nick_name: str,
        timestamp: Optional[str] = None,
        daddr: Optional[str] = None,
    ) -> None:
        self.__ip_address = ip_address
        self.__nick_name = nick_name
        self.__timestamp = time.time() if not timestamp else timestamp
        self.__daddr = self.__generate_next_hex() if not daddr else daddr

    @classmethod
    def __generate_next_hex(cls) -> str:
        try:
            hex_num = int(cls._current_hex_str, 16)
            hex_num += 1
            prev_hex_str = cls._current_hex_str
            cls._current_hex_str = (
                str(hex(hex_num))[2:].upper().zfill(constants.DADDR_LENGTH)
            )
            return prev_hex_str
        except ValueError as _:
            return "-1"

    @property
    def ip_address(self) -> str:
        return self.__ip_address

    @property
    def nick_name(self) -> str:
        return self.__nick_name

    @property
    def timestamp(self) -> float:
        return self.__timestamp

    @property
    def daddr(self) -> str:
        return self.__daddr

    def __str__(self) -> str:
        return f"{self.__ip_address}: {self.__nick_name} ({self.__timestamp}) -> {self.__daddr}"

    def __eq__(self, other: "LedgerEntry") -> bool:
        return (
            self.__ip_address == other.ip_address
            and self.__nick_name == other.nick_name
            and self.__timestamp == other.timestamp
            and self.__daddr == other.daddr
        )
