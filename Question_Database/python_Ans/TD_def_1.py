# TD_def_1.py  — 正確答案
import sys

data = sys.stdin.read().strip()
if data == "":
    # 沒輸入就不印東西（或根據題目決定）
    pass
else:
    n = int(data)
    print(n * n)
