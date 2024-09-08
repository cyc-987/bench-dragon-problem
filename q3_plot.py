import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brenth
import map
import boat
from matplotlib import rcParams

# 配置
config = {
    "font.family": ['Times New Roman', 'STZhongsong'],
    "font.size": 12,
    "mathtext.fontset": 'stix',
    'axes.unicode_minus': False
}
rcParams.update(config)

def optimize(scale):
    map1 = map.Map(scale)
    start_degree = 16 * 360
    boat1 = boat.boat(start_degree, map1)
    boat1.updateLocation(4.5 / map1.scale)
    
    # 碰撞检测，合法性检测
    headCollectionDetect = boat1.createCollisionDetectFunc(0, 0)
    distance_collision = headCollectionDetect() - 0.15
    return distance_collision

# 使用 brenth 找到边界值
boundary = brenth(optimize, 0.35, 0.45, rtol=8.88179e-16)

def plot_dragon_boundary(boundary):
    map1 = map.Map(boundary)
    start_degree = 16 * 360
    boat1 = boat.boat(start_degree, map1)
    
    # 设置窗口大小
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.grid(True)
    
    # 绘制灰色螺线
    degree = np.linspace(0, 360 * 16, 5000)
    y = np.array([map1.angleToPos(i) for i in degree])
    ax.plot(y.T[0], y.T[1], 'gray', label='螺线路径')
    
    # 绘制舞龙队的位置
    boat1.updateLocation(4.5 / map1.scale)
    for i in range(len(boat1.board)):
        head_position_degree = boat1.board[i].head_degree
        tail_position_degree = boat1.board[i].tail_degree
        head_position = map1.angleToPos(head_position_degree)
        tail_position = map1.angleToPos(tail_position_degree)
        
        # 绘制前后把手
        ax.plot(head_position[0], head_position[1], 'o', color='orange')
        ax.plot(tail_position[0], tail_position[1], 'o', color='orange')
        
        # 连接前后把手
        ax.plot([head_position[0], tail_position[0]], 
                [head_position[1], tail_position[1]], 
                color='orange', linestyle='-', linewidth=3)
    
    # 绘制调头区域的边界和填充
    collision_circle = plt.Circle((0, 0), 4.5, color='black', fill=False, linestyle='--', linewidth=2, label='调头区域边界')
    collision_circle_fill = plt.Circle((0, 0), 4.5, color='gold', alpha=0.3, label='调头区域内部')
    ax.add_patch(collision_circle_fill)
    ax.add_patch(collision_circle)
    
    # 设置图形标题和标签
    ax.set_title('舞龙队刚好进入调头区域的示意图')
    ax.set_xlabel('X 位置 (米)')
    ax.set_ylabel('Y 位置 (米)')
    
    # 确保 x 和 y 轴同比例
    ax.set_aspect('equal')
    
    # 添加图例
    ax.legend()
    
    # 显示图形
    plt.show()
    
    # 输出边界值
    print("调头区域边界的比例因子:", boundary)

if __name__ == "__main__":
    plot_dragon_boundary(boundary)
