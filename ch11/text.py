import numpy as np
from pylab import plt, mpl

print(plt.style.available)
plt.style.use("seaborn-v0_8")
mpl.rcParams["font.family"] = "Malgun Gothic"
mpl.rcParams["axes.unicode_minus"] = False


def create_plot(x, y, styles, labels, axlabels):
    plt.figure(figsize=(10, 6))
    for i in range(len(x)):
        plt.plot(x[i], y[i], styles[i], label=labels[i])
    plt.xlabel(axlabels[0])
    plt.ylabel(axlabels[1])
    plt.legend()
    plt.show()


def f(x):
    return np.sin(x) + 0.5 * x


x = np.linspace(-2 * np.pi, 2 * np.pi, 50)

# create_plot([x], [f(x)], ["b"], ["f(x)"], ["x", "f(x)"])

# deg=1 선형회귀는 사인 함수에 잘 맞지 않는다...대충 맞는데...
# res = np.polyfit(x, f(x), deg=1, full=True)
# deg=5 꽤 잘 맞는데...
# res = np.polyfit(x, f(x), deg=5, full=True)
# 7차 함수 회귀는 거의 붙어가는데도 np.allclose는 False네...
# res = np.polyfit(x, f(x), deg=7, full=True)
# print(res)
# ry = np.polyval(res[0], x)

# 이번에는 행렬 - 속도가 빠를지 모르겠지만 코드만 다르고 결과는 동일...
# matrix = np.zeros((3 + 1, len(x)))
# # matrix[3, :] = x**3
# # 최 고차를 sin 함수로 바꾸면 완전 좋아지네...
# matrix[3, :] = np.sin(x)
# matrix[2, :] = x**2
# matrix[1, :] = x
# matrix[0, :] = 1

# reg = np.linalg.lstsq(matrix.T, f(x), rcond=None)[0]
# print(reg.round(4))
# ry = np.dot(reg, matrix)

# 중간에 잡음이 끼면...
# xn = x + 0.15 * np.random.standard_normal(len(x))
# yn = f(xn) + 0.25 * np.random.standard_normal(len(x))
# reg = np.polyfit(xn, yn, deg=7, full=True)
# ry = np.polyval(reg[0], xn)

# 순서 없는 데이터는?
# xu = np.random.permutation(x)
# yu = f(xu)
# reg = np.polyfit(xu, yu, deg=5, full=True)
# ry = np.polyval(reg[0], xu)

# print(np.allclose(f(x), ry))
# print(np.mean((f(x) - ry) ** 2))
# create_plot([x, x], [f(x), ry], ["b", "r."], ["f(x)", "회귀직선"], ["x", "f(x)"])
# create_plot([x, x], [yn, ry], ["b", "r."], ["f(x)", "회귀직선"], ["x", "f(x)"])
# 순서없는 데이터는 scatter 해야 하므로 마커를 다 점 모양으로 바꾼다..
# create_plot([xu, xu], [yu, ry], ["b.", "ro"], ["f(x)", "회귀직선"], ["x", "f(x)"])


# 2차원 회귀
def fm(p):
    x, y = p
    return np.sin(x) + 0.5 * x + np.sqrt(y) + 0.05 * y**2


x = np.linspace(0, 10, 20)
y = np.linspace(0, 10, 20)
X, Y = np.meshgrid(x, y)
Z = fm((X, Y))
x = X.flatten()
y = Y.flatten()

from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection="3d")
# surf = ax.plot_surface(
#     X, Y, Z, rstride=2, cstride=2, linewidth=0.5, antialiased=True, cmap="coolwarm"
# )
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("f(x,y)")
# fig.colorbar(surf, shrink=0.5, aspect=5)
# plt.show()

matrix = np.zeros((len(x), 6 + 1))
matrix[:, 0] = 1
matrix[:, 1] = x
matrix[:, 2] = y
matrix[:, 3] = x**2
matrix[:, 4] = y**2
matrix[:, 5] = np.sin(x)
matrix[:, 6] = np.sqrt(y)

reg = np.linalg.lstsq(matrix, fm((x, y)), rcond=None)[0]
RZ = np.dot(matrix, reg).reshape((20, 20))

surf1 = ax.plot_surface(
    X,
    Y,
    Z,
    rstride=2,
    cstride=2,
    linewidth=0.5,
    antialiased=True,
    cmap="Greys",
)
surf2 = ax.plot_wireframe(X, Y, RZ, rstride=2, cstride=2, label="회귀")
ax.legend()
fig.colorbar(surf1, shrink=0.5, aspect=5)
plt.show()
