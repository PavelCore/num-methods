import numpy
import sys
from PyQt5.QtWidgets import QApplication as QApp5
import cauchi_problem
import ui
from functions import z_function, p_function, s_function, integral_p, \
                      interpolated_function, f_function

def initialize_functions(a, b, c, d):
    p_func = p_function.PFunction([a, b])
    z_func = z_function.ZFunction([c])
    s_func = s_function.SFunction([d])

    return p_func, z_func, s_func


def main(a, b, c, d, x_0, y_0, beta, T, calculating_mod):
    if (calculating_mod == "auto"):
        beta = beta[0]
    N = 10000

    # initialize functions
    p_func, z_func, s_func = initialize_functions(a, b, c ,d)

    
    # Tabulate them
    p_func.tabulate(numpy.arange(0, T + T/N, T/N), "p_func_tabulated")
    z_func.tabulate(numpy.arange(0, T + T/N, T/N), "z_func_tabulated")
    s_func.tabulate(numpy.arange(0, T + T/N, T/N), "s_func_tabulated")

    p_interpolated = p_func  # delete this later
    z_interpolated = z_func  # delete this later
    s_interpolated = s_func  # delete this later
    #p_interpolated = InterpolatedFunction(p_func.calculate_interpolation_coeffs())
    #z_interpolated = InterpolatedFunction(z_func.calculate_interpolation_coeffs())
    #s_interpolated = InterpolatedFunction(s_func.calculate_interpolation_coeffs())
    
    integral = integral_p.IntegralP(p_interpolated)
    integral.tabulate(numpy.arange(0, T + T/N, T/N), "integral_tabulated")

    # Calculate interpolation coefficients and make corresponding functions (uncomment for real interpolation)
    #u_interpolated = InterpolatedFunction(integral.calculate_interpolation_coeffs())
    
    u_interpolated = integral  # delete this later

    # Initialize f function
    f_func = f_function.FFunction([beta, s_interpolated, z_interpolated, N])

    cauchi_problem.solve(x_0, y_0, beta, T,  N,
                         p_interpolated, z_interpolated,
                         s_interpolated, u_interpolated, f_func)
    ui.draw_graphics()


if __name__ == '__main__':
    app = QApp5(sys.argv)
    window = ui.Window(main)
    sys.exit(app.exec_())
