from network.model import Model


class Feedline(Model):
    """
    A feedline model that represents a pipe or conduit for fluid flow in the feed system.
    """

    __slots__ = ('flow_coefficient',)

    def __init__(self, name: str, flow_coefficient: float) -> None:
        super().__init__(name)
        self.interfaces = {"upstream_mass_flow_rate": 0.0, "downstream_mass_flow_rate": 0.0}
        self.flow_coefficient = flow_coefficient

    def try_oneway_interface(self, other: "Model"):
        """
        Attempt to connect the feedline to another model's interface.
        This method checks if the other model has compatible interfaces and connects them if possible.
        """
        if "downstream_mass_flow_rate" in self.interfaces and "upstream_mass_flow_rate" in other.interfaces:
            other.interfaces["upstream_mass_flow_rate"] = self.interfaces.get("downstream_mass_flow_rate", 0.0)

    def calculate(self, time: float, dt: float | None = None) -> list[float]:
        """
        Calculate the state of the feedline at the given time and time step.
        Incompressible fluids are assumed at the moment.
        """
        # Conserve mass
        self.interfaces["downstream_mass_flow_rate"] = self.interfaces["upstream_mass_flow_rate"]

        return []

    def __repr__(self) -> str:
        return f"<Feedline {self.name}: flow_coefficient={self.flow_coefficient}>"