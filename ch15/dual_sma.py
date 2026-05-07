import numpy as np
import pandas as pd
from itertools import product
from pylab import mpl, plt

mpl.rcParams["font.family"] = "Malgun Gothic"
# matplotlib 그래프에서 마이너스 기호 깨지는 거 방지
mpl.rcParams["axes.unicode_minus"] = False
print(plt.style.available)
plt.style.use("seaborn-v0_8")


def test_log_return():
    # data: [100, 90, 100] -> shift: [Nan, 100, 90] -> 비교 [90, 100] / [100, 90]
    print(
        "하락 후 상승의 로그 수익률:", np.log(np.array([90, 100]) / np.array([100, 90]))
    )
    # 로그 수익률은 하락하면 음수, 상승하면 양수가 된다...
    # 여기에 포지션을 곱하면 롱과 숏 모두 수익률을 한 번에 계산 가능하다...
    # 상승했을 때 롱 포지션을 잡았다면 양수 x 양수 -> 양의 수익
    # 상승했을 때 숏 포지션을 잡았다면 양수 x 음수 -> 음의 손실
    # 하락했을 때 롱 포지션을 잡았다면 음수 x 양수 -> 음의 손실
    # 하락했을 때 숏 포지션을 잡았다면 음수 x 음수 -> 양의 수익


# 함수로 바꿔보자
def dual_SMA(csv, symbol, sma1, sma2, show_plot=False, show_info=False):
    with open(filename, "r") as f:
        raw = pd.read_csv(f, index_col=0, parse_dates=True)

    results = pd.DataFrame()
    for SMA1, SMA2 in product(sma1, sma2):
        data = pd.DataFrame(raw[symbol]).dropna()
        # 요약정보 info와 describe
        if show_info:
            print(data.info())
            print(data.describe())

        # 장단기 이동평균선
        data["SMA1"] = data[symbol].rolling(SMA1).mean()
        data["SMA2"] = data[symbol].rolling(SMA2).mean()
        if show_info:
            print(data[[symbol, "SMA1", "SMA2"]].tail())

        # 이동평균 매매전략 포지션
        data.dropna(inplace=True)
        data["positions"] = np.where(data["SMA1"] > data["SMA2"], 1, -1)

        # 로그 주가 수익률 - 전날과 오늘 주가 차이 비율을 로그로...오르면 양의 수익, 내리면 음의 수익
        data["returns"] = np.log(data[symbol] / data[symbol].shift(1))
        # 전략 포지션을 하루 늦추고 수익률을 곱하는게 미래 예측을 막는다...
        # 우선 수익이나 손실은 test_log_return() 주석 참고하고...
        # 종가를 보고 이동평균을 계산하는데, 그럼 그 날은 들어갈 수가 없다...
        # 따라서 포지션으로 먹거나 잃는 수익은 다음날 들어가서 얻을 수 있다.
        data["strategy"] = data["returns"] * data["positions"].shift(1)
        if show_info:
            print(data.round(4).head())
        data.dropna(inplace=True)
        # 이렇게 되면 실제 수익률이 된다는 건데...
        # 원래 복리 손익을 매일의 손익을 곱해야 한다.
        # 로그 손익을 sum하면 다 더한 값인데, logA + logB = logAB 이므로 이게 된다.
        # 여기에 exp 하면 log가 사라져서 AB만 남고, 이게 실제 수익률이다.
        # returns는 애플 주식을 그냥 들고 있었을 때, strategy는 이동평균에 따라 손익을 바꿨을 때...
        perf = np.exp(data[["returns", "strategy"]].sum())
        new_result = pd.DataFrame(
            {
                "SMA1": SMA1,
                "SMA2": SMA2,
                "MARKET": perf["returns"],
                "STRATEGY": perf["strategy"],
                "OUT": perf["strategy"] - perf["returns"],
            },
            index=[0],
        )
        results = pd.concat([results, new_result], ignore_index=True)

        # 그림 출력
        data[[symbol, "SMA1", "SMA2", "positions"]].plot(
            figsize=(10, 6), secondary_y="positions"
        )
        if show_plot:
            plt.show()

        ax = data[["returns", "strategy"]].cumsum().apply(np.exp).plot(figsize=(10, 6))
        data["positions"].plot(ax=ax, secondary_y="positions", style="--")
        ax.get_legend().set_bbox_to_anchor((0.25, 0.85))
        if show_plot:
            plt.show()

    if show_info:
        print(results.info())
    print(results.sort_values(by="OUT", ascending=False).round(4))


if __name__ == "__main__":
    # 책 예제----------------------------------------------
    # 데이터파일
    filename = "data/tr_eikon_eod_data.csv"
    # 종목 애플
    symbol = "AAPL.O"
    # 장단기 이동평균선
    SMA1 = [42]
    SMA2 = [252]
    more = False
    # 비트코인-----------------------------------------------
    # 데이터파일
    filename = "data/btc_usdt_1m_cache.csv"
    # 종목 애플
    symbol = "close"
    # 비트코인 1분 봉 2주간 테스트...아래 숫자가 제일 나은데...수수료 생각 안하고 7%? 안되겠다...
    SMA1 = [200, 400, 600]
    SMA2 = [800, 1000, 1200]

    # 백테스트
    dual_SMA(filename, symbol, SMA1, SMA2, show_plot=more, show_info=more)
