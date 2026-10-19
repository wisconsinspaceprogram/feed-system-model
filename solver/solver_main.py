import numpy
from scipy.optimize import least_squares, OptimizeResult

from network.model import Model


class Solver:
    __slots__ = ("model",)

    def __init__(self, model: Model):
        """
        Initialize the solver with a given model. The model should be the intended base node for calculation.
        It is what inputs will be sent into.
        :param model:
        """
        self.model = model

    def solve(self, x0: list[float]) -> OptimizeResult:
        result = least_squares(
            self.model.calculate_residuals,
            numpy.array(x0),
        )

        return result