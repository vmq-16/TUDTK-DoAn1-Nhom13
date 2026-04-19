import random
import time
import matplotlib.pyplot as plt
import math

from part3.solvers import *

def generate_random_matrix(size):
    A = [[random.uniform(-1,1) for _ in range (size)] for _ in range(size)]

    for i in range(size):
        A[i][i] = sum(abs(A[i][j]) for j in range (size)) + 1

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

def matrix_vector_multiplication(A, x):
    n = len(A)
    result = [0.0] * n

    for i in range(n):
        for j in range(n):
            result[i] += A[i][j] * x[j]

    return result

def euclid_norm(v):
    return sum(x * x for x in v) ** 0.5

def residual_error(A, x, b):
    Ax = matrix_vector_multiplication(A, x)
    diff = [Ax[i] - b[i] for i in range(len(b))]
    return euclid_norm(diff) / euclid_norm(b)



sizes = [50, 100, 200, 500, 1000]
times_gauss = []
times_lu = []
times_gs = []
errors = []

for n in sizes:
    A = generate_random_matrix(n)
    b = generate_random_free_variable(n)

    t = measure_time(gauss_seidel, A, b) 
    times_gauss.append(t)

    x = gauss_seidel(A, b)
    err = residual_error(A, x, b)

    errors.append(err)


log_n = [math.log10(n) for n in sizes]
log_t = [math.log10(t) for t in times]

plt.plot(log_n, log_t, marker="o", label = "Measured")

C = times[0] / (sizes[0]**3)
theory = [C * (n**3) for n in sizes]
log_theory = [math.log10(t) for t in theory]

plt.plot(log_n, log_theory, linestyle="--", label = "O(n^3)")

plt.xlabel("log(n)")
plt.ylabel("log(time)")
plt.legend()
plt.title("Time Complexity Comparison")
plt.show()

