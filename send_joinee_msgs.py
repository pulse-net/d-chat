from typing import List
import socket

from action import Action
from ledger import Ledger


class SendJoineeMessage(Action):
    def start(self, server: socket.socket, clients: Ledger, client_list: List[socket.socket]) -> None:
        while True:
            message = input(f"{clients[0].nick_name}> ")

            for client in client_list:
                client.send(f"\n{clients[0].nick_name}> {message}".encode('ascii'))