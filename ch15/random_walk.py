import numpy as np
from pylab import plt, mpl
import pandas as pd

symbol = ".SPX"
filename = "data/tr_eikon_eod_data.csv"
raw = pd.read_csv(filename, index_col=0, parse_dates=True)
data = pd.DataFrame(raw[symbol])
lags = 5
cols = []
for lag in range(1, lags + 1):
    col = f"lag_{lag}"
    data[col] = data[symbol].shift(lag)
    cols.append(col)
print(data[cols + [symbol]].head(10))
print(data[cols + [symbol]].tail(10))

# 5개 변수 1차 선형 회귀
data.dropna(inplace=True)
reg = np.linalg.lstsq(data[cols], data[symbol], rcond=-1)[0]
print(reg.round(3))
plt.figure(figsize=(10, 6))
# cols에 있는 컬럼 이름마다, 회귀 가중치 계산된 값 1개(1차 선형 회귀니까)를 연결해서 바 차트로...
plt.bar(cols, reg)
plt.show()
data["pred"] = np.dot(data[cols], reg)
data[["pred", symbol]].plot(figsize=(10, 6))
plt.show()
