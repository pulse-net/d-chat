"""
Encode messages in standard format.
"""
import socket
from typing import Optional

from dchat.message.command import Command
from dchat.message.dtype import DType
from dchat.message.message import Message
from dchat.message.token import Token


def send_msg_with_end_token(
    cmd: Command, dtype: DType, msg: str, client: Optional[socket.socket]
) -> None:
    """
    Send a message in standard format serialized and followed by
    an end token.
    :param cmd: The command of the message.
    :param dtype: The data type of the message.
    :param msg: The actual string of the message.
    :param client: The client socket to send the message to.
    """
    assert client is not None

    message: Message = Message(cmd, dtype, msg)
    client.send(message.serialize())
    client.send(str(Token.END).encode("utf-8"))
