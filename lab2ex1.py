import numpy as np
import time
import matplotlib.pyplot as plt
from numba import njit

def sum_cycle(x):
    sn = 0
    for i in range(1, x + 1):
        sn += ((-1)**(i + 1)) / (i * 2**i)
    return sn

def sum_vector(x):
    k = np.linspace(1, x, x)
    terms = ((-1)**(k + 1)) / (k * 2**k)
    return np.sum(terms)

@njit
def sum_numba_parallel(x):
    result = 0
    for i in range(1, x + 1):
        result += ((-1)**(i + 1)) / (i * np.exp2(i))
    return result

n = 1000

sttime1 = time.time()
result1 = sum_cycle(n)
edtime1 = time.time()
delta1 = edtime1 - sttime1

sttime2 = time.time()
result2 = sum_vector(n)
edtime2 = time.time()
delta2 = edtime2 - sttime2

sum_numba_parallel(10) # warm up

sttime3 = time.time()
result3 = sum_numba_parallel(n)
edtime3 = time.time()
delta3 = edtime3 - sttime3

print(delta1)
print(delta2)
print(delta3)
print(f'Vectorization time / Loop time for n = {n}: {delta2 / delta1}')
print(f'Numba time / Loop time for n = {n}: {delta3 / delta1}')

n_for_plot = np.arange(1, n + 1, 1)
snarray = [sum_vector(i) for i in n_for_plot]
plt.plot(n_for_plot, snarray, label='s(n)')
plt.hlines(np.log(1.5), xmin=0, xmax=n, linestyles='--', color='red', label='Log(1.5)')
plt.xlabel('n')
plt.ylabel('s(n)')
plt.legend()
plt.savefig('overleaf/67fe68e723632af9fad1411b/figures/lab2ex1.png')