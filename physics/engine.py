import numpy as np
from rocketcea.cea_obj_w_units import CEA_Obj as CEA_Obj_w_units
from scipy.optimize import least_squares

from network.model import Model


class Engine(Model):
    cea_fuel = 'Isopropanol'
    cea_ox = 'LOX'

    c_psiPa = 6894.76  # Conversion from psi to Pa

    # Parameters
    d_cc = 0.0762  # Combustion chamber diameter, 3 in --> [m]
    d_t = 1.66878 * 2 / 100  # Throat diameter [m]
    d_e = 7.4781 / 100  # Exit diameter [m]
    #p_c = 500 * c_psiPa  # Chamber pressure 500 psi --> [Pa]
    #p_c_bar = p_c / 1e5  # Chamber pressure [bar]
    p_e = 101325  # Exit pressure, sea level --> [Pa]
    p_amb = 101325  # Ambient atmospheric pressure [Pa]
    #PcOvPe = p_c / p_e  # = 32.38 for 500 psi chamber, sea level exit
    T_i = 298  # Initial propellant temperature [K]
    MR = 1.0  # Mixture ratio [-]

    A_cc = np.pi * (d_cc / 2) ** 2  # Combustion chamber area [m^2]
    A_t = np.pi * (d_t / 2) ** 2  # Throat area [m^2]
    A_e = np.pi * (d_e / 2) ** 2  # Exit area [m^2]
    cr = A_cc / A_t  # Contraction ratio
    eps = A_e / A_t  # Expansion ratio (epsilon)

    __slots__ = ("engine",)

    def __init__(self, name: str):
        super().__init__(name)
        self.interfaces = {"upstream_mass_flow_rate": 0.0, "downstream_mass_flow_rate": 0.0}
        self.engine = CEA_Obj_w_units(oxName=self.cea_ox, fuelName=self.cea_fuel, fac_CR=self.cr,
                        isp_units            = 'sec',
                        cstar_units          = 'm/sec',
                        pressure_units       = 'Pa',
                        temperature_units    = 'K',
                        sonic_velocity_units = 'm/sec',
                        enthalpy_units       = 'kJ/kg',
                        density_units        = 'kg/m^3',
                        specific_heat_units  = 'kJ/kg-K',
                        viscosity_units      = 'poise',
                        thermal_cond_units   = 'mcal/cm-K-s')

    def try_oneway_interface(self, other: "Model"):
        """
        Attempt to connect the engine to another model's interface.
        This method checks if the other model has compatible interfaces and connects them if possible.
        """
        if "downstream_mass_flow_rate" in self.interfaces and "upstream_mass_flow_rate" in other.interfaces:
            other.interfaces["upstream_mass_flow_rate"] = self.interfaces.get("downstream_mass_flow_rate", 0.0)

    def get_cstar(self, Pc: list[float]) -> list[float]:
        """
        Get the characteristic velocity (C*) of the engine at the given chamber pressure.
        This method uses the CEA model to compute the characteristic velocity based on the current conditions.
        """
        IspVac, Cstar, Tcomb, MW, gamma_th = self.engine.get_IvacCstrTc_ThtMwGam(Pc=Pc[0], MR=self.MR, eps=self.eps)
        upstream_mass_flow_rate = self.interfaces.get("upstream_mass_flow_rate", 0.0)
        return [upstream_mass_flow_rate - (Pc[0] * self.A_t / Cstar)]

    def calculate(self, time: float, dt: float | None = None) -> list[float]:
        """
        Calculate the state of the engine at the given time and time step.
        This method uses the CEA model to compute the engine performance based on the current conditions.
        """
        # Get upstream pressure and mass flow rate
        upstream_mass_flow_rate = self.interfaces.get("upstream_mass_flow_rate", 0.0)

        upstream_pressure = least_squares(
            self.get_cstar,
            [upstream_mass_flow_rate * 178000.0 / self.A_t],
        ).x[0]

        # Run CEA calculations
        IspVac, Cstar, Tcomb, MW, gamma_th = self.engine.get_IvacCstrTc_ThtMwGam(Pc=upstream_pressure, MR=self.MR, eps=self.eps)
        ERr, ERphi = self.engine.get_eqratio(Pc=upstream_pressure, MR=self.MR, eps=self.eps)
        CF = self.engine.get_PambCf(Pamb=self.p_amb,Pc=upstream_pressure, MR=self.MR, eps=self.eps)[0]

        sonicVelocities = self.engine.get_SonicVelocities(Pc=upstream_pressure, MR=self.MR, eps=self.eps, frozen=0, frozenAtThroat=0)
        sonicVelocity_e = sonicVelocities[2]
        sonicVelocity_th = sonicVelocities[1]

        machNumber_e = self.engine.get_MachNumber(Pc=upstream_pressure, MR=self.MR, eps=self.eps, frozen=0, frozenAtThroat=0)
        v_e = machNumber_e * sonicVelocity_e
        v_th = sonicVelocity_th

        rho_e = self.engine.get_Densities(Pc=upstream_pressure, MR=self.MR, eps=self.eps, frozen=0, frozenAtThroat=0)[2]
        rho_th = self.engine.get_Densities(Pc=upstream_pressure, MR=self.MR, eps=self.eps, frozen=0, frozenAtThroat=0)[1]

        m_dot_e = rho_e * v_e * self.A_e
        m_dot_th = rho_th * v_th * self.A_t  # diagnostic, should equal m_dot_e

        # Update downstream interfaces
        self.interfaces["downstream_mass_flow_rate"] = m_dot_e

        return [m_dot_e - m_dot_th, upstream_mass_flow_rate - m_dot_e]