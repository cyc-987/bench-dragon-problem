import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import map
import boat
import tqdm
import pandas as pd

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
for i in tqdm.tqdm(range(numofpoints), ncols=100):
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
    boat1.updateLocation(map1.move(start_degree, x[i], -1))
    current_head_degree = boat1.board[0].head_degree

boat1.saveCurrentStatus("results/q2.csv")
location_degree = x[i] + bias_dist

# 画图
print(location_degree)
fig, ax = plt.subplots()
ax.grid(True)
ax.plot(x, y)
plt.show()

# 保存结果
boat1.updateLocation(map1.move(start_degree, location_degree, -1))
result = np.zeros((224, 3))

pos = boat1.outputFormatPosition()
speed = boat1.outputFormatSpeed()

for i in range(224):
    result[i, 0] = pos[2*i]
    result[i, 1] = pos[2*i+1]
result[:, 2] = speed

data_pd = pd.DataFrame(result)
data_pd.to_excel('Excel_output/q2.xlsx', float_format="%.6f")