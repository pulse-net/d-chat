from typing import List

from ledger_entry import LedgerEntry


class Ledger:
    def __init__(self) -> None:
        self.__ledger = []

    def bulk_entry(self, ledger_entries: List[LedgerEntry]) -> None:
        self.__ledger.extend(ledger_entries)

    def add_entry(self, ledger_entry: LedgerEntry) -> None:
        if ledger_entry not in self.__ledger:
            self.__ledger.append(ledger_entry)

    @property
    def ledger(self) -> List[LedgerEntry]:
        return self.__ledger

    def __str__(self) -> str:
        ledger_str = ""
        for entry in self.__ledger:
            ledger_str += str(entry) + "\n"

        return ledger_str

    def __getitem__(self, idx):
        return self.__ledger[idx]