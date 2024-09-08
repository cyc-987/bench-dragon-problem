import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from map import Map
from matplotlib import rcParams

# 配置
config = {
    "font.family": ['Times New Roman', 'STZhongsong'],
    "font.size": 12,
    "mathtext.fontset": 'stix',
    'axes.unicode_minus': False
}
rcParams.update(config)

def plot_dragon_positions():
    # 创建地图对象
    map1 = Map(0.55)
    
    # 定义时间点和颜色
    time_points = ['0', '60', '120', '180', '240', '300']
    colors = plt.cm.plasma(np.linspace(0, 1, len(time_points)))
    
    # 创建图形，设置窗口大小
    fig, ax = plt.subplots(figsize=(12, 12))  # 设置窗口大小
    ax.grid(True)
    
    # 绘制灰色螺线
    degree = np.linspace(0, 360 * 16, 5000)
    y = np.array([map1.angleToPos(i) for i in degree])
    ax.plot(y.T[0], y.T[1], 'gray', label='螺线路径')
    
    # 读取和绘制每个时间点的龙头位置
    for time_point, color in zip(time_points, colors):
        filename = f"results/{time_point}.csv"
        data = pd.read_csv(filename)
        
        # 获取龙头的位置
        head_position_degree = data.iloc[0]['head_degree']
        tail_position_degree = data.iloc[0]['tail_degree']
        head_position = map1.angleToPos(head_position_degree)
        tail_position = map1.angleToPos(tail_position_degree)
        
        # 绘制龙头把手的位置
        ax.plot(head_position[0], head_position[1], 'o', color=color, label=f' {time_point}s 时龙头位置')
        ax.plot(tail_position[0], tail_position[1], 's', color=color)
        
        # 连接龙头前把手和后把手，并加粗连线
        ax.plot([head_position[0], tail_position[0]], 
                [head_position[1], tail_position[1]], 
                color=color, linestyle='-', linewidth=3)
    
    # 设置图形标题和标签
    ax.set_title('不同时间点的龙头位置示意图')
    ax.set_xlabel('X 位置 (米)')
    ax.set_ylabel('Y 位置 (米)')

    # 确保x和y轴同比例
    ax.set_aspect('equal')
    
    # 处理图例
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())
    
    # 显示图形
    plt.show()

if __name__ == "__main__":
    plot_dragon_positions()
