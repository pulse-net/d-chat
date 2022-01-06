import re

from .action import Action
from ..ledger.ledger_entry import LedgerEntry


class ListenJoinerMsgs(Action):
    def __init__(self):
        super(ListenJoinerMsgs, self).__init__()

    def start(self) -> None:
        client = self._thread_values.get('client')
        clients = self._thread_values.get('clients')

        is_update = False
        ip = ""
        nickname = ""
        timestamp = ""
        daddr = ""

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
                            elif re.match(r"\d+\.\d+", val):
                                timestamp = val
                            elif re.match(r"[0-9a-fA-F]+", val) and len(val) == 10:
                                daddr = val
                            elif val != "<STOP>":
                                nickname = val

                        if ip != "" and nickname != "" and timestamp != "" and daddr != "":
                            clients.add_entry(LedgerEntry(ip_address=ip, nick_name=nickname, 
                                                          timestamp=timestamp, daddr=daddr))
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

