import numpy as np
import pandas as pd
from pylab import mpl, plt

mpl.rcParams["font.family"] = "Malgun Gothic"
# matplotlib 그래프에서 마이너스 기호 깨지는 거 방지
mpl.rcParams["axes.unicode_minus"] = False
print(plt.style.available)
plt.style.use("seaborn-v0_8")

filename = "data/tr_eikon_eod_data.csv"
with open(filename, "r") as f:
    df = pd.read_csv(f, index_col=0, parse_dates=True)
# df.plot(figsize=(10, 6), subplots=True)
# plt.show()

# Reuters Instrument Code 확인
# instruments = [
#     "Apple Stock",
#     "Microsoft Stock",
#     "Intel Stock",
#     "Amazon Stock",
#     "Goldman Sachs Stock",
#     "SPDR S&P 500 ETF Trust",
#     "S&P 500 Index",
#     "VIX Volatility Index",
#     "EUR/USD Exchange Rate",
#     "Gold Price",
#     "VanEck Vectors Gold Miners ETF",
#     "SPDR Gold Trust",
# ]
# for ric, name in zip(df.columns, instruments):
#     print("{:8s} : {}".format(ric, name))

# # 요약정보 info와 describe
# print(df.info())
# print(df.describe())

# 로그 수익률
# rets = np.log(df / df.shift(1))
# print(rets.head().round(3))
# # 원래 apply는 엄청 느린데...이건 괜찮나? 벡터화해서?
# # rets.cumsum().apply(np.exp).plot(figsize=(10, 6))
# rets.cumsum().apply(np.exp).resample("1m", label="right").last().plot(figsize=(10, 6))
# plt.show()

# # 장단기 이동평균선
# sym = "AAPL.O"
# df.dropna(inplace=True)
# df["SMA1"] = df[sym].rolling(window=42).mean()
# df["SMA2"] = df[sym].rolling(window=252).mean()
# print(df[[sym, "SMA1", "SMA2"]].tail())
# df["positions"] = np.where(df["SMA1"] > df["SMA2"], 1, -1)
# df[[sym, "SMA1", "SMA2", "positions"]].plot(figsize=(10, 6), secondary_y="positions")
# plt.show()

# 상관관계 - 눈으로 보기엔 꽤 유의미한데 계수는 -0.576503밖에 안나온다...비선형이라서 그런가?
raw = pd.read_csv("data/tr_eikon_eod_data.csv", index_col=0, parse_dates=True)
data = raw[[".SPX", ".VIX"]].dropna()
print(data.corr())
# data.loc[:"2012-12-31"].plot(secondary_y=".VIX", figsize=(10, 6))
# plt.show()
# 로그 수익률과 선형회귀
rets = np.log(data / data.shift(1))
rets.dropna(inplace=True)
# rets.plot(subplots=True, figsize=(10, 6))
# pd.plotting.scatter_matrix(rets, alpha=0.2, diagonal="hist", hist_kwds={"bins": 35})
# reg = np.polyfit(rets[".SPX"], rets[".VIX"], deg=1)
# print(reg)
# ax = rets.plot(kind="scatter", x=".SPX", y=".VIX", figsize=(10, 6))
# ax.plot(rets[".SPX"], reg[0] * rets[".SPX"] + reg[1], "r", lw=2)
# plt.show()
# 원래 데이터 상관관계는 -5 정도인데, 단지 차분 값으로 나눴을 뿐인데 -0.804382까지 높아졌다?
print(rets.corr())
ax = rets[".SPX"].rolling(window=252).corr(rets[".VIX"]).plot(figsize=(10, 6))
ax.axhline(rets.corr().iloc[0, 1], color="r")
plt.show()
