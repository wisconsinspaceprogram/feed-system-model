from network.model import Model


class Feedline(Model):
    """
    A feedline model that represents a pipe or conduit for fluid flow in the feed system.
    """

    __slots__ = ('flow_coefficient',)

    def __init__(self, name: str, flow_coefficient: float) -> None:
        super().__init__(name)
        self.inputs = {"mass_flow_rate": 0.0, "upstream_pressure": 0.0}
        self.outputs = {"mass_flow_rate": 0.0, "downstream_pressure": 0.0}
        self.flow_coefficient = flow_coefficient

    def calculate(self, time: float, dt: float | None = None) -> None:
        """
        Calculate the state of the feedline at the given time and time step.
        Incompressible fluids are assumed at the moment.
        """
        upstream_pressure = self.inputs.get("upstream_pressure", 0.0)
        # assumes incompressible liquid
        self.outputs["downstream_pressure"] = self.flow_coefficient * upstream_pressure

        # Conserve mass
        self.outputs["mass_flow_rate"] = self.inputs["mass_flow_rate"]


    def __repr__(self) -> str:
        return f"<Feedline {self.name}: flow_coefficient={self.flow_coefficient}>"