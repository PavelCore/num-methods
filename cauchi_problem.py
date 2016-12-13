import numpy
from functions import base_function, integral_p

def solve(x_0, y_0, beta, T, N,
          p_func, z_func, s_func, u_func, f_func):

    t_range = numpy.arange(0, T + T/N, T/N)

    def f_function(t, x, y):
        if t == T:
            derived_z_i = (z_func.calculate(t) - z_func.calculate(t - 1/(N * 10))) * N * 10
        else:
            derived_z_i = (z_func.calculate(t + 1/(N * 10)) - z_func.calculate(t)) * N * 10
        return derived_z_i * u_func.calculate(y)
    
    def g_function(t, x, y):
        return f_func.calculate(t, x)
    
    x_ans, y_ans = solve_diff_equation(f_function, g_function, t_range, x_0, y_0)

    #t_range = numpy.arange(0, T + T/N, T/N)
    #x_ans = [x_0]
    #y_ans = [y_0]
#
    #for i in range(0, len(t_range) - 1):
    #    x_i = x_ans[-1]
    #    y_i = y_ans[-1]
    #    tau_i = t_range[i + 1] - t_range[i]
    #    # Unused here because of the precision
    #    # (z' = (z_i+1 - z_i) / tai_i)
    #    # x = z' * tau_i * ........ = (z_i+1 - z_i) * ......
    #    derived_z_i = (z_func.calculate(t_range[i + 1]) - z_func.calculate(t_range[i])) / tau_i
#
    #    x_ans.append((z_func.calculate(t_range[i + 1]) - z_func.calculate(t_range[i])) * u_func.calculate(y_i) + x_i)
    #    y_ans.append(tau_i * f_func.calculate(t_range[i], x_i) + y_i)

    print_solution(x_ans, y_ans, t_range)
    c2 = numpy.abs(x_ans[-1] - s_func.calculate(T)) / s_func.calculate(T)

    class C1IntegrandOfIntegrand(base_function.BaseFunction):
        def __init__(self):
            super().__init__(None)
#
        def calculate(w):
            return w * p_func.calculate(w)
#
    c1_integral_of_integrand = integral_p.IntegralP(C1IntegrandOfIntegrand())
#
    class C1Integrand(base_function.BaseFunction):
        def __init__(self, integrand_of_integrand):
            super().__init__(integrand_of_integrand)
#
        def calculate(t):
            # x'(t)
            i = numpy.searchsorted(t_range, t)
            if t_range[i] < t or i == len(t_range) - 1:
                i -= 1
            derived_x = (x_ans[i + 1] - x_ans[i]) / (t_range[i + 1] - t_range[i])
            if t == t_range[i]:
                return derived_x * self.params.calculate(y_ans[i])
            return derived_x * self.params.calculate((y_ans[t] + y_ans[t + 1]) / 2)

    c1_integral = integral_p.IntegralP(C1Integrand(c1_integral_of_integrand))
    c1 =  1 - c1_integral.calculate(0) / (x_ans[-1] - x_ans[0])
    return c1, c2


def print_solution(x, y, t_range):
    with open("x_answer.txt", 'w') as output_file:
        for i in range(0, len(t_range)):
            output_file.write("{} {}\n".format(t_range[i], x[i]))
    with open("y_answer.txt", 'w') as output_file:
        for i in range(0, len(t_range)):
            output_file.write("{} {}\n".format(t_range[i], y[i]))

def solve_diff_equation(f, g, t, x_0, y_0):
    x = numpy.zeros(len(t))
    x[0] = x_0
    y = numpy.zeros(len(t))
    y[0] = y_0
    
    for i in range(0, len(t) - 1):
        tau = t[i + 1] - t[i]
        k1 = f(t[i], x[i], y[i]) * tau
        m1 = g(t[i], x[i], y[i]) * tau
        
        k2 = f(t[i] + tau / 2, x[i] + k1 / 2, y[i] + m1 / 2) * tau
        m2 = g(t[i] + tau / 2, x[i] + k1 / 2, y[i] + m1 / 2) * tau
        
        k3 = f(t[i] + tau / 2, x[i] + k2 / 2, y[i] + m2 / 2) * tau
        m3 = g(t[i] + tau / 2, x[i] + k2 / 2, y[i] + m2 / 2) * tau
        
        k4 = f(t[i] + tau, x[i] + k3, y[i] + m3) * tau
        m4 = g(t[i] + tau, x[i] + k3, y[i] + m3) * tau

        #print("k:", k1, k2, k3, k4)
        
        x[i + 1] = x[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        y[i + 1] = y[i] + (m1 + 2 * m2 + 2 * m3 + m4) / 6
    
    return x, y