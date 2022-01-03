"""
Representation of a role that can be assigned to a node
in the P2P network. Each role can perform multiple actions,
all of these actions have to be run in an infinite loop in their
own thread.
"""
import socket
from typing import List, Optional
from abc import abstractmethod
import threading

from action import Action
from ledger import Ledger


class Role:
    """
    Represents of a role that can be assigned to a node.
    """
    def __init__(self) -> None:
        self.__actions: List[Action] = []

    @abstractmethod
    def start(self, clients: Ledger) -> None:
        pass

    def start_actions(self, server: socket.socket, clients: Ledger,
                      client_list: Optional[List[socket.socket]] = None) -> None:
        """
        Starts all the actions of the role.
        """
        threads = []
        for action in self.__actions:
            thread = threading.Thread(target=action.start,
                                      args=(server, clients, client_list))
            threads.append(thread)

        for thread in threads:
            thread.start()

        # for thread in threads:
        #     thread.join()

    def hook_action(self, action: Action) -> None:
        """
        Hooks a new action to an existing role.

        action: Action to be hooked.
        """
        self.__actions.append(action)