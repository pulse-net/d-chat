import argparse

from dchat.node.node import Node
from dchat.roles.creator import Creator
from dchat.roles.joiner import Joiner
from dchat.roles.role import Role
from dchat.actions.listen_clients import ListenClient
from dchat.actions.send_joinee_msgs import SendJoineeMessage
from dchat.actions.listen_joiner_msgs import ListenJoinerMsgs
from dchat.actions.send_joiner_msgs import SendJoinerMsgs
from dchat.actions.action import Action


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Decentralized chat"
    )
    parser.add_argument(
        "--create", action="store_true", default=False, help="Create a new chat"
    )
    parser.add_argument(
        "--join", action="store_true", default=False, help="Join an existing chat"
    )

    args: argparse.Namespace = parser.parse_args()

    if args.create:
        nickname: str = input("Enter your nickname: ")
        server_node: Node = Node(nickname=nickname)

        listen_requests_action: Action = ListenClient()
        send_joinee_message_action: Action = SendJoineeMessage()

        creator_role: Role = Creator()
        creator_role.hook_action(action=listen_requests_action)
        creator_role.hook_action(action=send_joinee_message_action)

        server_node.hook_role(role=creator_role)
        server_node.start()

        print(server_node.ledger)

        server_node.register_action_values(
            server=creator_role.server,
            client_list=creator_role.client_list,
            clients=server_node.ledger,
        )

        server_node.start_threads()
    elif args.join:
        ip = input("Enter the IP address of the chat node: ")
        nickname = input("Enter your nickname: ")
        client_node: Node = Node(nickname=nickname)

        listen_joiner_msgs_action: Action = ListenJoinerMsgs()
        send_joiner_message_action: Action = SendJoinerMsgs()

        joiner_role: Role = Joiner()
        joiner_role.register_values(
            server_ip=ip, nickname=nickname, clients=client_node.ledger
        )
        joiner_role.hook_action(action=listen_joiner_msgs_action)
        joiner_role.hook_action(action=send_joiner_message_action)

        client_node.hook_role(role=joiner_role)
        client_node.start()

        client_node.register_action_values(
            client=joiner_role.client,
            clients=client_node.ledger,
            nickname=client_node.nickname,
        )

        print(client_node.ledger)

        client_node.start_threads()
