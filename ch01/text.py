import this
import math
import numpy as np

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
