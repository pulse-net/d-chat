"""
Representation of a Node in a P2P network, where each node can
have multiple roles and each role can perform multiple actions,
all of these actions have to be run in an infinite loop in their own thread.
"""
from typing import List

from dchat.roles.role import Role
from dchat.ledger.ledger import Ledger
from dchat.ledger.ledger_entry import LedgerEntry
from dchat.utils import helper


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
        """
        Adds itself to the ledger of the node.
        """
        self_client: LedgerEntry = LedgerEntry(
            ip_address=helper.get_ip(), nick_name=self.__nickname
        )
        self.__ledger.add_entry(self_client)

    def start(self) -> None:
        """
        Starts all the threads in every role of the node.
        """
        for role in self.__roles:
            if role.role_type == "Joiner":
                self.__ledger.empty_ledger()
            role.start()

    def register_action_values(self, **kwargs) -> None:
        """
        Registers values dynamically to the actions via the roles.
        :param kwargs: Values to be registered.
        """
        for role in self.__roles:
            for action in role.actions:
                action.register_values(**kwargs)

    def start_threads(self) -> None:
        """
        Starts all the role threads.
        """
        for role in self.__roles:
            role.start_threads()

    def hook_role(self, role: Role) -> None:
        """
        Hooks a rule to the node.
        :param role: Role to be hooked.
        """
        self.__roles.append(role)

    @property
    def nickname(self) -> str:
        """
        Returns the nickname of the node.
        :return: Nickname of the node.
        """
        return self.__nickname

    @property
    def ledger(self) -> Ledger:
        """
        Returns the ledger of the node.
        :return: Ledger of the node.
        """
        return self.__ledger
