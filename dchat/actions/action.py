"""
Abstract class representing the template for an action class.
"""
from abc import abstractmethod
from typing import Dict


class Action:
    """
    The abstract class representing template for action classes, with
    methods to be implemented by the inheriting classes. This contains
    methods to register values at runtime and starting an action in a
    separate thread.
    """

    def __init__(self) -> None:
        self._thread_values: Dict = {}

    def register_values(self, **kwargs) -> None:
        """
        Register values at runtime.
        :param kwargs: dictionary containing the values to be registered
        """
        self._thread_values = kwargs

    @abstractmethod
    def start(self) -> None:
        """
        Start the action in a separate thread.
        """
