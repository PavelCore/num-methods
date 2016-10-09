from functions.base_function import BaseFunction
from numpy import sin

class SFunction(BaseFunction):

    def __init__(self, params):
        super().__init__(params)

    def calculate(self, t):
        return self.params[0] * t + sin(t)