import socket
from typing import Optional, Dict

import constants
from role import Role


class Joiner(Role):
    def __init__(self) -> None:
        super().__init__()

        self.__client: Optional[socket.socket] = None
        self.__joiner_values: Dict = {}

    def register_values(self, **kwargs):
        self.__joiner_values = kwargs

    def start(self) -> None:
        server_ip = self.__joiner_values.get('server_ip')
        nickname = self.__joiner_values.get('nickname')

        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((server_ip, constants.PORT))

        self.__client.send(nickname.encode())

    @property
    def client(self) -> socket.socket:
        return self.__client



