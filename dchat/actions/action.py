from abc import abstractmethod


class Action:
    def __init__(self):
        self._thread_values = {}

    def register_values(self, **kwargs) -> None:
        self._thread_values = kwargs

    @abstractmethod
    def start(self) -> None:
        pass
