import this
import math
import numexpr as ne
import numpy as np
import pandas as pd
from pylab import mpl, plt
from timeit import timeit

# 유러피안 콜 옵션의 몬테카를로 가격결정
np.random.seed(1000)

S0 = 100
K = 105
T = 1.0
r = 0.05
sigma = 0.2

I = 10_000
# 10,000개의 표준정규분포 난수 벡터
z = np.random.standard_normal(I)
ST = S0 * np.exp((r - sigma**2 / 2) * T + sigma * np.sqrt(T) * z)
# 10,000개의 벡터 원소들을 각각 K를 빼고 0보다 큰지 보고, 작으면 0으로 채운 벡터
hT = np.maximum(ST - K, 0)
C0 = math.exp(-r * T) * np.mean(hT)
print("Value of the European call option %5.3f." % C0)

# 효율성
print(plt.style.available)
plt.style.use("seaborn-v0_8")
mpl.rcParams["font.family"] = "serif"
data = pd.read_csv("data/tr_eikon_eod_data.csv", index_col=0, parse_dates=True)
data = pd.DataFrame(data[".SPX"])
data.dropna(inplace=True)
print(data.info())
data["rets"] = np.log(data / data.shift(1))
data["vola"] = data["rets"].rolling(252).std() * np.sqrt(252)
data[[".SPX", "vola"]].plot(subplots=True, figsize=(10, 6))
# plt.show()

# 고성능
loops = 250_000
a = range(1, loops)


def f(x):
    return 3 * math.log(x) + math.cos(x) ** 2


print(timeit(lambda: [f(x) for x in a], number=1))

# 넘파이로
a = np.arange(1, loops)
print(timeit(lambda: 3 * np.log(a) + np.cos(a) ** 2, number=1))

# 더...numexpr
ne.set_num_threads(1)
f = "3 * log(a) + cos(a) ** 2"
print(timeit(lambda: ne.evaluate(f), number=1))
ne.set_num_threads(4)
print(timeit(lambda: ne.evaluate(f), number=1))
