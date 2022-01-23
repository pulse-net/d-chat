"""
A single entry in the ledger.
"""
import time
from typing import Optional

from dchat.utils import constants


class LedgerEntry:
    """
    A single entry in the ledger, this contains
    information like IP address, nickname, timestamp,
    and the DAddress of the peer.
    """

    _current_hex_str: str = "0" * constants.DADDR_LENGTH

    def __init__(
        self,
        ip_address: str,
        nick_name: str,
        timestamp: Optional[str] = None,
        daddr: Optional[str] = None,
    ) -> None:
        """
        Initialize a new LedgerEntry.
        :param ip_address: The IP address of the peer.
        :param nick_name: The nickname of the peer.
        :param timestamp: The timestamp of the entry.
        :param daddr: The DAddress of the peer.
        """
        self.__ip_address: str = ip_address
        self.__nick_name: str = nick_name
        self.__timestamp: float = time.time() if not timestamp else float(timestamp)
        self.__daddr: str = self.__generate_next_hex() if not daddr else daddr

    @classmethod
    def __generate_next_hex(cls) -> str:
        try:
            hex_num: int = int(cls._current_hex_str, 16)
            hex_num += 1
            prev_hex_str: str = cls._current_hex_str
            cls._current_hex_str = (
                str(hex(hex_num))[2:].upper().zfill(constants.DADDR_LENGTH)
            )
            return prev_hex_str
        except ValueError as _:
            return "-1"

    @property
    def ip_address(self) -> str:
        """
        The IP address of the peer.
        :return: The IP address of the peer.
        """
        return self.__ip_address

    @property
    def nick_name(self) -> str:
        """
        The nickname of the peer.
        :return: The nickname of the peer.
        """
        return self.__nick_name

    @property
    def timestamp(self) -> float:
        """
        The timestamp of the entry.
        :return: The timestamp of the entry.
        """
        return self.__timestamp

    @property
    def daddr(self) -> str:
        """
        The DAddress of the peer.
        :return: The DAddress of the peer.
        """
        return self.__daddr

    def __str__(self) -> str:
        """
        Return a string representation of the LedgerEntry.
        :return: A string representation of the LedgerEntry.
        """
        return f"{self.__ip_address}: {self.__nick_name} ({self.__timestamp}) -> {self.__daddr}"

    def __eq__(self, other: object) -> bool:
        """
        Check if two LedgerEntries are equal.
        :param other: The other LedgerEntry to compare to.
        :return: True if the LedgerEntries are equal, False otherwise.
        """
        if not isinstance(other, LedgerEntry):
            return False

        return (
            self.__ip_address == other.ip_address
            and self.__nick_name == other.nick_name
            and self.__timestamp == other.timestamp
            and self.__daddr == other.daddr
        )
