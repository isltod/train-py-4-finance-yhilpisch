import numpy as np
from pylab import plt, mpl
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from lr_gnb_svc import prepare_data, create_bins
import time

mpl.rcParams["font.family"] = "Malgun Gothic"
mpl.rcParams["axes.unicode_minus"] = False
print(plt.style.available)
plt.style.use("seaborn-v0_8")

model = MLPClassifier(
    solver="lbfgs",
    alpha=1e-5,
    hidden_layer_sizes=3 * [500],
    random_state=1,
    max_iter=500,
)
# 책 예제 - 이것도 테스트 데이터를 나누니 간신히 5% 정도 수익?
filename = "data/tr_eikon_eod_data.csv"
symbol = "EUR="
# 비트코인 - 훈련 데이터와 시험 데이터로 나눴더니 1% 정도라...
filename = "data/btc_usdt_1m_cache.csv"
symbol = "close"

lags = 5
# lags = 2
data, cols = prepare_data(filename, symbol, lags)

mu = data["returns"].mean()
v = data["returns"].std()
bins = [mu - v, mu, mu + v]
# bins[0]
data, cols_bin = create_bins(data, cols, bins)

# 그냥하면 너무 말도 안되는 수익률(35배 이상)이 나온다...
# # 이걸 무작위로 나누기? 시계열 자료인데 이게 말이 되나? 이건 아닌 듯...
# train, test = train_test_split(data, test_size=0.5, random_state=100)
# train = train.copy().sort_index()
# test = test.copy().sort_index()
# 일단 이게 더 말이 되는거 같은데...
split = int(len(data) * 0.5)
train = data.iloc[:split].copy()
test = data.iloc[split:].copy()


print("start model fitting...")
start = time.time()
# 측정할 코드 - 대충 200 iter 기준으로 6초 정도인듯...
model.fit(train[cols_bin], train["direction"])
end = time.time()
print(f"{end - start:.5f} sec")
print(model)

test["pos_dnn_sk"] = model.predict(test[cols_bin])
test["strat_dnn_sk"] = test["pos_dnn_sk"] * test["returns"]
print(test[["returns", "strat_dnn_sk"]].sum().apply(np.exp))
test[["returns", "strat_dnn_sk"]].cumsum().apply(np.exp).plot(figsize=(10, 6))
plt.show()
