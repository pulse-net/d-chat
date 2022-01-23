"""
Listens for joinees to connect to the creator.
"""
import socket
import threading
from typing import List, Optional
import pickle

from dchat.ledger.ledger import Ledger
from dchat.ledger.ledger_entry import LedgerEntry
from dchat.actions.action import Action
from dchat.message.message import Message
from dchat.message.command import Command
from dchat.message.dtype import DType
from dchat.utils import constants
from dchat.utils import encode


class ListenClient(Action):
    """
    Listens for new joinees to be connected to the creator,
    and also listens for messages from the joinees.
    """

    @staticmethod
    def __send_ledger_entry(client: socket.socket, ledger_entry: LedgerEntry) -> None:
        encode.send_msg_with_end_token(
            cmd=Command.LEDGER_ENTRY,
            dtype=DType.LEDGER_IP,
            msg=ledger_entry.ip_address,
            client=client,
        )

        encode.send_msg_with_end_token(
            cmd=Command.LEDGER_ENTRY,
            dtype=DType.LEDGER_NICKNAME,
            msg=ledger_entry.nick_name,
            client=client,
        )

        encode.send_msg_with_end_token(
            cmd=Command.LEDGER_ENTRY,
            dtype=DType.LEDGER_TIMESTAMP,
            msg=str(ledger_entry.timestamp),
            client=client,
        )

        encode.send_msg_with_end_token(
            cmd=Command.LEDGER_ENTRY,
            dtype=DType.LEDGER_DADDR,
            msg=ledger_entry.daddr,
            client=client,
        )

    def __send_ledger(self, client: socket.socket, ledger: Ledger) -> None:
        for entry in ledger.ledger:
            self.__send_ledger_entry(client=client, ledger_entry=entry)

        message: Message = Message(Command.STOP_SEND, DType.NONE, "")
        client.send(message.serialize())

    def __update_ledger(self, client: socket.socket, ledger_entry: LedgerEntry) -> None:
        self.__send_ledger_entry(client=client, ledger_entry=ledger_entry)

    @staticmethod
    def __listen_for_client_messages(
            client: socket.socket, client_list: List[socket.socket]
    ) -> None:
        is_message_remaining: bool = False
        current_message: bytes = b""
        msg_len: int = 0
        message_obj: Optional[Message] = None

        client_list = [
            client_ledger for client_ledger in client_list if client_ledger != client
        ]

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

                        for client_socket in client_list:
                            encode.send_msg_with_end_token(
                                cmd=Command.MSG,
                                dtype=DType.MSG,
                                msg=message_obj.msg,
                                client=client_socket,
                            )
                    message_obj = None

    def start(self) -> None:
        """
        Starts the creator, accepts connections and starts listening for messages.
        """
        print("Server is listening...")

        server: Optional[socket.socket] = self._thread_values.get("server")
        clients: Optional[Ledger] = self._thread_values.get("clients")
        client_list: Optional[List[socket.socket]] = self._thread_values.get(
            "client_list"
        )

        assert server is not None
        assert clients is not None
        assert client_list is not None

        while True:
            client, address = server.accept()
            print(f"Connected with {str(address)}")

            nickname: str = client.recv(1024).decode()

            client_ledger: LedgerEntry = LedgerEntry(
                ip_address=address[0], nick_name=nickname
            )
            clients.add_entry(ledger_entry=client_ledger)

            print("Clients connected: ")
            print(clients)

            self.__send_ledger(client=client, ledger=clients)

            for i, client_send in enumerate(client_list):
                self.__update_ledger(client_send, client_ledger)
                print(f"Sent to: {clients[i + 1]}")

            client_list.append(client)

            listen_message_thread = threading.Thread(
                target=self.__listen_for_client_messages, args=(client, client_list)
            )
            listen_message_thread.start()
