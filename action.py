from abc import abstractmethod
import socket
from typing import List

from ledger import Ledger


class Action:
    @abstractmethod
    def register_values(self, **kwargs) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass
