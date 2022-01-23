"""
Listen for messages from joiner nodes.
"""
import pickle
import socket
from typing import Optional, List

from dchat.actions.action import Action
from dchat.ledger.ledger import Ledger
from dchat.ledger.ledger_entry import LedgerEntry
from dchat.utils import constants
from dchat.message.command import Command
from dchat.message.dtype import DType
from dchat.message.message import Message


class ListenJoinerMsgs(Action):
    """
    Listens for messages from joiner nodes,
    a message can either be a ledger update
    (in which case, the ledger will be updated)
    or an actual message (in which case it will
    be displayed to STDOUT).
    """

    @staticmethod
    def __classify_message(message: Message, ledger_values: List[str]) -> None:
        if message.dtype == DType.LEDGER_IP:
            ledger_values[0] = message.msg
        elif message.dtype == DType.LEDGER_NICKNAME:
            ledger_values[1] = message.msg
        elif message.dtype == DType.LEDGER_TIMESTAMP:
            ledger_values[2] = message.msg
        elif message.dtype == DType.LEDGER_DADDR:
            ledger_values[3] = message.msg

    def start(self) -> None:
        """
        Start listening for messages infinitely in a separate thread.
        """
        client: Optional[socket.socket] = self._thread_values.get("client")
        clients: Optional[Ledger] = self._thread_values.get("clients")

        assert client is not None
        assert clients is not None

        ledger_values: List[str] = ["" for _ in range(4)]
        is_message_remaining: bool = False
        current_message: bytes = b""
        msg_len: int = 0
        message_obj: Optional[Message] = None

        while True:
            message: bytes = client.recv(1024)
            messages: List[bytes] = message.split(b"<END>")

            for message in messages:
                if len(message) == 0:
                    continue

                if not is_message_remaining:
                    msg_len = int(message[: constants.MSG_HEADER_LENGTH])
                    remaining_message: bytes = message[constants.MSG_HEADER_LENGTH:]

                    if len(remaining_message) == msg_len:
                        message_obj = pickle.loads(remaining_message)
                        current_message = b""
                    else:
                        current_message += remaining_message
                        is_message_remaining = True
                else:
                    current_message += message
                    is_message_remaining = False

                    if len(current_message) == msg_len:
                        message_obj = pickle.loads(current_message)
                        current_message = b""

                if message_obj:
                    if message_obj.cmd == Command.MSG:
                        print(message_obj.msg)
                    elif message_obj.cmd == Command.LEDGER_ENTRY:
                        self.__classify_message(
                            message=message_obj, ledger_values=ledger_values
                        )

                        if all(ledger_values):
                            clients.add_entry(
                                LedgerEntry(
                                    ip_address=ledger_values[0],
                                    nick_name=ledger_values[1],
                                    timestamp=ledger_values[2],
                                    daddr=ledger_values[3],
                                )
                            )
                            print("Ledger updated: ")
                            print(clients)

                            ledger_values = ["" for _ in range(4)]
                    message_obj = None
