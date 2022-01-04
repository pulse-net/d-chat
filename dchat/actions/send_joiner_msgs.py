from .action import Action


class SendJoinerMsgs(Action):
    def __init__(self):
        super(SendJoinerMsgs, self).__init__()

    def start(self) -> None:
        nickname = self._thread_values.get('nickname')
        client = self._thread_values.get('client')

        while True:
            message = input(f"{nickname}> ")
            client.send(f"\n{nickname}> {message}".encode('ascii'))

