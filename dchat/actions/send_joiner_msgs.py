from .action import Action
from ..message.message import Message
from ..message.command import Command
from ..message.dtype import DType


class SendJoinerMsgs(Action):
    def __init__(self):
        super(SendJoinerMsgs, self).__init__()

    def start(self) -> None:
        nickname = self._thread_values.get('nickname')
        client = self._thread_values.get('client')

        while True:
            message = input(f"{nickname}> ")
            m = Message(Command.MSG, DType.MSG, f"\n{nickname}> {message}")
            client.send(m.serialize())
            client.send("<END>".encode("utf-8"))

