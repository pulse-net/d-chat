import re

from action import Action
from ledger_entry import LedgerEntry


class ListenInitialLedger(Action):
    def __init__(self):
        super(ListenInitialLedger, self).__init__()

    def start(self) -> None:
        client = self._thread_values.get('client')
        clients = self._thread_values.get('clients')

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

        for ip, nick_name in zip(ips, nicknames):
            clients.add_entry(LedgerEntry(ip_address=ip, nick_name=nick_name))

        print("Initial ledger: ")
        print(clients)
