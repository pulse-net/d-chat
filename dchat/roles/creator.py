"""
The one who creates a chat or is in charge of a chat
if the original creator drops off from the network.
A creator listens for new incoming requests from
other nodes, updates and broadcasts ledger, listens
for and forwards messages to all other nodes.
"""
import socket
from typing import Optional, List

from .role import Role
from ..utils import constants
from ..ledger.ledger import Ledger


class Creator(Role):
    """
    Represents a creator/in-charge node of a chat.
    """
    def __init__(self) -> None:
        super().__init__()

        self.__server: Optional[socket.socket] = None
        self.__client_list = []
        self.__clients: Ledger = Ledger()

    def start(self) -> None:
        """
        Starts the creator role.
        """
        self.__server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((constants.HOST, constants.PORT))
        self.__server.listen()

    @property
    def server(self) -> socket.socket:
        """
        Returns the server socket.

        :return: socket instance of server
        """
        return self.__server

    @property
    def client_list(self) -> List[socket.socket]:
        """
        Returns the list of client sockets.

        :return: list of client sockets
        """
        return self.__client_list
