from network.model import Model


class Valve(Model):
    """
    A valve model that can be opened or closed to control flow in the feed system.
    """

    def __init__(self, name: str, is_open: bool = True) -> None:
        super().__init__(name)
        self.inputs = {"mass_flow_rate": 0.0}
        self.outputs = {"mass_flow_rate": 0.0}
        self.is_open = is_open

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def toggle(self) -> None:
        self.is_open = not self.is_open

    def calculate(self, time: float, dt: float | None = None) -> None:
        """
        Calculate the state of the valve at the given time and time step.
        If the valve is open, it allows flow; if closed, it blocks flow.
        """
        if self.is_open:
            # inputs.get should never fail
            self.outputs["mass_flow_rate"] = self.inputs.get("mass_flow_rate", 0.0)
        else:
            self.outputs["mass_flow_rate"] = 0.0

    def __repr__(self) -> str:
        state = "open" if self.is_open else "closed"
        return f"<Valve {self.name}: {state}>"