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
fig.suptitle('板凳把手在不同时间点的速度矢量示意图', fontsize=16)
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
    head_line_speed = df['head_line_speed']
    tail_line_speed = df['tail_line_speed']
    
    # 绘制每个板凳的速度矢量
    for i in range(len(nodes)):
        # 计算速度矢量
        dx = tail_x[i] - head_x[i]
        dy = tail_y[i] - head_y[i]
        speed = (dx**2 + dy**2)**0.5
        if speed != 0:
            dx /= speed
            dy /= speed
        
        # 绘制速度矢量
        ax.quiver(head_x[i], head_y[i], dx * head_line_speed[i], dy * head_line_speed[i],
                  angles='xy', scale_units='xy', scale=1, color='black', width=0.005, headlength=4, headaxislength=3)

    # 设置标题和标签
    ax.set_title(f'时间 {time} 秒')
    ax.set_xlabel('X 位置 (米)')
    ax.set_ylabel('Y 位置 (米)')
    
    # 设置 x 和 y 轴等比例
    ax.set_aspect('equal')

# 显示图形
plt.show()
