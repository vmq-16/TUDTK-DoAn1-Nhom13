import random
import time
import matplotlib.pyplot as plt
import math
import copy

from part1.gaussian import *
from part2.decomposition import *

from part3.solvers import *

def matrix_vector_multiplication(A, x):
    n = len(A)
    result = [0.0] * n

    for i in range(n):
        for j in range(n):
            result[i] += A[i][j] * x[j]

    return result

def svd_solver(A, b):
    U, S , V_T = svd_manual(A)

    U_T = transpose(U)
    y = matrix_vector_multiplication(U_T, b)

    z = []
    for i in range(len(y)):
        if S[i][i] > 1e-9:
            z.append(y[i] / S[i][i])
        else:
            z.append(0)
    
    V = transpose(V_T)
    x = matrix_vector_multiplication(V, z)

    return x

def gaussian_solver(A, b):
    _, x, _ = gaussian_elimination(A, b)
    return x

def generate_random_matrix(size):
    A = [[random.uniform(-1,1) for _ in range (size)] for _ in range(size)]

    for i in range(size):
        A[i][i] = sum(abs(A[i][j]) for j in range (size) if j != i) + 1

    return A

def generate_random_free_variable(size):
    return [random.uniform(-1,1) for _ in range(size)]

def measure_time(method, A, b, runs=5):
    total = 0

    for _ in range(runs):
        start = time.perf_counter()
        method(A, b)
        end = time.perf_counter()
        total += (end - start)

    return total / runs

def euclid_norm(v):
    return sum(x * x for x in v) ** 0.5

def residual_error(A, x, b):
    Ax = matrix_vector_multiplication(A, x)
    diff = [Ax[i] - b[i] for i in range(len(b))]
    return euclid_norm(diff) / euclid_norm(b)

def compute_error(method, A, b):
    x = method(copy.deepcopy(A), copy.deepcopy(b))

    if x is None:
        return float("inf")
    return residual_error(A, x, b)

sizes = [50, 100, 200, 500, 1000]
times_gauss = []
times_svd = []
times_gs = []
errors_gauss = []
errors_svd = []
errors_gs = []

for n in sizes:
    print(f"[Benchmark]: Running with matrix of size {n}")
    A = generate_random_matrix(n)
    b = generate_random_free_variable(n)

    times_gauss.append(measure_time(gaussian_elimination, copy.deepcopy(A), copy.deepcopy(b)))
    times_svd.append(measure_time(svd_solver, copy.deepcopy(A), copy.deepcopy(b)))
    times_gs.append(measure_time(gauss_seidel, copy.deepcopy(A), copy.deepcopy(b)))

    errors_gauss.append(compute_error(gaussian_solver, A, b))
    errors_svd.append(compute_error(svd_solver, A, b))
    errors_gs.append(compute_error(gauss_seidel, A, b))


log_n = [math.log10(n) for n in sizes]

log_gauss = [math.log10(t) for t in times_gauss]
log_svd = [math.log10(t) for t in times_svd]
log_gs = [math.log10(t) for t in times_gs]

plt.plot(log_n, log_gauss, marker="o", label = "Gaussian Elimination")
plt.plot(log_n, log_svd, marker="o", label = "SVD")
plt.plot(log_n, log_gs, marker="o", label = "Gauss-Seidel")

C = times_gauss[0] / (sizes[0]**3)
theory = [C * (n**3) for n in sizes]
log_theory = [math.log10(t) for t in theory]

plt.plot(log_n, log_theory, linestyle="--", label = "O(n^3)")

plt.xlabel("log(n)")
plt.ylabel("log(time)")
plt.legend()
plt.grid(True)
plt.title("Time Complexity Comparison")
plt.show()

