import numpy
import pandas as pd
from functions.base_function import BaseFunction

class IntegralP(BaseFunction):

    a = b = -1

    def __init__(self, integrand):
        super().__init__(integrand)

    def calculate(self, y, total_parts=10000):
        # Integrate func here
        if y <= 0:
            return 1
        if y >= 1:
            return 0
        result = 0
        n = total_parts
        h = (1 - y) / (total_parts * 2)
        points = numpy.linspace(y, 1, num=n * 2 + 1)

        if len(points) == 0:
            return 0
        result += self.params.calculate(points[0])
        result += self.params.calculate(points[-1])
        for i in range(1, n):
            result += 2 * self.params.calculate(points[2 * i])
        for i in range(1, n + 1):
            result += 4 * self.params.calculate(points[2 * i - 1])
        return result * h / 3
        #return 1/2 * self.a * self.b * (1 - np.power(y, 2)) - 1/3 * self.a * (1 - np.power(y, 3))

    def tabulate(self, points, filename):
        with open("tabulated_functions/" + filename, 'w') as f:
            for x in points:
                f.write("{} {}\n".format(x, self.calculate(x, (points[1] - points[0]) / 1)))
