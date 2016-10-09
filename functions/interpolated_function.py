from functions.base_function import BaseFunction

class InterpolatedFunction(BaseFunction):

    def __init__(self, interpolation_coeffs):
        super().__init__(interpolation_coeffs)

    def calculate(self, t):
        # Calculate function
        return t
