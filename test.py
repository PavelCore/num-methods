from functions import z_function, p_function, s_function, integral_p, \
                      interpolated_function, f_function
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy


def initialize_functions(a, b, c, d):
    p_func = p_function.PFunction([a, b])
    z_func = z_function.ZFunction([c])
    s_func = s_function.SFunction([d])

    return p_func, z_func, s_func

T = 1
N = 100

p_func, z_func, s_func = initialize_functions(6, 1, 5, 3)

#p_func.tabulate(numpy.arange(0, T + T/N, T/N), "p_func_tabulated")
#z_func.tabulate(numpy.arange(0, T + T/N, T/N), "z_func_tabulated")
#s_func.tabulate(numpy.arange(0, T + T/N, T/N), "s_func_tabulated")

p_interpolated = interpolated_function.InterpolatedFunction("p_func_tabulated")
integral_interp = integral_p.IntegralP(p_interpolated)
intergral = integral_p.IntegralP(p_func)

x, y, y_int = [], [], []

for i in numpy.arange(0, T + T/(N*30), T/(N*30)):
    x.append(i)
    y.append(intergral.calculate(i))
    y_int.append(integral_interp.calculate(i))

plt.plot(x, y, x, y_int)
plt.show()