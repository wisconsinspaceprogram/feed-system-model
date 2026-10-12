from network.model import Model


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

def snapshot_graph(model: Model, processed_list: list = []) -> ModelSnapshot:
    snapshot = ModelSnapshot(model)
    for connection in model.connections:
        if connection in processed_list:
            continue

        processed_list.append(connection)
        if not isinstance(connection, Model):
            continue

        child_snapshot = snapshot_graph(connection, processed_list)


