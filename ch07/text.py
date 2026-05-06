import matplotlib.pyplot as plt
import numpy as np

y = np.random.standard_normal((20, 2)).cumsum(axis=0)
# fig = plt.figure(figsize=(10, 6))
# 이 명령과...
# plt.plot(y, lw=1.5)
# plt.plot(y, "ro")
# plt.grid(True)

# 이 명령의 차이는 x, y를 다 줬을 뿐인데...그럼 산점도가 되나?
# plt.plot(y[:, 0], y[:, 1], "ro")

# 근데 또 이렇게 x, y를 주면 선 차트...
# x = np.arange(len(y[:, 1]))
# print(x.shape)
# plt.plot(x, y[:, 0])
# plt.plot(x, y[:, 1])
# plt.legend(loc="best")

# 결국 x, y 이후에 "ro"만 줘서 그렇고, "ro--"만 해도 선이되니 헷갈린다.
# 그보다는 명시적으로 scatter 사용
# plt.scatter(y[:, 0], y[:, 1], marker="o")

c = np.random.randint(0, 10, len(y))
# c= 값으로 컬러 값을 주고, colorbar() 호출...
# plt.scatter(y[:, 0], y[:, 1], c=c, marker="o", cmap="coolwarm")
# plt.colorbar()


# 정적분
# def func(x):
#     return 0.5 * np.exp(x) + 1


# a, b = 0.5, 1.5
# # 0~2 숫자 50개(기본값) 배열 - 전체 범위
# x = np.linspace(0, 2)
# y = func(x)
# # 적분구간
# Ix = np.linspace(a, b)
# Iy = func(Ix)
# # (a,0)으로 시작해서 (b,0)으로 끝나는, 사이에 (Ix, Iy) 순서쌍들을 포함하는 리스트
# verts = [(a, 0)] + list(zip(Ix, Iy)) + [(b, 0)]

# from matplotlib.patches import Polygon

# fig, ax = plt.subplots(figsize=(10, 6))
# ax.plot(x, y, "b", linewidth=2)
# plt.ylim(bottom=0)
# # 적분 구간을 폴리곤으로 칠하고
# poly = Polygon(verts, facecolor="0.7", edgecolor="0.5")
# ax.add_patch(poly)
# # 적분식을 텍스트로...위치 ((a+b)/2, 1), 수식과 정렬 등...
# plt.text(
#     0.5 * (a + b),
#     1,
#     r"$\int_a^b f(x)\mathrm{d}x$",
#     horizontalalignment="center",
#     fontsize=20,
# )
# # 축 이름을...
# plt.figtext(0.9, 0.075, "$x$")
# plt.figtext(0.075, 0.9, "$f(x)$")
# ax.set_xticks((a, b))
# ax.set_xticklabels(("$a$", "$b$"))
# ax.set_yticks([func(a), func(b)])
# ax.set_yticklabels(("$f(a)$", "$f(b)$"))
# plt.grid(True)

# 이번엔 3차원
strike = np.linspace(50, 150, 24)
ttm = np.linspace(0.5, 2.5, 22)
# meshgrid라는게, x(m,), y(n,)을 받아서, x'(n,m), y'(n,m)을 반환하네...
# 그렇다는 건...x는 행으로 y개만큼 반복, y는 전치하고 열로 x개 만큼 반복한단 말이네...
strike, ttm = np.meshgrid(strike, ttm)
iv = (strike - 100) ** 2 / (100 * strike) / ttm

from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 6))
# 이건 옛날 코드...작동 안함...
# ax = fig.gca(projection="3d")
# 이걸로 대체...
ax = fig.add_subplot(projection="3d")
surf = ax.plot_surface(
    strike,
    ttm,
    iv,
    rstride=2,
    cstride=2,
    cmap=plt.cm.coolwarm,
    linewidth=0.5,
    antialiased=True,
)
ax.set_xlabel("strike")
ax.set_ylabel("time to maturity")
ax.set_zlabel("implied volatility")
fig.colorbar(surf, shrink=0.5, aspect=5)

# 이 명령은 마지막에 한 번
plt.show()
