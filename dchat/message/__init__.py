"""
Standard format for a message which is used
in both sender and receiver side. A message
consists of three parts:
1. Command (The command is used to identify the intent of message
            as not all messages are intended to be displayed to STDOUT
            but can be internal messages for some task like updating
            ledger).
2. DType   (The data type of the message is used to identify the
            sub type of the intent, this can be a sub part of a message,
            like in case of a ledger update it can be ip address, d address, etc.)
3. Message (This is the actual message which is sent and received, if this is of command
            and dtype MSG then this string is displayed to STDOUT).
"""
