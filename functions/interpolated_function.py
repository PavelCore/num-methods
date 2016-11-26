import numpy as np
from bisect import bisect_left
from functions.base_function import BaseFunction

class InterpolatedFunction(base_function.BaseFunction):

    def __init__(self, tabulated_func_filename, points=None):
        params = self.calculate_interpolation_coeffs(tabulated_func_filename, points)
        super().__init__(params)

    def calculate_interpolation_coeffs(self, tabulated_func_filename, points=None):
        x = []
        f = []
        if points is not None:
            x = [point for point in points[0]]
            f = [point for point in points[1]]
        else:
            with open("tabulated_functions/" + tabulated_func_filename, 'r') as file:
                for line in file:
                    point = line.strip().split(' ')
                    x.append(float(point[0]))
                    f.append(float(point[1]))

        n = len(x) - 1
        A = np.zeros([n - 1, n - 1], dtype=type(1.0))
        h = [float(x[i] - x[i - 1]) for i in range(1, n + 1)]
        for i in range(0, n - 1):
            A[i][i] = 2 * (h[i] + h[i + 1])
        for i in range(1, n - 1):
            A[i][i - 1] = h[i]
            A[i - 1][i] = h[i]

        F = [6 * (((f[i + 1] - f[i]) / h[i]) - ((f[i] - f[i - 1]) / h[i - 1])) for i in range(1, n)]
        F = np.array(F, dtype=type(1.0))

        system_solution = self.solve_linear_system(A, F)
        self.a = f
        self.b = [0] * (n + 1)
        self.c = [0]
        self.d = [0] * (n + 1)
        for c_i in system_solution:
            self.c.append(c_i)
        self.c.append(0)

        for i in range(1, len(x)):
            self.d[i] = (self.c[i] - self.c[i - 1]) / h[i - 1]
            self.b[i] = h[i - 1] * (2.0 * self.c[i] + self.c[i - 1]) / 6.0 + (f[i] - f[i - 1]) / h[i - 1]
        self.x = x
        self.f = f
        return None

    def make_lup_decomposition(self, A):
        C = np.copy(A)
        P = np.zeros(A.shape)
        for i in range(0, A.shape[0]):
            P[i][i] = 1.0
        for i in range(0, A.shape[1]):
            max_row = -1
            max_row_val = 0.0
            for row in range(i, A.shape[0]):
                if np.abs(C[row][i]) > max_row_val:
                    max_row = row
                    max_row_val = C[row][i]
            
            if max_row_val == 0:
                return None
    
            temp_row = np.copy(C[i, :])
            C[i, :] = np.copy(C[max_row, :])
            C[max_row, :] = temp_row
            temp_row = np.copy(P[i, :])
            P[i, :] = np.copy(P[max_row, :])
            P[max_row, :] = temp_row
            
            for j in range(i + 1, A.shape[0]):
                C[j][i] /= C[i][i]
                for k in range(i + 1, A.shape[1]):
                    C[ j ][ k ] -= C[ j ][ i ] * C[ i ][ k ]
        
        L = np.zeros(A.shape)
        U = np.zeros(A.shape)
        for row in range(A.shape[0]):
            for col in range(A.shape[1]):
                if col >= row:
                    U[row][col] = C[row][col]
                if row == col:
                    L[row][col] = 1
                if col < row:
                    L[row][col] = C[row][col]
        
        return (L, U, P)

    def solve_linear_system(self, A, b):
        # Ax = b
        # PAx = Pb
        # LUx = Pb
        # Ly = Pb
        # Ux = y
        L, U, P = self.make_lup_decomposition(A)
        
        x = np.zeros(A.shape[1])
        y = np.zeros(A.shape[1])
        b = np.dot(P, b)
        
        # Ly = Pb
        for i in range(A.shape[0]):
            if i == 0:
                y[i] = b[i]
                continue
            temp_sum = sum(L[i][j] * y[j] for j in range(0, i))
            y[i] = b[i] - temp_sum
        
        for i in range(A.shape[0] - 1, -1, -1):
            if i == A.shape[0] - 1:
                x[i] = y[i] / U[i][i]
                continue
            temp_sum = sum(U[i][j] * x[j] for j in range(A.shape[0] - 1, i, -1))
            x[i] = (y[i] - temp_sum) / U[i][i]
        return x

    def calculate(self, x):
        distribution = self.x
        i = bisect_left(distribution, x)
        if i == len(distribution):
            return 0
        dx = x - self.x[i]
        return self.a[i] + self.b[i] * dx + self.c[i] * dx**2 / 2. + self.d[i] * dx**3 / 6.
