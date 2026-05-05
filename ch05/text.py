import numpy as np
import pandas as pd
from timeit import timeit

df = pd.DataFrame([10, 20, 30, 40], columns=["numbers"], index=["a", "b", "c", "d"])
print(df)
print(df.index)
print(df.columns)
print(df.values)
print(df.loc[["a", "d"]])
print(df.iloc[1:3])

# 근데 이게 넘파이와 비슷하다...
print(df.sum())
print(df.apply(lambda x: x**2))
print(df**2)

# 넘파이와 속도 비교
data = np.random.standard_normal((1000000, 2))
print("넘파이 배열 크기", data.nbytes)
df = pd.DataFrame(data, columns=["x", "y"])
print("판다스 데이터프레임 크기", df.info())

# 이게 젤 빠르다...
print("열 객체 더하기", timeit(lambda: df["x"] + df["y"], number=1))
print("판다스 sum", timeit(lambda: df.sum(axis=1), number=1))
# df.values가 ndarray를 반환...두 번째로 빠름...
print("ndarray sum", timeit(lambda: df.values.sum(axis=1), number=1))
print("넘파이 sum", timeit(lambda: np.sum(df, axis=1), number=1))
print("ndarray의 np.sum", timeit(lambda: np.sum(df.values, axis=1), number=1))
print("판다스 eval", timeit(lambda: df.eval("x + y"), number=1))
# 이건 말도 안되게 느리다...쓰지 말것!
print(
    "판다스 apply",
    timeit(lambda: df.apply(lambda x: x["x"] + x["y"], axis=1), number=1),
)
