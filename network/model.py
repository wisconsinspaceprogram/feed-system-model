from abc import abstractmethod
from typing import cast

from network.node import Node


class Model(Node):
    """
    Base class for physics models in the feed system graph.
    """

    __slots__ = ("interfaces",)

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.interfaces: dict[str, float] = {}

    @abstractmethod
    def try_oneway_interface(self, other: "Model"):
        pass

    @abstractmethod
    def calculate(self, time: float, dt: float | None = None) -> list[float]:
        """
        Calculate the state of the model at the given time and time step.
        This method should be overridden by subclasses to implement specific model behavior.

        :param time: The current simulation time.
        :param dt: The time step for the simulation (optional).
        :return: residuals
        """
        raise NotImplementedError("Subclasses must implement the calculate method.")

    def calculate_all(self, time: float, dt: float | None = None, processed_list: list = [], x0: list[float] = []) -> list[float]:
        """
        Calculate the state of the model and all connected models at the given time and time step.
        This method recursively calls the calculate method on all connected models.

        :param processed_list: A list of models that have already been processed to avoid infinite recursion.
        :param time: The current simulation time.
        :param dt: The time step for the simulation (optional).
        :return: residuals
        """
        residuals = []
        for (i, (key, _)) in enumerate(self.interfaces.items()):
            if i < len(x0):
                self.interfaces[key] = x0[i]
        residuals.extend(self.calculate(time, dt))
        for connection in self.connections:
            if connection not in processed_list:
                processed_list.append(connection)
                if isinstance(connection, Model):
                    residuals.extend(connection.calculate_all(time, dt, processed_list))

                    """for (name, value) in self.interfaces.items():
                        if name in connection.interfaces:
                            connection.interfaces[name] = value
                            print(f"setting interfaces on \"{connection.name}\" {name}: {value}")"""
                    self.try_oneway_interface(connection)

        return residuals

    def calculate_residuals(self, x0: list[float]) -> list[float]:
        return self.calculate_all(0.0, x0=x0)

    def snapshot_graph(self, processed_list: list = []) -> "ModelSnapshot":
        snapshot = ModelSnapshot(self)
        for connection in self.connections:
            if connection in processed_list:
                continue

            processed_list.append(connection)
            if not isinstance(connection, Model):
                continue

            child_snapshot = self.snapshot_graph(processed_list)

            snapshot.connect(child_snapshot)

        return snapshot

class ModelSnapshot:

    __slots__ = ["inputs", "outputs", "connections"]
    def __init__(self, model: Model) -> None:
        self.inputs = model.inputs
        self.outputs = model.outputs
        self.connections = []

    def connect(self, other: "ModelSnapshot") -> None:
        """
        Connect this snapshot to another snapshot.

        :param snapshot: The ModelSnapshot to connect to.
        """
        self.connections.append(other)
        other.connections.append(self)