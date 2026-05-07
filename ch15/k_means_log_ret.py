import numpy as np
import pandas as pd
from pylab import plt, mpl
from sklearn.cluster import KMeans

mpl.rcParams["font.family"] = "Malgun Gothic"
mpl.rcParams["axes.unicode_minus"] = False
print(plt.style.available)
plt.style.use("seaborn-v0_8")


def create_lags(data, lags):
    cols = []
    for lag in range(1, lags + 1):
        col = f"lag_{lag}"
        data[col] = data["returns"].shift(lag)
        cols.append(col)
    return data, cols


# 이전 날들(lags)의 수익을 가지고 다음날 수익을 예측하는 회귀 모형을 만들어서 백테스트...
def bt_k_means_ll_ret(filename, symbol, lags, show_plot=False, show_info=False):
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
    if show_info:
        print(data.head())
    data.dropna(inplace=True)
    # 이건 lags가 2라고 가정한 코드라...
    # if show_plot:
    #     data.plot.scatter(
    #         x="lag_1",
    #         y="lag_2",
    #         c="returns",
    #         cmap="coolwarm",
    #         figsize=(10, 6),
    #         colorbar=True,
    #     )
    #     plt.axvline(0, color="r", ls="--")
    #     plt.axhline(0, color="r", ls="--")
    #     plt.show()

    # 회귀
    model = KMeans(n_clusters=2, random_state=0)
    model.fit(data[cols])
    data["pos_clus"] = model.predict(data[cols])

    # 회귀 예측 값들을 방향성으로 맞추고
    data["pos_clus"] = np.where(data["pos_clus"] == 1, -1, 1)
    if show_info:
        print(data["pos_clus"].values)
    if show_plot:
        plt.figure(figsize=(10, 6))
        plt.scatter(
            data[cols].iloc[:, 0],
            data[cols].iloc[:, 1],
            c=data["pos_clus"],
            cmap="coolwarm",
        )
        plt.show()

    # 전략
    data["strat_clus"] = data["pos_clus"] * data["returns"]
    print("전략별 수익률:")
    print(data[["returns", "strat_clus"]].cumsum().apply(np.exp))
    print("방향성 예측의 맞고 틀림:")
    print((data["direction"] == data["pos_clus"]).value_counts())
    data[["returns", "strat_clus"]].cumsum().apply(np.exp).plot(figsize=(10, 6))
    plt.show()


if __name__ == "__main__":
    # 책 예제 - 이번엔 수익률이 15%로 적다...
    filename = "data/tr_eikon_eod_data.csv"
    symbol = "EUR="
    # 지연된 로그수익률
    lags = 2
    # more = True
    more = False
    # 비트코인 - 이건 2주동안 -...
    filename = "data/btc_usdt_1m_cache.csv"
    symbol = "close"
    bt_k_means_ll_ret(filename, symbol, lags, show_plot=more, show_info=more)

    # 이 전략을 사용하려면 아마도 다음과 같은 방식이어야 할 것이다...
    # 1. 매 시간 단위 close 쯤에서 정해진 시간 범위 내 과거 자료를 모은다.
    # 2. 위 방법으로 회귀 모델을 만들고 전략 비교를 해서 모델을 선택한다.
    # 3. 다음 날을 예측해서 현재와 포지션이 같다면 보유, 다르다면 청산하고 반대 방향으로 진입
    # 대충 6000번 정도 방향성이 바뀌니 평균 보유 시간 단위가 3 단위 정도 뿐이다...
    # 최소 시간 단위 아니면 사용하기 어려운 전략 같다...
