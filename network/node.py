from abc import ABC

class Node(ABC):
    """
    Base class for nodes in the feed system graph.
    """
    __slots__ = ("connections", "name")

    def __init__(self, name: str):
        self.name = name
        self.connections: list["Node"] = []

    @property
    def degree(self) -> int:
        return len(self.connections)

    def connect(self, other: "Node"):
        if other not in self.connections:
            self.connections.append(other)
            other.connect(self)

    def disconnect(self, other: "Node"):
        if other in self.connections:
            self.connections.remove(other)
            other.disconnect(self)

    def render(self):
        """
        Implementation of this method is optional
        """
        pass

    def __repr__(self) -> str:
        return f"<Node {self.name}>"