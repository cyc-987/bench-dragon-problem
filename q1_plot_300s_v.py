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

def plot_speed_vectors():
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
    
    # 绘制速度矢量
    for i in range(223):
        # 获取前把手的位置和速度
        head_position_degree = data.iloc[i]['head_degree']
        head_position = map1.angleToPos(head_position_degree)
        head_line_speed = data.iloc[i]['head_line_speed']
        
        # 计算切线方向
        tangent_angle = map1.findCutAngle(head_position_degree)
        # 切线方向是切线角度，顺时针方向要旋转180度
        tangent_angle_rad = np.radians(tangent_angle + 180)  # 顺时针方向
        
        # 计算速度矢量的终点
        scale = 1.0  # 可以调整这个缩放因子来改变矢量长度的显示比例
        dx = head_line_speed * np.cos(tangent_angle_rad) * scale
        dy = head_line_speed * np.sin(tangent_angle_rad) * scale
        end_position = [head_position[0] + dx, head_position[1] + dy]
        
        # 绘制速度矢量
        ax.arrow(head_position[0], head_position[1], 
                 dx, dy, 
                 head_width=0.2, head_length=0.4, 
                 fc='orange', ec='orange', 
                 linestyle='-', linewidth=2)
    
    # 设置图形标题和标签
    ax.set_title('300s舞龙队前把手速度矢量图')
    ax.set_xlabel('X 位置 (米)')
    ax.set_ylabel('Y 位置 (米)')
    
    # 确保x和y轴同比例
    ax.set_aspect('equal')
    
    # 显示图形
    plt.show()

if __name__ == "__main__":
    plot_speed_vectors()
