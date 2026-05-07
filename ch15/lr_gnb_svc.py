import numpy as np
import pandas as pd
from pylab import plt, mpl
from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

mpl.rcParams["font.family"] = "Malgun Gothic"
mpl.rcParams["axes.unicode_minus"] = False
print(plt.style.available)
plt.style.use("seaborn-v0_8")


def highlight_max(s):
    is_max = s == s.max()
    return ["background-color: yellow" if v else "" for v in is_max]


def bt_freq_ll_ret(data, cols_bin, show_plot=False, show_info=False):
    grouped = data.groupby(cols_bin + ["direction"])
    if show_info:
        print(grouped.size())

    res = grouped["direction"].size().unstack(fill_value=0)
    res.style.apply(highlight_max, axis=1)
    if show_info:
        print(res)

    data.dropna(inplace=True)

    # 회귀 예측 값들을 방향성으로 맞추고
    data["pos_freq"] = np.where(data[cols_bin].sum(axis=1) == 2, -1, 1)

    # 전략
    data["strat_freq"] = data["pos_freq"] * data["returns"]
    if show_info:
        print("전략별 수익률:")
        print(data[["returns", "strat_freq"]].cumsum().apply(np.exp))
        print("방향성 예측의 맞고 틀림:")
        print((data["direction"] == data["pos_freq"]).value_counts())
    if show_plot:
        data[["returns", "strat_freq"]].cumsum().apply(np.exp).plot(figsize=(10, 6))
        plt.show()
    return data


def create_bins(data, cols, bins, show_info=False):
    cols_bin = []
    for col in cols:
        col_bin = col + "_bin"
        # np.digitize: 정렬된 배열 받아서 bins에 지정된 값 들에서 끊어주기 위한 인덱스 배열을 반환...
        data[col_bin] = np.digitize(data[col], bins=bins)
        cols_bin.append(col_bin)
    if show_info:
        print("cols...", cols_bin + ["direction"])
        print(data[cols_bin + ["direction"]].head())
    return data, cols_bin


def prepare_data(filename, symbol, lags, bins=[0], show_plot=False, show_info=False):
    raw = pd.read_csv(filename, index_col=0, parse_dates=True).dropna()
    data = pd.DataFrame(raw[symbol])
    if show_plot:
        data.plot(figsize=(10, 6))
        plt.show()

    # 로그 수익률과 방향
    data["returns"] = np.log(data / data.shift(1))
    data.dropna(inplace=True)
    data["direction"] = np.sign(data["returns"]).astype(int)
    if show_info:
        print(data.head())
    if show_plot:
        data["returns"].hist(bins=35, figsize=(10, 6))
        plt.show()
    data, cols = create_lags(data, lags)
    return data, cols


def fit_models(data, cols_bin):
    mfit = {
        model: models[model].fit(data[cols_bin], data["direction"]) for model in models
    }
    return mfit


def create_lags(data, lags):
    cols = []
    for lag in range(1, lags + 1):
        col = f"lag_{lag}"
        data[col] = data["returns"].shift(lag)
        cols.append(col)
    return data, cols


def derive_positions(data, models):
    for model in models.keys():
        data[f"pos_{model}"] = models[model].predict(data[cols_bin])
    return data


def evaluate_strats(data, models):
    sel = []
    for model in models.keys():
        col = f"strat_{model}"
        data[col] = data[f"pos_{model}"] * data["returns"]
        sel.append(col)
    sel.insert(0, "returns")
    return sel


if __name__ == "__main__":
    # 책 예제 - 이것도 훈련 데이터에서는 500%까지도 갔는데, 시험 데이터에서는 망한다...
    filename = "data/tr_eikon_eod_data.csv"
    symbol = "EUR="
    # 비트코인 - 일단 세 가지가 1.173...lags 5에서는 svm 1.283까지...bins 바꾸니 svm이 1.887까지...이건 가능성이 있을라나?
    # 근데 훈련 데이터와 시험 데이터로 나눴더니 망했다...
    # filename = "data/btc_usdt_1m_cache.csv"
    # symbol = "close"

    # lags는 2개보다 5개를 사용하는게 더 나아지고...
    lags = 2
    lags = 5

    C = 1
    models = {
        "log_reg": linear_model.LogisticRegression(C=C),
        "gauss_nb": GaussianNB(),
        "svm": SVC(C=C),
    }

    data, cols = prepare_data(filename, symbol, lags)

    # 이게 기본 빈
    # bins = [0]
    # 평균과 표준편차로 만드는 빈 - 이게 성능이 더 좋다고...
    mu = data["returns"].mean()
    v = data["returns"].std()
    bins = [mu - v, mu, mu + v]
    data, cols_bin = create_bins(data, cols, bins)

    # 훈련데이터와 검증 데이터 나누기...
    split = int(len(data) * 0.5)
    train = data.iloc[:split].copy()
    test = data.iloc[split:].copy()
    # 이걸 무작위로 나누기? 시계열 자료인데 이게 말이 되나? 이건 아닌 듯...
    # 일단 이렇게 하면 로그 회귀가 그나마 높지만 망하긴 마찬가지...
    # train, test = train_test_split(data, test_size=0.5, shuffle=True, random_state=0)
    # train = train.copy().sort_index()
    # test = test.copy().sort_index()

    # 그래서 이 밑에서 적합만 train으로, 나머지는 다 test로 바뀐다...
    models = fit_models(train, cols_bin)
    test = derive_positions(test, models)
    sel = evaluate_strats(test, models)
    # 이건 앞 장에서 했던 빈도주의 방법인데...
    test = bt_freq_ll_ret(test, cols_bin)
    sel.insert(1, "strat_freq")
    print(test[sel].sum().apply(np.exp))
    test[sel].cumsum().apply(np.exp).plot(figsize=(10, 6))
    plt.show()
