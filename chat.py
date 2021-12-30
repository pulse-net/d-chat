import argparse
import socket
import re
import threading

from ledger import Ledger
from ledger_entry import LedgerEntry


def send_ledger_entry(client, ledger_entry):
    client.send(ledger_entry.ip_address.encode('ascii'))
    client.send('<END>'.encode('ascii'))
    client.send(ledger_entry.nick_name.encode('ascii'))
    client.send('<END>'.encode('ascii'))


def send_ledger(client, ledger):
    for entry in ledger.ledger:
        send_ledger_entry(client=client, ledger_entry=entry)

    client.send("<STOP>".encode('ascii'))


def update_ledger(client, ledger_entry):
    client.send("<UPDATE>".encode('ascii'))

    send_ledger_entry(client=client, ledger_entry=ledger_entry)

    client.send("<STOP>".encode('ascii'))


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.connect(("8.8.8.8", 1))
    IP = s.getsockname()[0]
    s.close()

    return IP


def listen_for_requests():
    print("Server is listening...")
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        nickname = client.recv(1024).decode()

        client_ledger = LedgerEntry(ip_address=address[0], nick_name=nickname)
        clients.add_entry(ledger_entry=client_ledger)

        print("Clients connected: ")
        print(clients)

        thread = threading.Thread(target=send_ledger, args=(client, clients))
        thread.start()
        thread.join()

        for i, client_send in enumerate(client_list):
            update_ledger(client_send, client_ledger)
            print(f"Sent to: {clients[i+1]}")

        client_list.append(client)


def send_message():
    while True:
        message = input(f"{clients[0].nick_name}> ")

        for client in client_list:
            client.send(message.encode('ascii'))
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decentralized chat")
    parser.add_argument("--create", action="store_true", default=False, help="Create a new chat")
    parser.add_argument("--join", action="store_true", default=False, help="Join an existing chat")

    args = parser.parse_args()

    if args.create:
        clients = Ledger()

        nickname = input("Enter your nickname: ")

        host = '0.0.0.0'
        port = 12345

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()

        self_client = LedgerEntry(ip_address=get_ip(), nick_name=nickname)
        clients.add_entry(ledger_entry=self_client)

        client_list = []

        print(clients)

        listen_thread = threading.Thread(target=listen_for_requests)
        listen_thread.start()

        send_thread = threading.Thread(target=send_message)
        send_thread.start()

        listen_thread.join()
        send_thread.join()
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
        for ip, nickname in zip(ips, nicknames):
            clients.add_entry(LedgerEntry(ip_address=ip, nick_name=nickname))

        print("Initial ledger: ")
        print(clients)

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
            except:
                break