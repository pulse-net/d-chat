"""
Send messages from creator to all joinees.
"""
import socket
from typing import List, Optional

from dchat.actions.action import Action
from dchat.message.command import Command
from dchat.message.dtype import DType
from dchat.utils import encode
from dchat.ledger.ledger import Ledger


class SendJoineeMessage(Action):
    """
    Send messages from server to to all joinees, this runs
    in an infinite loop in a separate thread.
    """

    def start(self) -> None:
        """
        Starts the process of listening for messages
        from STDIN and sending messages to all
        connected joinees.
        """
        clients: Optional[Ledger] = self._thread_values.get("clients")
        client_list: Optional[List[socket.socket]] = self._thread_values.get(
            "client_list"
        )

        assert clients is not None
        assert client_list is not None

        while True:
            message: str = input(f"{clients[0].nick_name}> ")

            for client in client_list:
                encode.send_msg_with_end_token(
                    cmd=Command.MSG,
                    dtype=DType.MSG,
                    msg=f"\n{clients[0].nick_name}> {message}",
                    client=client,
                )
