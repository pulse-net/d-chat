from dchat.actions.action import Action
from dchat.message.command import Command
from dchat.message.dtype import DType
from dchat.utils import encode


class SendJoinerMsgs(Action):
    def start(self) -> None:
        nickname = self._thread_values.get("nickname")
        client = self._thread_values.get("client")

        while True:
            message = input(f"{nickname}> ")

            encode.send_msg_with_end_token(
                cmd=Command.MSG,
                dtype=DType.MSG,
                msg=f"\n{nickname}> {message}",
                client=client,
            )
