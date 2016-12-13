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

def func_to_min(c):
    return c[0] + 10 * c[1]


def main(a, b, c, d, x_0, y_0, beta, T, calculating_mod):
    if calculating_mod != "auto":
        c1, c2 = calculate_manual(a, b, c, d, x_0, y_0, beta, T)
        print("c1: {}\n c2: {}".format(c1, c2))
        ui.draw_graphics()
        return
    left, right = beta[0], beta[1]
    eps = (right - left) / 20
    delta = (right - left) / 1000
    while right - left > eps:
        print("left: {1}, right: {0}".format(right, left))
        x1 = (right + left - delta) / 2
        x2 = (right + left + delta) / 2
        y1 = func_to_min(calculate_manual(a, b, c, d, x_0, y_0, x1, T))
        y2 = func_to_min(calculate_manual(a, b, c, d, x_0, y_0, x2, T))
        if y1 >= y2:
            left = x1
        else:
            right = x2
    c1, c2 = calculate_manual(a, b, c, d, x_0, y_0, (left + right) / 2, T)
    print("final beta:", (left + right) / 2)
    print("c1: {}\n c2: {}".format(c1, c2))
    ui.draw_graphics()


def calculate_manual(a, b, c, d, x_0, y_0, beta, T):
    N = 50

    # initialize functions
    p_func, z_func, s_func = initialize_functions(a, b, c ,d)

    
    # Tabulate them
    p_func.tabulate(numpy.arange(0, T + T/N, T/N), "p_func_tabulated")
    z_func.tabulate(numpy.arange(0, T + T/N, T/N), "z_func_tabulated")
    s_func.tabulate(numpy.arange(0, T + T/N, T/N), "s_func_tabulated")

    #p_interpolated = p_func  # delete this later
    #z_interpolated = z_func  # delete this later
    #s_interpolated = s_func  # delete this later
    p_interpolated = interpolated_function.InterpolatedFunction("p_func_tabulated")
    z_interpolated = interpolated_function.InterpolatedFunction("z_func_tabulated")
    s_interpolated = interpolated_function.InterpolatedFunction("s_func_tabulated")

    p_interpolated.tabulate(numpy.arange(0, T + T/(N * 100), T/(N * 100)), "p_func_interp_tabulated")
    z_interpolated.tabulate(numpy.arange(0, T + T/(N * 100), T/(N * 100)), "z_func_interp_tabulated")
    s_interpolated.tabulate(numpy.arange(0, T + T/(N * 100), T/(N * 100)), "s_func_interp_tabulated")
    
    integral = integral_p.IntegralP(p_interpolated)

    # Calculate interpolation coefficients and make corresponding functions (uncomment for real interpolation)
    #u_interpolated = InterpolatedFunction(integral.calculate_interpolation_coeffs())
    
    #u_interpolated = integral  # delete this later

    # Initialize f function
    f_func = f_function.FFunction([beta, s_interpolated, z_interpolated, N])

    return cauchi_problem.solve(x_0, y_0, beta, T,  N,
                         p_interpolated, z_interpolated,
                         s_interpolated, integral, f_func)
    


if __name__ == '__main__':
    app = QApp5(sys.argv)
    window = ui.Window(main)
    sys.exit(app.exec_())
