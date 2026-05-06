import random
import sys

sys.path.append("./")
from util import measure_time
from timeit import timeit


@measure_time
def average_py1(n):
    s = 0
    for i in range(1, n + 1):
        s += random.random()
    return s / n


def average_py2(n):
    s = 0
    for i in range(1, n + 1):
        s += random.random()
    return s / n


n = 10000000

# 그냥 파이썬 루프는 0.701417초, 0.6904087000002619, 0.8485384000086924
# average_py1(n)
# print(timeit(lambda: average_py2(n), number=1))
# print(timeit(lambda: sum(random.random() for _ in range(n)) / n, number=1))

# 넘파이 - 0.086545초, 0.08651910000480711, 0.09069339999405202
import numpy as np


@measure_time
def average_np1(n):
    s = np.random.random(n)
    return s.mean()


def average_np2(n):
    s = np.random.random(n)
    return s.mean()


# average_np1(n)
# print(timeit(lambda: average_np2(n), number=1))
# print(timeit(lambda: np.random.random(n).mean(), number=1))

# Numba라는...콜백 복잡해서 그냥 로컬만...0.09731700000702403 좀 느리고 두 번 돌려야 효과 있고...
import numba

average_nb2 = numba.jit(average_py2)
# print(timeit(lambda: average_nb2(n), number=1))
# print(timeit(lambda: average_nb2(n), number=1))

# Cython 버전은 너무 복잡해서 포기...
