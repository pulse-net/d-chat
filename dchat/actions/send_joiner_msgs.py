"""
Sends message from a joinee to all other joinees
via the creator.
"""
import socket
from typing import Optional

from dchat.actions.action import Action
from dchat.message.command import Command
from dchat.message.dtype import DType
from dchat.utils import encode


class SendJoinerMsgs(Action):
    """
    Send message from a joinee to all other joinees
    via the creator, the message is sent to the creator
    which broadcasts it to all other joinees.
    """

    def start(self) -> None:
        """
        Starts listening for messages from
        STDIN and sends them to the creator.
        """
        nickname: Optional[str] = self._thread_values.get("nickname")
        client: Optional[socket.socket] = self._thread_values.get("client")

        assert client is not None

        while True:
            message: str = input(f"{nickname}> ")

            encode.send_msg_with_end_token(
                cmd=Command.MSG,
                dtype=DType.MSG,
                msg=f"\n{nickname}> {message}",
                client=client,
            )
