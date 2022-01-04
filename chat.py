import argparse
import socket
import re
import threading

from ledger import Ledger
from ledger_entry import LedgerEntry
from node import Node
from creator import Creator
from listen_clients import ListenClient
from send_joinee_msgs import SendJoineeMessage
from role import Role
from action import Action


def listen_messages(client, clients):
    is_update = False
    ip = ""
    nickname = ""
    
    while True:
        try:
            message = client.recv(1024)
            message = message.decode('ascii')

            if "<UPDATE>" in message:
                is_update = True

            message = [val for val in message.split('<END>') if len(val) > 0]

            if len(message) > 0:
                if is_update:
                    for val in message:
                        if re.match(r"\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b", val):
                            ip = val
                        elif val != "<STOP>":
                            nickname = val

                    if ip != "" and nickname != "":
                        clients.add_entry(LedgerEntry(ip_address=ip, nick_name=nickname))
                        print("Ledger updated: ")
                        print(clients)
                        is_update = False
                        ip = ""
                        nickname = ""
                else:
                    for val in message:
                        print(val)
        except:
            break


def send_message_client(client, nickname):
    while True:
        message = input(f"{nickname}> ")
        client.send(f"\n{nickname}> {message}".encode('ascii'))


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Decentralized chat")
    parser.add_argument("--create", action="store_true", default=False, help="Create a new chat")
    parser.add_argument("--join", action="store_true", default=False, help="Join an existing chat")

    args: argparse.Namespace = parser.parse_args()

    if args.create:
        nickname: str = input("Enter your nickname: ")
        server_node: Node = Node(nickname=nickname)

        print(server_node.ledger)

        listen_requests_action: Action = ListenClient()
        send_joinee_message_action: Action = SendJoineeMessage()

        creator_role: Role = Creator()
        creator_role.hook_action(action=listen_requests_action)
        creator_role.hook_action(action=send_joinee_message_action)

        server_node.hook_role(role=creator_role)
        server_node.start()
    elif args.join:
        ip = input("Enter the IP address of the chat node: ") 
        nickname = input("Enter your nickname: ")

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, 12345))

        client.send(nickname.encode())

        ips = []
        nicknames = []
        while True:
            try:
                ip_nickname = client.recv(1024)
                ip_nickname = [val for val in ip_nickname.decode('ascii').split('<END>') if len(val) > 0]                

                for val in ip_nickname:
                    if re.match(r"\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b", val):
                        ips.append(val)
                    elif val != "<STOP>":
                        nicknames.append(val)

                if "<STOP>" in ip_nickname:
                    break
            except:
                break

        clients = Ledger()
        for ip, nick_name in zip(ips, nicknames):
            clients.add_entry(LedgerEntry(ip_address=ip, nick_name=nick_name))

        print("Initial ledger: ")
        print(clients)

        listen_thread = threading.Thread(target=listen_messages, args=(client, clients))
        listen_thread.start()

        send_thread = threading.Thread(target=send_message_client, args=(client, nickname))
        send_thread.start()

        listen_thread.join()
        send_thread.join()