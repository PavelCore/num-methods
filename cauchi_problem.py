import numpy

def solve(x_0, y_0, beta, T, N,
          p_func, z_func, s_func, u_func, f_func):
    t_range = numpy.arange(0, T + T/N, T/N)
    x_ans = [x_0]
    y_ans = [y_0]

    for i in range(0, len(t_range) - 1):
        x_i = x_ans[-1]
        y_i = y_ans[-1]
        tau_i = t_range[i + 1] - t_range[i]
        # Unused here because of the precision
        # (z' = (z_i+1 - z_i) / tai_i)
        # x = z' * tau_i * ........ = (z_i+1 - z_i) * ......
        derived_z_i = (z_func.calculate(t_range[i + 1]) - z_func.calculate(t_range[i])) / tau_i

        x_ans.append((z_func.calculate(t_range[i + 1]) - z_func.calculate(t_range[i])) * u_func.calculate(y_i) + x_i)
        y_ans.append(tau_i * f_func.calculate(t_range[i], x_i) + y_i)

    print_solution(x_ans, y_ans, t_range)
    print("C2:", numpy.abs(x_ans[-1] - s_func.calculate(T)) / s_func.calculate(T))


def print_solution(x, y, t_range):
    with open("x_answer.txt", 'w') as output_file:
        for i in range(0, len(t_range)):
            output_file.write("{} {}\n".format(t_range[i], x[i]))
    with open("y_answer.txt", 'w') as output_file:
        for i in range(0, len(t_range)):
            output_file.write("{} {}\n".format(t_range[i], y[i]))