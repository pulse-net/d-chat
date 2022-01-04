"""
Representation of a role that can be assigned to a node
in the P2P network. Each role can perform multiple actions,
all of these actions have to be run in an infinite loop in their
own thread.
"""
import socket
from typing import List, Dict
from abc import abstractmethod
import threading

from ..actions.action import Action


class Role:
    """
    Represents of a role that can be assigned to a node.
    """
    def __init__(self) -> None:
        self.__actions: List[Action] = []
        self._joiner_values: Dict = {}

    @abstractmethod
    def start(self) -> None:
        pass

    def start_threads(self) -> None:
        """
        Starts all the actions of the role.
        """
        threads = []
        for action in self.__actions:
            thread = threading.Thread(target=action.start)
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def hook_action(self, action: Action) -> None:
        """
        Hooks a new action to an existing role.

        action: Action to be hooked.
        """
        self.__actions.append(action)

    def register_values(self, **kwargs):
        self._joiner_values = kwargs

    @property
    @abstractmethod
    def server(self) -> str:
        pass

    @property
    @abstractmethod
    def client_list(self) -> List[socket.socket]:
        pass

    @property
    @abstractmethod
    def client(self) -> socket.socket:
        pass

    @property
    def actions(self) -> List[Action]:
        return self.__actions
