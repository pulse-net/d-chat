import socket
import threading
from typing import List

from ledger import Ledger
from ledger_entry import LedgerEntry
from action import Action


class ListenClient(Action):
    @staticmethod
    def __send_ledger_entry(client: socket.socket, ledger_entry: LedgerEntry) -> None:
        client.send(ledger_entry.ip_address.encode('ascii'))
        client.send('<END>'.encode('ascii'))
        client.send(ledger_entry.nick_name.encode('ascii'))
        client.send('<END>'.encode('ascii'))

    def __send_ledger(self, client: socket.socket, ledger: Ledger):
        for entry in ledger.ledger:
            self.__send_ledger_entry(client=client, ledger_entry=entry)

        client.send("<STOP>".encode('ascii'))

    def __update_ledger(self, client: socket.socket, ledger_entry: LedgerEntry) -> None:
        client.send("<UPDATE>".encode('ascii'))

        self.__send_ledger_entry(client=client, ledger_entry=ledger_entry)

        client.send("<STOP>".encode('ascii'))

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

    def start(self, server: socket.socket, clients: Ledger, client_list: List[socket.socket]) -> None:
        print("Server is listening...")
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
