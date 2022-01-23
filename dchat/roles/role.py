"""
Representation of a role that can be assigned to a node
in the P2P network. Each role can perform multiple actions,
all of these actions have to be run in an infinite loop in their
own thread.
"""
import socket
from typing import List, Dict, Optional
from abc import abstractmethod
import threading

from dchat.actions.action import Action


class Role:
    """
    Represents of a role that can be assigned to a node.
    """

    def __init__(self) -> None:
        self.__actions: List[Action] = []
        self._joiner_values: Dict = {}

    @abstractmethod
    def start(self) -> None:
        """
        Starts the role.
        """

    def start_threads(self) -> None:
        """
        Starts all the actions of the role.
        """
        threads: List[threading.Thread] = []
        for action in self.__actions:
            thread = threading.Thread(target=action.start)
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def hook_action(self, action: Action) -> None:
        """
        Hooks an action to the role.
        :param action: The action to hook.
        """
        self.__actions.append(action)

    def register_values(self, **kwargs):
        """
        Registers values to be used by the role.
        :param kwargs: The values to register.
        """
        self._joiner_values = kwargs

    @property
    @abstractmethod
    def server(self) -> Optional[socket.socket]:
        """
        The server instance
        :return: The server instance
        """

    @property
    @abstractmethod
    def client_list(self) -> Optional[List[socket.socket]]:
        """
        The list of clients
        :return: The list of clients
        """

    @property
    @abstractmethod
    def client(self) -> Optional[socket.socket]:
        """
        The client instance
        :return: The client instance
        """

    @property
    def actions(self) -> List[Action]:
        """
        The actions of the role.
        :return: The actions of the role.
        """
        return self.__actions

    @property
    def role_type(self) -> str:
        """
        The type of the role.
        :return: The type of the role.
        """
        return self.__class__.__name__
