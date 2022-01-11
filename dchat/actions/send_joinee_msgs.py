from .action import Action
from ..message.message import Message
from ..message.command import Command
from ..message.dtype import DType
from ..utils import encode


class SendJoineeMessage(Action):
    def __init__(self) -> None:
        super(SendJoineeMessage, self).__init__()

    def start(self) -> None:
        clients = self._thread_values.get('clients')
        client_list = self._thread_values.get('client_list')

        while True:
            message = input(f"{clients[0].nick_name}> ")

            for client in client_list:
                encode.send_msg_with_end_token(
                    cmd=Command.MSG, dtype=DType.MSG,
                    msg=f"\n{clients[0].nick_name}> {message}", client=client
                )
