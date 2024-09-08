import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 配置
config = {
    "font.family": ['Times New Roman', 'STZhongsong'],
    "font.size": 12,
    "mathtext.fontset": 'stix',
    'axes.unicode_minus': False
}
rcParams.update(config)

# 时间点和对应的文件路径
time_points = ['-100', '-50', '0', '50', '100']
file_paths = [f'results/q4_{time}.csv' for time in time_points]

# 创建绘图
fig, axs = plt.subplots(1, 5, figsize=(20, 4), sharex=True, sharey=True)
fig.suptitle('舞龙队在不同时间点的位置示意图', fontsize=16)
fig.subplots_adjust(wspace=0.2)

for ax, file_path, time in zip(axs, file_paths, time_points):
    # 读取CSV文件
    df = pd.read_csv(file_path)
    
    # 获取板凳的位置数据
    nodes = df['node']
    head_x = df['head_x']
    head_y = df['head_y']
    tail_x = df['tail_x']
    tail_y = df['tail_y']
    
    # 绘制每个板凳的前把手和后把手
    for i in range(len(nodes)):
        # 前把手
        ax.plot(head_x[i], head_y[i], 'o', color='black', markersize=2)
        # 后把手
        ax.plot(tail_x[i], tail_y[i], 'o', color='black', markersize=2)
        # 连线
        ax.plot([head_x[i], tail_x[i]], [head_y[i], tail_y[i]], '-', color='black', linewidth=1)
    
    # 设置标题和标签
    ax.set_title(f'时间为 {time} 秒')
    ax.set_xlabel('X 位置 (米)')
    ax.set_ylabel('Y 位置 (米)')
    
    # 设置 x 和 y 轴等比例
    ax.set_aspect('equal')

# 显示图形
plt.show()
