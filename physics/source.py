from network.model import Model


class Source(Model):
    """
    A magical source that provides a constant mass flow rate to the feed system.
    """

    __slots__ = ("mass_flow_rate", "pressure")

    def __init__(self, name: str, mass_flow_rate: float, pressure: float) -> None:
        super().__init__(name)
        self.inputs = {}
        self.outputs = {"mass_flow_rate": mass_flow_rate, "pressure": pressure}
        self.mass_flow_rate = mass_flow_rate
        self.pressure = pressure

    def calculate(self, time: float, dt: float | None = None) -> None:
        """
        Calculate the state of the source at the given time and time step.
        The source maintains a constant mass flow rate.
        """
        # The source maintains a constant mass flow rate
        self.outputs["mass_flow_rate"] = self.mass_flow_rate
        self.outputs["pressure"] = self.pressure

    def __repr__(self) -> str:
        return f"<Source {self.name}: mass_flow_rate={self.outputs['mass_flow_rate']}>"