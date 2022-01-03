from abc import abstractmethod
import socket
from typing import List

from ledger import Ledger


class Action:
    @abstractmethod
    def start(self, server: socket.socket, clients: Ledger, client_list: List[socket.socket]) -> None:
        pass
