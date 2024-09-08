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

def plot_collision_positions():
    # 创建地图对象
    map1 = Map(0.55)
    
    # 读取碰撞时刻的结果数据
    filename = "results/q2.csv"
    data = pd.read_csv(filename)
    
    # 碰撞检测时的板凳编号和碰撞顶点信息
    collision_bench_index = 0  # 假设碰撞发生在板凳0 (可以根据实际情况调整)
    collision_head_position_degree = data.iloc[collision_bench_index]['head_degree']
    collision_tail_position_degree = data.iloc[collision_bench_index]['tail_degree']
    
    # 计算碰撞顶点位置
    collision_head_position = map1.angleToPos(collision_head_position_degree)
    collision_tail_position = map1.angleToPos(collision_tail_position_degree)

    # 创建图形，设置窗口大小
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.grid(True)
    
    # 绘制灰色螺线
    degree = np.linspace(0, 360 * 16, 5000)
    y = np.array([map1.angleToPos(i) for i in degree])
    ax.plot(y.T[0], y.T[1], 'gray', label='螺线路径')
    
    # 绘制每块板凳的前后把手位置，并连接
    for i in range(len(data)):
        head_position_degree = data.iloc[i]['head_degree']
        tail_position_degree = data.iloc[i]['tail_degree']
        
        # 计算前后把手的位置
        head_position = map1.angleToPos(head_position_degree)
        tail_position = map1.angleToPos(tail_position_degree)
        
        # 绘制前后把手位置
        ax.plot(head_position[0], head_position[1], 'o', color='orange')
        ax.plot(tail_position[0], tail_position[1], 'o', color='orange')
        
        # 连接前后把手
        ax.plot([head_position[0], tail_position[0]], 
                [head_position[1], tail_position[1]], 
                color='orange', linestyle='-', linewidth=3)
        
        # 标注第0和第8块板凳的编号
        if i == 0 or i == 8:
            ax.text(head_position[0], head_position[1] - 0.1, f'{i}', color='black', fontsize=20, 
                    verticalalignment='top', horizontalalignment='center')

    # 计算碰撞顶点位置并标注
    collision_head_position_offset = [
        collision_head_position[0] + 0.25,
        collision_head_position[1] + 0.16
    ]
    ax.plot(collision_head_position_offset[0], collision_head_position_offset[1], 'x', color='red', markersize=14, markeredgewidth=3 ,label='碰撞顶点')
    
    # 设置图形标题和标签
    ax.set_title('问题二碰撞时舞龙队位置示意图')
    ax.set_xlabel('X 位置 (米)')
    ax.set_ylabel('Y 位置 (米)')
    
    # 确保x和y轴同比例
    ax.set_aspect('equal')
    
    # 添加图例
    ax.legend()
    
    # 显示图形
    plt.show()
    
    # 输出碰撞的具体参数
    print("碰撞发生在板凳编号:", collision_bench_index)
    print("碰撞顶点（前把手）位置: X =", collision_head_position_offset[0], ", Y =", collision_head_position_offset[1])
    print("碰撞时龙头的角度:", collision_head_position_degree)
    print("碰撞时龙尾的角度:", collision_tail_position_degree)

if __name__ == "__main__":
    plot_collision_positions()
