import pickle

from dchat.message.message import Message
from dchat.message.command import Command
from dchat.message.dtype import DType


if __name__ == "__main__":
#     m = Message(Command.LEDGER_ENTRY, DType.LEDGER_IP, "10.0.0.240")
#
#     with open("message.obj", "wb") as file:
#         pickle.dump(m, file)
# #
    with open("message.obj", "rb") as file:
        m = pickle.load(file)

    print(m)