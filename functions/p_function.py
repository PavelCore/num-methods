from functions.base_function import BaseFunction

class PFunction(BaseFunction):

    def __init__(self, params):
        super().__init__(params)

    def calculate(self, t):
        return self.params[0] * t * (self.params[1] - t) 