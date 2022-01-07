import socket
import threading
from typing import List, Dict

from ..ledger.ledger import Ledger
from ..ledger.ledger_entry import LedgerEntry
from .action import Action
from ..message.message import Message
from ..message.command import Command
from ..message.dtype import DType


class ListenClient(Action):
    def __init__(self) -> None:
        super(ListenClient, self).__init__()

    @staticmethod
    def __send_ledger_entry(client: socket.socket, ledger_entry: LedgerEntry) -> None:
        message = Message(Command.LEDGER_ENTRY, DType.LEDGER_IP, ledger_entry.ip_address)
        client.send(message.serialize())
        client.send("<END>".encode("utf-8"))

        message = Message(Command.LEDGER_ENTRY, DType.LEDGER_NICKNAME, ledger_entry.nick_name)
        client.send(message.serialize())
        client.send("<END>".encode("utf-8"))

        message = Message(Command.LEDGER_ENTRY, DType.LEDGER_TIMESTAMP, str(ledger_entry.timestamp))
        client.send(message.serialize())
        client.send("<END>".encode("utf-8"))

        message = Message(Command.LEDGER_ENTRY, DType.LEDGER_DADDR, ledger_entry.daddr)
        client.send(message.serialize())
        client.send("<END>".encode("utf-8"))

    def __send_ledger(self, client: socket.socket, ledger: Ledger):
        for entry in ledger.ledger:
            self.__send_ledger_entry(client=client, ledger_entry=entry)

    def __update_ledger(self, client: socket.socket, ledger_entry: LedgerEntry) -> None:
        self.__send_ledger_entry(client=client, ledger_entry=ledger_entry)

    @staticmethod
    def __listen_for_client_messages(client: socket.socket, client_list: List[socket.socket]) -> None:
        while True:
            try:
                message = client.recv(1024).decode('ascii')

                if message == "<STOP>":
                    break

                if len(message) > 0:
                    print(message)

                    for client_socket in client_list:
                        if client_socket != client:
                            client_socket.send(f"\n{message}".encode('ascii'))
            except:
                break

    def start(self) -> None:
        print("Server is listening...")

        server = self._thread_values.get('server')
        clients = self._thread_values.get('clients')
        client_list = self._thread_values.get('client_list')

        while True:
            client, address = server.accept()
            print(f'Connected with {str(address)}')

            nickname = client.recv(1024).decode()

            client_ledger = LedgerEntry(ip_address=address[0], nick_name=nickname)
            clients.add_entry(ledger_entry=client_ledger)

            print("Clients connected: ")
            print(clients)

            self.__send_ledger(client=client, ledger=clients)

            for i, client_send in enumerate(client_list):
                self.__update_ledger(client_send, client_ledger)
                print(f"Sent to: {clients[i + 1]}")

            client_list.append(client)

            listen_message_thread = threading.Thread(target=self.__listen_for_client_messages,
                                                     args=(client, client_list))
            listen_message_thread.start()
