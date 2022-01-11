from dchat.actions.action import Action
from dchat.message.command import Command
from dchat.message.dtype import DType
from dchat.utils import encode


class SendJoineeMessage(Action):
    def start(self) -> None:
        clients = self._thread_values.get("clients")
        client_list = self._thread_values.get("client_list")

        while True:
            message = input(f"{clients[0].nick_name}> ")

            for client in client_list:
                encode.send_msg_with_end_token(
                    cmd=Command.MSG,
                    dtype=DType.MSG,
                    msg=f"\n{clients[0].nick_name}> {message}",
                    client=client,
                )
