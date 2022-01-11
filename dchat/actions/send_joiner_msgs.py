from .action import Action
from ..message.message import Message
from ..message.command import Command
from ..message.dtype import DType
from ..utils import encode


class SendJoinerMsgs(Action):
    def __init__(self):
        super(SendJoinerMsgs, self).__init__()

    def start(self) -> None:
        nickname = self._thread_values.get('nickname')
        client = self._thread_values.get('client')

        while True:
            message = input(f"{nickname}> ")

            encode.send_msg_with_end_token(
                cmd=Command.MSG, dtype=DType.MSG,
                msg=f"\n{nickname}> {message}", client=client
            )
