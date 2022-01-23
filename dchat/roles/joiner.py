"""
A joiner is a role for the node which joins an
existing network via a creator. The joiner
sends messages to creator who broadcasts
it to all other joiners.
"""
import socket
from typing import Optional, List
import pickle

from dchat.roles.role import Role
from dchat.ledger.ledger import Ledger
from dchat.ledger.ledger_entry import LedgerEntry
from dchat.utils import constants
from dchat.message.dtype import DType
from dchat.message.command import Command
from dchat.message.message import Message


class Joiner(Role):
    """
    Represents a joiner node of a chat.
    """

    def __init__(self) -> None:
        super().__init__()

        self.__client: Optional[socket.socket] = None

    @property
    def server(self) -> Optional[socket.socket]:
        """
        Returns the server instance.
        :return: The server instance.
        """
        return None

    @property
    def client_list(self) -> Optional[List[socket.socket]]:
        """
        Returns the client list.
        :return: The client list.
        """
        return None

    def start(self) -> None:
        """
        Starts the joiner.
        """
        server_ip: Optional[str] = self._joiner_values.get("server_ip")
        nickname: Optional[str] = self._joiner_values.get("nickname")
        clients: Optional[Ledger] = self._joiner_values.get("clients")

        assert server_ip is not None
        assert nickname is not None
        assert clients is not None

        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((server_ip, constants.PORT))

        self.__client.send(nickname.encode())

        ips: List[str] = []
        nicknames: List[str] = []
        timestamps: List[str] = []
        daddrs: List[str] = []

        current_message: bytes = b""
        msg_len: int = 0
        message: Optional[Message] = None
        is_message_remaining: bool = False
        break_loop: bool = False
        while not break_loop:
            ledger_info: bytes = self.__client.recv(1024)
            ledger_info_split: List[bytes] = ledger_info.split(b"<END>")

            for ledger_info_val in ledger_info_split:
                if len(ledger_info_val) == 0:
                    continue

                if not is_message_remaining:
                    msg_len = int(ledger_info_val[: constants.MSG_HEADER_LENGTH])
                    remaining_message = ledger_info_val[constants.MSG_HEADER_LENGTH :]

                    if len(remaining_message) == msg_len:
                        message = pickle.loads(remaining_message)
                        current_message = b""
                    else:
                        current_message += remaining_message
                        is_message_remaining = True
                else:
                    current_message += ledger_info_val
                    is_message_remaining = False

                    if len(current_message) == msg_len:
                        message = pickle.loads(current_message)
                        current_message = b""

                if message is not None:
                    if message.cmd == Command.STOP_SEND:
                        break_loop = True
                        break

                    if message.dtype == DType.LEDGER_IP:
                        ips.append(message.msg)
                    elif message.dtype == DType.LEDGER_NICKNAME:
                        nicknames.append(message.msg)
                    elif message.dtype == DType.LEDGER_TIMESTAMP:
                        timestamps.append(message.msg)
                    elif message.dtype == DType.LEDGER_DADDR:
                        daddrs.append(message.msg)

                    message = None

        for ip_addr, nick_name, timestamp, daddr in zip(
            ips, nicknames, timestamps, daddrs
        ):
            clients.add_entry(
                LedgerEntry(
                    ip_address=ip_addr,
                    nick_name=nick_name,
                    timestamp=timestamp,
                    daddr=daddr,
                )
            )

    @property
    def client(self) -> Optional[socket.socket]:
        """
        Returns the client instance.
        :return: The client instance.
        """
        return self.__client
