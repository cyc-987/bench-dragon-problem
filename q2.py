import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import map
import boat
import tqdm
import pandas as pd

# syk
from matplotlib import rcParams

# 配置
config = {
    "font.family": ['Times New Roman', 'STZhongsong'],
    "font.size": 12,
    "mathtext.fontset": 'stix',
    'axes.unicode_minus': False
}
rcParams.update(config)
# syk

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
# 画图
collision_point_x = x[i] + bias_dist
collision_point_y = y[i]

fig, ax = plt.subplots(figsize=(12, 12))  # 设置窗口大小
ax.plot(x, y, label='检测函数值', color='black')
ax.axhline(y=0, color='black', linestyle='--')  # 添加y=0的水平线，方便观察碰撞位置
ax.plot(collision_point_x, collision_point_y, 'ro', markersize=10, label=f'检测到碰撞')

# 设置标题和标签
ax.set_title('二分法计算碰撞检测函数值迭代图像')
ax.set_xlabel('龙头前把手前进距离 (米)')
ax.set_ylabel('检测函数值')
ax.legend()
ax.grid(True)
plt.show()
# 输出碰撞的具体参数
print(f"碰撞发生点的前进距离: {collision_point_x:.6f} 米")
print(f"碰撞点的检测函数值: {collision_point_y:.2f}")

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