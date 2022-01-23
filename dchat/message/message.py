"""
The actual message which can either be an internal
message or an actual message which has to be displayed
to STDOUT.
"""
import pickle

from dchat.message.command import Command
from dchat.message.dtype import DType
from dchat.utils import constants


class Message:
    """
    The standard message format, consisting of a command,
    a data type and the actual message.
    """

    def __init__(self, cmd: Command, dtype: DType, msg: str):
        self.__cmd: Command = cmd
        self.__dtype: DType = dtype
        self.__msg: str = msg

    @property
    def cmd(self) -> Command:
        """
        Returns the command of the message.
        :return: The command of the message.
        """
        return self.__cmd

    @property
    def dtype(self) -> DType:
        """
        Returns the data type of the message.
        :return: The data type of the message.
        """
        return self.__dtype

    @property
    def msg(self) -> str:
        """
        Returns the actual string of the message.
        :return: The actual string of the message.
        """
        return self.__msg

    def __str__(self) -> str:
        """
        String representation of a message.
        :return: The string representation of a message.
        """
        return f"[{self.__cmd}]: {self.__dtype} -> {self.__msg}"

    def serialize(self) -> bytes:
        """
        Serializes the message into a byte array.
        :return: The serialized message.
        """
        msg: bytes = pickle.dumps(self)
        msg = bytes(f"{len(msg):<{constants.MSG_HEADER_LENGTH}}", "utf-8") + msg

        return msg
