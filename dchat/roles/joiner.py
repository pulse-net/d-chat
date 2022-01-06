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
        timestamps = []
        daddrs = []
        while True:
            try:
                ledger_info = self.__client.recv(1024)
                ledger_info = [val for val in ledger_info.decode('ascii').split('<END>') if len(val) > 0]

                for val in ledger_info:
                    if re.match(r"\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b", val):
                        ips.append(val)
                    elif re.match(r"\d+\.\d+", val):
                        timestamps.append(val)
                    elif re.match(r"[0-9a-fA-F]+", val) and len(val) == 10:
                        daddrs.append(val)
                    elif val != "<STOP>":
                        nicknames.append(val)

                if "<STOP>" in ledger_info:
                    break
            except:
                break

        for ip, nick_name, timestamp, daddr in zip(ips, nicknames, timestamps, daddrs):
            clients.add_entry(LedgerEntry(ip_address=ip, nick_name=nick_name, timestamp=timestamp, daddr=daddr))

    @property
    def client(self) -> socket.socket:
        return self.__client



