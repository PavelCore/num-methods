from functions.base_function import BaseFunction

class FFunction(BaseFunction):

    # NOTE that FFunction isn't like the other functions, as it requires 
    # x(t), which will be calculated iteratively during solving cauchi problem
    # that is why calculate() needs x(t_i) as an argument
    # thus methods tabulate() and calculate_interpolation_coeffs() makes no sence

    def __init__(self, params):
        # beta -- 0
        # s(t) -- 1
        # z(t) -- 2
        # N    -- 3
        super().__init__(params)

    def calculate(self, t, x_t):
        N = self.params[3]
        #print("in f: t={0:.4f}, x(t)={1:.4f}, s(t)={2:.4f}, x(t) - s(t)={3:.4f}".format(t, x_t,
        #        self.params[1].calculate(t),
        #        x_t - self.params[1].calculate(t)))
        return self.params[0] * (x_t - self.params[1].calculate(t))

    def tabulate(self):
        pass

    def calculate_interpolation_coeffs(self):
        pass