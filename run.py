import numpy
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PyQt5.QtWidgets import QApplication as QApp5
import cauchi_problem
import ui
from functions import z_function, p_function, s_function, integral_p, \
                      interpolated_function, f_function

def initialize_functions(a, b, c, d):
    # Write normal input later
    print("write parameters for p(w) (a, b)\none parameter -- one line")
    #a, b = float(input()), float(input())
    a, b = 6, 1
    p_func = p_function.PFunction([a, b])

    print("write parameter for z(t) (one float)\none parameter -- one line")
    #z_par = float(input())
    c = 5
    z_func = z_function.ZFunction([c])

    print("write parameter for s(t)\none parameter -- one line")
    #s_par = float(input())
    d = 3
    s_func = s_function.SFunction([d])

    return p_func, z_func, s_func


def get_initial_parameters():
    print("enter x0, y0, beta, T\none parameter -- one line")
    #x_0, y_0, beta, T = float(input()), float(input()), float(input()), float(input())
    x_0, y_0, beta, T = 0, 0, 1, 1
    return x_0, y_0, beta, T


def draw_graphics():
    plt.figure(1)

    # initialize plots data and add them as subplot
    t_x, x = [], []
    with open("x_answer.txt", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_x.append(float(data[0]))
            x.append(float(data[1]))
    plt.subplot(231)
    plt.plot(t_x, x)
    plt.title('X(t)')

    t_s, s = [], []
    with open("tabulated_functions/s_func_tabulated", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_s.append(float(data[0]))
            s.append(float(data[1]))
    plt.subplot(232)
    plt.plot(t_s, s)
    plt.title('S(t)')

    t_p, p = [], []
    with open("tabulated_functions/p_func_tabulated", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_p.append(float(data[0]))
            p.append(float(data[1]))
    plt.subplot(233)
    plt.plot(t_p, p)
    plt.title('p(w)')

    t_z, z = [], []
    with open("tabulated_functions/z_func_tabulated", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_z.append(float(data[0]))
            z.append(float(data[1]))
    plt.subplot(234)
    plt.plot(t_z, z)
    plt.title('Z(t)')

    x_s = [x[i] - s[i] for i in range(0, len(t_x))]
    plt.subplot(235)
    plt.plot(t_x, x_s)
    plt.title('X(t) - S(t)')

    t_y, y = [], []
    with open("y_answer.txt", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_y.append(float(data[0]))
            y.append(float(data[1]))
    plt.subplot(236)
    plt.plot(t_y, y)
    plt.title('Y(t)')

    plt.show()


def main(a, b, c, d, x_0, y_0, beta, T):
    N = 10000

    # initialize functions
    p_func, z_func, s_func = initialize_functions(a, b, c ,d)

    
    # Tabulate them
    p_func.tabulate(numpy.arange(0, T + T/N, T/N), "p_func_tabulated")
    z_func.tabulate(numpy.arange(0, T + T/N, T/N), "z_func_tabulated")
    s_func.tabulate(numpy.arange(0, T + T/N, T/N), "s_func_tabulated")
    integral = integral_p.IntegralP("p_func_tabulated")
    integral.tabulate(numpy.arange(0, T + T/N, T/N), "integral_tabulated")

    # Calculate interpolation coefficients and make corresponding functions (uncomment for real interpolation)
    #p_interpolated = InterpolatedFunction(p_func.calculate_interpolation_coeffs())
    #z_interpolated = InterpolatedFunction(z_func.calculate_interpolation_coeffs())
    #s_interpolated = InterpolatedFunction(s_func.calculate_interpolation_coeffs())
    #u_interpolated = InterpolatedFunction(integral.calculate_interpolation_coeffs())
    p_interpolated = p_func  # delete this later
    z_interpolated = z_func  # delete this later
    s_interpolated = s_func  # delete this later
    u_interpolated = integral  # delete this later

    # Initialize f function
    f_func = f_function.FFunction([beta, s_interpolated, z_interpolated])

    cauchi_problem.solve(x_0, y_0, beta, T,  N,
                         p_interpolated, z_interpolated,
                         s_interpolated, u_interpolated, f_func)
    ui.draw_graphics()


if __name__ == '__main__':
    app = QApp5(sys.argv)
    window = ui.Window(main)
    sys.exit(app.exec_())

    #main()
