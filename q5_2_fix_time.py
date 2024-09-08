import numpy as np
import matplotlib.pyplot as plt
import q4_module
import map
from matplotlib import rcParams

# 配置
config = {
    "font.family": ['Times New Roman', 'STZhongsong'],
    "font.size": 12,
    "mathtext.fontset": 'stix',
    'axes.unicode_minus': False
}
rcParams.update(config)

# 初始化
refMap = map.Map(1.7)
map1 = q4_module.Map_dist(refMap)
boat1 = q4_module.boat(map1)

# 定义要绘制的时间点
time_points = [50]

# 循环绘制每个时间点的独立图形
for time in time_points:
    boat1.updateLocation(time)  # 更新船的位置
    y = np.zeros(223)  # 存储速度数据
    for i in range(223):
        y[i] = boat1.board[i].head_line_speed

    # Create a new figure for each time point
    fig, ax = plt.subplots(figsize=(8, 6))  # 设置图形大小
    bar_width = 0.7  # 柱子的宽度
    x = np.arange(223)  # X轴的板凳编号

    ax.bar(x, y, width=bar_width, color='black')  # 绘制柱状图
    ax.set_title(f'{time}秒时舞龙队所有板凳前把手的速度分布')  # 设置标题
    ax.set_xlabel('板凳编号')  # 设置X轴标签
    ax.set_ylabel('速度 (单位)')  # 设置Y轴标签
    ax.grid(True, which='both', linestyle='--', linewidth=0.7)  # 添加网格线

    # Display the plot
    plt.show()
