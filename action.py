from abc import abstractmethod
import socket
from typing import List

from ledger import Ledger


class Action:
    def __init__(self):
        self._thread_values = {}

    def register_values(self, **kwargs) -> None:
        self._thread_values = kwargs

    @abstractmethod
    def start(self) -> None:
        pass
