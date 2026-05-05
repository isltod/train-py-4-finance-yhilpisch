import math
import numpy as np
from timeit import timeit

a = np.arange(8, dtype=np.float64)

# np 함수를 유니버설 함수라고 하는 모양...근데 math 함수가 더 빠르다...
print(timeit(lambda: np.sqrt(2.5), number=1000000))
print(timeit(lambda: math.sqrt(2.5), number=1000000))

# 대신 math 함수는 벡터 적용이 안되네...TypeError
# print(timeit(lambda: math.sqrt(a), number=1000000))
# 그래서 벡터에 적용할 때는 유니버설 함수가 더 빠르네...
print(timeit(lambda: np.sqrt(a), number=10000))
print(timeit(lambda: [math.sqrt(scalar) for scalar in a], number=10000))

# 구조화 넘파이 배열
dt = np.dtype(
    [("Name", "S10"), ("Age", "i4"), ("Height", "f8"), ("Children/Pets", "i4", 2)]
)
s = np.array([("Smith", 45, 1.83, (0, 1)), ("Jones", 53, 1.72, (2, 2))], dtype=dt)
# 뭔가 딕셔너리라기 보다는 테이블 같은 느낌이네...
print(s)
print(s["Name"])
print(s["Age"])
