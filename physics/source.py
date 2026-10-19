from network.model import Model


class Source(Model):
    """
    A magical source that provides a constant mass flow rate to the feed system.
    In the future, this will act as a magic boundary condition where f(t) = (m_dot, P).
    """

    __slots__ = ("mass_flow_rate",)

    def __init__(self, name: str, mass_flow_rate: float) -> None:
        super().__init__(name)
        self.interfaces = {"mass_flow_rate": mass_flow_rate}
        self.mass_flow_rate = mass_flow_rate

    def try_oneway_interface(self, other: "Model"):
        """
        Attempt to connect the source to another model's interface.
        This method checks if the other model has compatible interfaces and connects them if possible.
        """
        if "mass_flow_rate" in self.interfaces and "upstream_mass_flow_rate" in other.interfaces:
            other.interfaces["upstream_mass_flow_rate"] = self.interfaces.get("mass_flow_rate", 0.0)
    def calculate(self, time: float, dt: float | None = None) -> list[float]:
        """
        Calculate the state of the source at the given time and time step.
        The source maintains a constant mass flow rate.
        """
        # The source maintains a constant mass flow rate
        self.interfaces["mass_flow_rate"] = self.mass_flow_rate

        return []

    def __repr__(self) -> str:
        return f"<Source {self.name}: mass_flow_rate={self.interfaces['mass_flow_rate']}>"