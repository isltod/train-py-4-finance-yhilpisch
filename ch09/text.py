import sqlite3 as sq3

path = "data/"
con = sq3.connect(path + "numbs.db")

# 테이블 생성
# query = "CREATE TABLE numbs (DATE date, NO1 real, NO2 real)"
# con.execute(query)
# con.commit()

# 테이블 메타 정보 보기
q = con.execute
print(q("SELECT * FROM sqlite_master WHERE type='table'").fetchall())

con.close()

import tables as tb
import datetime as dt

filename = path + "pytab.h5"
h5 = tb.open_file(filename, "w")
row_des = {
    "Date": tb.StringCol(26, pos=1),
    "Nol": tb.IntCol(pos=2),
    "No2": tb.IntCol(pos=3),
    "No3": tb.Float64Col(pos=4),
    "No4": tb.Float64Col(pos=5),
}
rows = 200000
filters = tb.Filters(complevel=0)
# tab = h5.create_table(
#     h5.root,
#     "ints_floats",
#     row_des,
#     title="Integers and Floats",
#     expectedrows=rows,
#     filters=filters,
# )
# print(type(tab))
# print(tab)

# pointer = tab.row
import numpy as np

ran_int = np.random.randint(0, 10000, size=(rows, 2))
ran_flo = np.random.standard_normal((rows, 2)).round(4)


import sys

sys.path.append(".")
from util import measure_time


# 이런 반복문 방식은 아주 느리고...
@measure_time
def f1(rows, ran_int, ran_flo, pointer, tab):
    for i in range(rows):
        pointer["Date"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pointer["Nol"] = ran_int[i, 0]
        pointer["No2"] = ran_int[i, 1]
        pointer["No3"] = ran_flo[i, 0]
        pointer["No4"] = ran_flo[i, 1]
        pointer.append()
    # tab.flush()


# f1(rows, ran_int, ran_flo, pointer, tab)

dty = np.dtype(
    [
        ("Date", "S26"),
        ("Nol", "<i4"),
        ("No2", "<i4"),
        ("No3", "<f8"),
        ("No4", "<f8"),
    ]
)
print(len(ran_int))
# 0 행렬을 만드는데, 컬럼을 dty에서 지정한 수와 형식대로 5개를...
sarray = np.zeros(len(ran_int), dtype=dty)
print(sarray[:4])


# 이렇게 넘파이로 다 만들고 한 방에 생성해야 빠르다...
@measure_time
def f2(rows, ran_int, ran_flo):
    sarray["Date"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sarray["Nol"] = ran_int[:, 0]
    sarray["No2"] = ran_int[:, 1]
    sarray["No3"] = ran_flo[:, 0]
    sarray["No4"] = ran_flo[:, 1]
    h5.create_table(
        "/",
        "ints_floats",
        sarray,
        title="Integers and Floats",
        expectedrows=rows,
        filters=filters,
    )


f2(rows, ran_int, ran_flo)


h5.close()
