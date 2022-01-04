"""
Representation of a Node in a P2P network, where each node can
have multiple roles and each role can perform multiple actions,
all of these actions have to be run in an infinite loop in their own thread.
"""
from typing import List

from role import Role
from action import Action
from ledger import Ledger
from ledger_entry import LedgerEntry
import helper


class Node:
    """
    Represents a Node in the P2P network.
    """
    def __init__(self, nickname) -> None:
        self.__nickname: str = nickname
        self.__ledger: Ledger = Ledger()
        self.__roles: List[Role] = []

        self.__self_ledger_update()

    def __self_ledger_update(self) -> None:
        self_client = LedgerEntry(ip_address=helper.get_ip(), nick_name=self.__nickname)
        self.__ledger.add_entry(self_client)

    def start(self) -> None:
        """
        Starts all the threads in every role of the node.
        """
        for role in self.__roles:
            role.start()
            self.__register_action_values(role, role.actions)
            role.start_threads()

    def __register_action_values(self, role: Role, actions: List[Action]) -> None:
        for action in actions:
            action.register_values(
                server=role.server,
                client_list=role.client_list,
                clients=self.__ledger,
            )

    def hook_role(self, role: Role) -> None:
        """
        Hooks a new role to an existing node.

        role: Role to be hooked.
        """
        self.__roles.append(role)

    @property
    def ledger(self) -> Ledger:
        """
        Returns the ledger of the node.

        :return: Ledger of the node.
        """
        return self.__ledger
