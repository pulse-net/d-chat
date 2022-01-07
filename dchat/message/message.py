import pickle

from .command import Command
from .dtype import DType
from ..utils import constants


class Message:
    def __init__(self, cmd: Command, dtype: DType, msg: str):
        self.__cmd: Command = cmd
        self.__dtype: DType = dtype
        self.__msg: str = msg

    @property
    def cmd(self) -> Command:
        return self.__cmd

    @property
    def dtype(self) -> DType:
        return self.__dtype

    @property
    def msg(self) -> str:
        return self.__msg

    def __str__(self) -> str:
        return f"[{self.__cmd}]: {self.__dtype} -> {self.__msg}"

    def serialize(self) -> bytes:
        msg = pickle.dumps(self)

        return msg
