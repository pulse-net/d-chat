import socket
from typing import Optional

import constants
from role import Role
from ledger import Ledger


class Joiner(Role):
    def __init__(self) -> None:
        super().__init__()

        self.__client: Optional[socket.socket] = None

    def start(self, clients: Optional[Ledger] = None, server_ip: Optional[str] = None) -> None:
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((server_ip, constants.PORT))

