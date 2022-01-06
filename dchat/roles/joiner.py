import socket
from typing import Optional, Dict
import re

from ..utils import constants
from .role import Role
from ..ledger.ledger_entry import LedgerEntry


class Joiner(Role):
    def __init__(self) -> None:
        super().__init__()

        self.__client: Optional[socket.socket] = None

    def start(self) -> None:
        server_ip = self._joiner_values.get('server_ip')
        nickname = self._joiner_values.get('nickname')
        clients = self._joiner_values.get('clients')

        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((server_ip, constants.PORT))

        self.__client.send(nickname.encode())

        ips = []
        nicknames = []
        while True:
            try:
                ip_nickname = self.__client.recv(1024)
                ip_nickname = [val for val in ip_nickname.decode('ascii').split('<END>') if len(val) > 0]

                for val in ip_nickname:
                    if re.match(r"\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b", val):
                        ips.append(val)
                    elif val != "<STOP>":
                        nicknames.append(val)

                if "<STOP>" in ip_nickname:
                    break
            except:
                break

        for ip, nick_name in zip(ips, nicknames):
            clients.add_entry(LedgerEntry(ip_address=ip, nick_name=nick_name))

    @property
    def client(self) -> socket.socket:
        return self.__client



