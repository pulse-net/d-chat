from typing import List
import socket

from action import Action
from ledger import Ledger


class SendJoineeMessage(Action):
    def __init__(self) -> None:
        self.__thread_values = {}

    def register_values(self, **kwargs) -> None:
        self.__thread_values = kwargs

    def start(self) -> None:
        clients = self.__thread_values.get('clients')
        client_list = self.__thread_values.get('client_list')

        while True:
            message = input(f"{clients[0].nick_name}> ")

            for client in client_list:
                client.send(f"\n{clients[0].nick_name}> {message}".encode('ascii'))