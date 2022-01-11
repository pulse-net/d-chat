import socket
from typing import Optional
import pickle

from dchat.roles.role import Role
from dchat.ledger.ledger_entry import LedgerEntry
from dchat.utils import constants
from dchat.message.dtype import DType
from dchat.message.command import Command


class Joiner(Role):
    def __init__(self) -> None:
        super().__init__()

        self.__client: Optional[socket.socket] = None

    def start(self) -> None:
        server_ip = self._joiner_values.get("server_ip")
        nickname = self._joiner_values.get("nickname")
        clients = self._joiner_values.get("clients")

        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((server_ip, constants.PORT))

        self.__client.send(nickname.encode())

        ips = []
        nicknames = []
        timestamps = []
        daddrs = []

        current_message = b""
        msg_len = 0
        message = None
        is_message_remaining = False
        break_loop = False
        while not break_loop:
            ledger_info = self.__client.recv(1024)
            ledger_info_split = ledger_info.split(b"<END>")

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

        for ip, nick_name, timestamp, daddr in zip(ips, nicknames, timestamps, daddrs):
            clients.add_entry(
                LedgerEntry(
                    ip_address=ip, nick_name=nick_name, timestamp=timestamp, daddr=daddr
                )
            )

    @property
    def client(self) -> socket.socket:
        return self.__client
