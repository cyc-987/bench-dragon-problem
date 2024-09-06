import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import map
import boat
import tqdm

map1 = map.Map(0.55)
start_degree = 16*360
boat1 = boat.boat(start_degree, map1)

# 从头部开始，逐渐增加角度，直到发生碰撞
numofpoints = 1500
end = 500
current_head_degree = start_degree
plus = end / numofpoints
x = np.linspace(0, end, numofpoints)
y = np.zeros(numofpoints)

# 生成碰撞检测函数，选定板子与头尾
headCollectionDetect = boat1.createCollisionDetectFunc(0, 0)

# 逐个点检测碰撞
for i in tqdm.tqdm(range(numofpoints)):
    y[i] = headCollectionDetect() - 0.15
    if y[i] < 0:
        # 监测到发生碰撞，使用二分法寻找精确碰撞点
        save_degree = current_head_degree
        # 二分法寻找碰撞点
        def f(x):
            if x < 0:
                boat1.updateLocation(map1.move(save_degree, -x, 1))
            else:
                boat1.updateLocation(map1.move(save_degree, x, -1))
            return headCollectionDetect() - 0.15
        bias_dist = brentq(f, -plus, 0, xtol=1e-6)
        break
    boat1.updateLocation(map1.move(current_head_degree, plus, -1))
    current_head_degree = boat1.board[0].head_degree

# 画图
print(x[i]+bias_dist)
fig, ax = plt.subplots()
ax.grid(True)
ax.plot(x, y)
plt.show()