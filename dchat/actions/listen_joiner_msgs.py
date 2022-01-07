import re
import pickle

from .action import Action
from ..ledger.ledger_entry import LedgerEntry
from ..utils import constants
from ..message.command import Command
from ..message.dtype import DType


class ListenJoinerMsgs(Action):
    def __init__(self):
        super(ListenJoinerMsgs, self).__init__()

    def start(self) -> None:
        client = self._thread_values.get('client')
        clients = self._thread_values.get('clients')

        ip = ""
        nickname = ""
        timestamp = ""
        daddr = ""
        is_message_remaining = False
        current_message = b""

        while True:
            # try:
            message = client.recv(1024)
            messages = message.split(b"<END>")

            for message in messages:
                if len(message) == 0:
                    continue

                if not is_message_remaining:
                    msg_len = int(message[:constants.MSG_HEADER_LENGTH])
                    remaining_message = message[constants.MSG_HEADER_LENGTH:]

                    if len(remaining_message) == msg_len:
                        message = pickle.loads(remaining_message)
                        current_message = b""
                    else:
                        current_message += remaining_message
                        is_message_remaining = True
                else:
                    current_message += message
                    is_message_remaining = False

                    if len(current_message) == msg_len:
                        message = pickle.loads(current_message)
                        current_message = b""

                if message:
                    if message.cmd == Command.MSG:
                        print(message.msg)
                    elif message.cmd == Command.LEDGER_ENTRY:
                        if message.dtype == DType.LEDGER_IP:
                            ip = message.msg
                        elif message.dtype == DType.LEDGER_NICKNAME:
                            nickname = message.msg
                        elif message.dtype == DType.LEDGER_TIMESTAMP:
                            timestamp = message.msg
                        elif message.dtype == DType.LEDGER_DADDR:
                            daddr = message.msg

                        if ip and nickname and timestamp and daddr:
                            clients.add_entry(LedgerEntry(ip_address=ip, nick_name=nickname, 
                                                        timestamp=timestamp, daddr=daddr))
                            print("Ledger updated: ")
                            print(clients)

                            ip = ""
                            nickname = ""
                            timestamp = ""
                            daddr = ""
            # except Exception as e:
            #     print(e)
            #     break

