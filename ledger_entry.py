import socket


class LedgerEntry:
    def __init__(self, ip_address: str, nick_name: str) -> None:
        self.__ip_address = ip_address
        self.__nick_name = nick_name

    @property
    def ip_address(self) -> str:
        return self.__ip_address

    @property
    def nick_name(self) -> str:
        return self.__nick_name

    def __str__(self) -> str:
        return f"{self.__ip_address}: {self.__nick_name}"

    def __eq__(self, other: 'LedgerEntry') -> bool:
        return self.__ip_address == other.ip_address