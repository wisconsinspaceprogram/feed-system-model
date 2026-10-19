import math

from scipy.constants import R

from network.model import Model


class Tank(Model):
    """
    A tank model that represents a storage tank for fluid in the feed system.
    """

    Rs = 287.05  # J/(kg*K)
    __slots__ = ("volume", "density", "mass", "Cd", "A")

    def __init__(self, name: str, volume: float, mass: float, Cd: float, radius: float) -> None:
        super().__init__(name)
        self.interfaces = {"upstream_mass_flow_rate": 0.0, "downstream_mass_flow_rate": 0.0}
        self.volume = volume
        self.mass = mass
        self.Cd = Cd
        self.A = 3.14159 * radius ** 2
    def try_oneway_interface(self, other: "Model"):
        """
        Attempt to connect the tank to another model's interface.
        This method checks if the other model has compatible interfaces and connects them if possible.
        """
        if "downstream_mass_flow_rate" in self.interfaces and "upstream_mass_flow_rate" in other.interfaces:
            other.interfaces["upstream_mass_flow_rate"] = self.interfaces.get("downstream_mass_flow_rate", 0.0)

    def mass_flow_rate(self, P):
        """Return the gas mass flow rate in kg/s."""

        P_ambient = 1.0 # atm
        gamma = 1.4
        T = 293.15 # K

        if P <= P_ambient:
            return 0.0

        pressure_ratio = P_ambient / P
        critical_ratio = (2 / (gamma + 1)) ** (
                gamma / (gamma - 1)
        )

        if pressure_ratio <= critical_ratio:
            # Choked flow
            mdot = (
                    self.Cd * self.A * P
                    * math.sqrt(gamma / (self.Rs * T))
                    * (2 / (gamma + 1)) ** (
                            (gamma + 1) / (2 * (gamma - 1))
                    )
            )
        else:
            # Subsonic, unchoked flow
            mdot = (
                    self.Cd * self.A * P
                    * math.sqrt(
                2 * gamma / (self.Rs * T * (gamma - 1))
                * (
                        pressure_ratio ** (2 / gamma)
                        - pressure_ratio ** (
                                (gamma + 1) / gamma
                        )
                )
            )
            )

        return mdot

    def calculate(self, time: float, dt: float | None = None) -> list[float]:
        """
        Calculate the state of the tank at the given time and time step.
        Incompressible fluids are assumed at the moment.
        """

        P = self.mass * self.Rs * 293.15 / self.volume
        m_dot = self.mass_flow_rate(P)
        self.interfaces["downstream_mass_flow_rate"] = m_dot

        return []

    def __repr__(self) -> str:
        return f"<Tank {self.name}: volume={self.volume}, density={self.density}, mass={self.mass}>"