"""
Ledger represents the basic unit for representing
information about creator and joinees which is
useful for sending and receiving messages.
"""
from typing import List

from dchat.ledger.ledger_entry import LedgerEntry


class Ledger:
    """
    A ledger contains a list of ledger entries which
    holds the actual information.
    """

    def __init__(self) -> None:
        """
        Initialize the ledger object.
        """
        self.__ledger: List[LedgerEntry] = []

    def bulk_entry(self, ledger_entries: List[LedgerEntry]) -> None:
        """
        Adds multiple ledger entries to the ledger.
        :param ledger_entries: the ledger entries to add.
        """
        self.__ledger.extend(ledger_entries)

    def add_entry(self, ledger_entry: LedgerEntry) -> None:
        """
        Adds a single ledger entry to the ledger.
        :param ledger_entry: the ledger entry to add.
        """
        if ledger_entry not in self.__ledger:
            self.__ledger.append(ledger_entry)

    def empty_ledger(self) -> None:
        """
        Empties the ledger.
        """
        self.__ledger = []

    @property
    def ledger(self) -> List[LedgerEntry]:
        """
        Returns all the ledger entries.
        :return: the ledger entries.
        """
        return self.__ledger

    def __str__(self) -> str:
        """
        Returns a string representation of the ledger.
        :return: the string representation.
        """
        ledger_str: str = ""
        for entry in self.__ledger:
            ledger_str += str(entry) + "\n"

        return ledger_str

    def __getitem__(self, idx: int) -> LedgerEntry:
        """
        Returns the ledger entry at the given index.
        :param idx: the index of the ledger entry.
        :return: the ledger entry.
        """
        return self.__ledger[idx]
