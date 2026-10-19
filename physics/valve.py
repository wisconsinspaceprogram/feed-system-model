import numpy as np

from network.model import Model


class Valve(Model):
    """
    A valve model that can be opened or closed to control flow in the feed system.
    """

    def __init__(self, name: str, is_open: bool = True) -> None:
        super().__init__(name)
        self.interfaces = {"upstream_mass_flow_rate": 0.0, "downstream_mass_flow_rate": 0.0}
        self.is_open = is_open

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def toggle(self) -> None:
        self.is_open = not self.is_open

    def try_oneway_interface(self, other: "Model"):
        """
        Attempt to connect the valve to another model's interface.
        This method checks if the other model has compatible interfaces and connects them if possible.
        """
        if "downstream_mass_flow_rate" in self.interfaces and "upstream_mass_flow_rate" in other.interfaces:
            other.interfaces["upstream_mass_flow_rate"] = self.interfaces.get("downstream_mass_flow_rate", 0.0)
    def calculate(self, time: float, dt: float | None = None) -> list[float]:
        """
        Calculate the state of the valve at the given time and time step.
        If the valve is open, it allows flow; if closed, it blocks flow.
        """
        if self.is_open:
            # interfaces.get should never fail
            self.interfaces["downstream_mass_flow_rate"] = self.interfaces.get("upstream_mass_flow_rate", 0.0)
        else:
            self.interfaces["downstream_mass_flow_rate"] = np.float64(0.0)

        return []

    def __repr__(self) -> str:
        state = "open" if self.is_open else "closed"
        return f"<Valve {self.name}: {state}>"