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

def plot_boat_positions():
    # 创建地图对象
    map1 = Map(0.55)
    
    # 读取300秒的数据
    filename = "results/300.csv"
    data = pd.read_csv(filename)
    
    # 创建图形，设置窗口大小
    fig, ax = plt.subplots(figsize=(12, 12))  # 设置窗口大小
    ax.grid(True)
    
    # 绘制灰色螺线
    degree = np.linspace(0, 360 * 16, 5000)
    y = np.array([map1.angleToPos(i) for i in degree])
    ax.plot(y.T[0], y.T[1], 'gray', label='螺线路径')
    
    # 遍历所有板凳，绘制前后把手及其连线
    for i in range(223):
        # 获取每块板凳的前后把手位置
        head_position_degree = data.iloc[i]['head_degree']
        tail_position_degree = data.iloc[i]['tail_degree']
        head_position = map1.angleToPos(head_position_degree)
        tail_position = map1.angleToPos(tail_position_degree)
        
        # 绘制前后把手位置（橙色圆点）
        ax.plot(head_position[0], head_position[1], 'o', color='black', markersize=6)
        ax.plot(tail_position[0], tail_position[1], 'o', color='black', markersize=6)
        
        # 连接前后把手（橙色线条，粗细为3）
        ax.plot([head_position[0], tail_position[0]], 
                [head_position[1], tail_position[1]], 
                color='black', linestyle='-', linewidth=2)
    
    # 设置图形标题和标签
    ax.set_title('300s舞龙队位置示意图')
    ax.set_xlabel('X 位置 (米)')
    ax.set_ylabel('Y 位置 (米)')
    
    # 确保x和y轴同比例
    ax.set_aspect('equal')
    
    # 显示图形
    plt.show()

if __name__ == "__main__":
    plot_boat_positions()
