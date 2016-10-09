class BaseFunction():

    def __init__(self, params):
        self.params = params

    def calculate(self, x):
        pass

    def tabulate(self, points, filename):
        # Here write tabulating
        with open("tabulated_functions/" + filename, 'w') as f:
            for x in points:
                f.write("{} {}\n".format(x, self.calculate(x)))

    def calculate_interpolation_coeffs(self):
        # Here write calculation of interpolation coeffs
        pass