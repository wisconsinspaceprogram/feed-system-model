from abc import abstractmethod
from typing import cast

from network.node import Node


class Model(Node):
    """
    Base class for physics models in the feed system graph.
    """

    __slots__ = ("inputs", "outputs",)

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.inputs: dict[str, float] = {}
        self.outputs: dict[str, float] = {}

    @abstractmethod
    def calculate(self, time: float, dt: float | None = None) -> None:
        """
        Calculate the state of the model at the given time and time step.
        This method should be overridden by subclasses to implement specific model behavior.

        :param time: The current simulation time.
        :param dt: The time step for the simulation (optional).
        """
        raise NotImplementedError("Subclasses must implement the calculate method.")

    def calculate_all(self, time: float, dt: float | None = None, processed_list: list = []) -> None:
        """
        Calculate the state of the model and all connected models at the given time and time step.
        This method recursively calls the calculate method on all connected models.

        :param processed_list: A list of models that have already been processed to avoid infinite recursion.
        :param time: The current simulation time.
        :param dt: The time step for the simulation (optional).
        """
        self.calculate(time, dt)
        for connection in self.connections:
            if connection not in processed_list:
                processed_list.append(connection)
                if connection is Model:
                    connection = cast(Model, connection)
                    connection.calculate_all(time, dt, processed_list)