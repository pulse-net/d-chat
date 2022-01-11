import socket

from ..message.command import Command
from ..message.dtype import DType
from ..message.message import Message
from ..message.token import Token


def send_msg_with_end_token(cmd: Command, dtype: DType, msg: str, client: socket.socket) -> None:
    message = Message(cmd, dtype, msg)
    client.send(message.serialize())
    client.send(str(Token.END).encode("utf-8"))