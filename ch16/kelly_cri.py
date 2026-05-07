import math
import time
import numpy as np
import pandas as pd
import datetime as dt
import cufflinks as cf
from pylab import plt, mpl

np.random.seed(100)

mpl.rcParams["font.family"] = "Malgun Gothic"
mpl.rcParams["axes.unicode_minus"] = False
print(plt.style.available)
plt.style.use("seaborn-v0_8")

# 이게 토이 케이스이고...
p = 0.55
f = p - (1 - p)
print(f)
I = 50
n = 100


def run_simulation(f):
    # 자금 변화 매트릭스...
    c = np.zeros((n, I))
    # 초기 자금, I번 시행하는 모든 경우에 1000으로 시작...
    c[0] = 100
    # 동전 던지기 n번을 I번 반복 시행?
    for i in range(I):
        for t in range(1, n):
            # 성공 확률 p를 1번 던지기...그 시행도 1번
            o = np.random.binomial(1, p)
            # 성공이란 말이겠지?
            if o > 0:
                # 바로 전 던지기에 성공이면 f 비율만큼 +, 실패면 그 비율만큼 -
                c[t, i] = c[t - 1, i] * (1 + f)
            else:
                # 이게 실패고...
                c[t, i] = c[t - 1, i] * (1 - f)
    return c


c_1 = run_simulation(f)
# print(c_1.round(2))
# plt.figure(figsize=(10, 6))
# plt.plot(c_1, "b", lw=0.5)
# plt.plot(c_1.mean(axis=1), "r", lw=2.5)
# plt.show()

# 주식 또는 지수에서 켈리 기준은...
raw = pd.read_csv("data/tr_eikon_eod_data.csv", index_col=0, parse_dates=True)
data = pd.DataFrame(raw[".SPX"])
data["returns"] = np.log(data / data.shift(1))
data.dropna(inplace=True)

# 이게 연율화된 평균과 표준편차라는 모양...
mu = data["returns"].mean() * 252
sigma = data["returns"].std() * 252**0.5

# 무위험 이자율...은행 이자는 없다...
r = 0.0

# 이게 최적 켈리 비율? 1보다 큰데? 레버리지 4,5란 얘긴가?
f = (mu - r) / sigma**2
print(f)

equs = []


def kelly_strategy(f):
    global equs
    equ = "equity_{:.2f}".format(f)
    equs.append(equ)
    cap = "capital_{:.2f}".format(f)
    # equity가 자본인 모양인데...cap은 뭐야 그럼...그냥 변수명인가?
    data[equ] = 1
    # f* 값을 자본에 곱했다...이게 뭘까 그럼...
    data[cap] = data[equ] * f
    for i, t in enumerate(data.index[1:]):
        # 이 루프는 1: 요소들에 대해서 돌고 있으니, i=0의 t가 원래는 1번 t였다...
        # 그런데 원래 데이터에서 i를 뽑으니 t_1은 0번부터 시작하는 t가 되고, 그래서 하루 전 날짜다...
        t_1 = data.index[i]
        # 다음날의 cap은 전날 cap * exp(log(수익률)) = cap * 수익률
        data.loc[t, cap] = data[cap].loc[t_1] * math.exp(data["returns"].loc[t])
        # 다음날 자기자본은 다음날 cap - 전날 cap + 전날 자기자본?
        data.loc[t, equ] = data[cap].loc[t] - data[cap].loc[t_1] + data[equ].loc[t_1]
        # 다음날 cap은 다음날 자기자본에 다시 켈리 기준 곱?
        # 이게 뭔가 왔다갔다 하면서 덮어쓰기 계산을 해서 못 알아먹겠네...
        data.loc[t, cap] = data[equ].loc[t] * f


# 못 알아먹겠고, 대충...f=4.47이고, 적정 레버리지 비율 정도라고 생각하고
# 레버리지 2.2 정도로 지수에 묻었으면 정도?
kelly_strategy(f * 0.5)
# 레버리지 3 정도로 지수에 묻었으면...
kelly_strategy(f * 0.66)
# 레버리지 4.5 정도로 지수에 묻었으면...
kelly_strategy(f)
# 그 결과를 비교하는건가?
print(data[equs].tail())
ax = data["returns"].cumsum().apply(np.exp).plot(figsize=(10, 6), legend=True)
data[equs].plot(ax=ax, legend=True)
plt.show()
