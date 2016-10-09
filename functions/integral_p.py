import numpy as np
from functions.base_function import BaseFunction

class IntegralP(BaseFunction):

    def __init__(self, integrand_tabulated_filename):
        super().__init__(integrand_tabulated_filename)

    def calculate(self, y):
        # Integrate func here
        #if y < 0:
        #    return self.calculate(0)
        return np.power((y - 1), 2) * (2 * y + 1)
