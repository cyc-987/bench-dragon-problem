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

def plot_dragon_velocity_vectors():
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
    
    # 读取和绘制每个时间点的龙头前把手速度矢量
    for time_point, color in zip(time_points, colors):
        filename = f"results/{time_point}.csv"
        data = pd.read_csv(filename)
        
        # 获取龙头前把手的位置和速度
        head_position_degree = data.iloc[0]['head_degree']
        head_cut_degree = data.iloc[0]['head_cut_degree']
        head_position = map1.angleToPos(head_position_degree)
        
        # 计算速度矢量
        head_velocity_direction = np.radians(head_cut_degree+ 180)

        # 增加速度矢量的长度
        speed_magnitude = 3.0  # 调整此值以改变矢量长度
        dx = speed_magnitude * np.cos(head_velocity_direction)
        dy = speed_magnitude * np.sin(head_velocity_direction)
        
        # 速度矢量的起点和终点
        start_point = head_position
        end_point = head_position + np.array([dx, dy])
        
        # 绘制速度矢量
        ax.quiver(start_point[0], start_point[1], dx, dy, angles='xy', scale_units='xy', scale=1, color=color, label=f'{time_point}s 速度矢量', width=0.005)
        
        # 绘制龙头把手的位置
        ax.plot(head_position[0], head_position[1], 'o', color=color)
    
    # 设置图形标题和标签
    ax.set_title('不同时间点的龙头前把手速度矢量图')
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
    plot_dragon_velocity_vectors()
