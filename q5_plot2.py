import numpy as np
import matplotlib.pyplot as plt
import q4_module
import map
# from multiprocessing import Pool
from matplotlib import rcParams

# 配置
config = {
    "font.family": ['Times New Roman', 'STZhongsong'],
    "font.size": 12,
    "mathtext.fontset": 'stix',
    'axes.unicode_minus': False
}
rcParams.update(config)

refMap = map.Map(1.7)
map1 = q4_module.Map_dist(refMap)
boat1 = q4_module.boat(map1)

def find_max_speed(dist):
    if int(dist)%5 == 0:
        print(dist)
    boat1.updateLocation(dist)
    # return boat1.findMaxLineSpeed()
    return boat1.board[20].head_line_speed

def main():
    # try:
    data = np.load('q5_data/0_50_board15_head.npy', allow_pickle=True)
    [distances, max_speeds] = data
    # except:
        # distances = np.linspace(0, 50, 500)
        # with Pool() as pool:
        #     max_speeds = pool.map(find_max_speed, distances)
            
    max_speeds = np.array(max_speeds)
    # np.save('q5_data/0_50_board20_head_2.npy', [distances, max_speeds])

    # Plot the results
    fig, ax = plt.subplots(figsize=(8, 6)) # Set figure size: width=8 inches, height=6 inches
    ax.grid(True)
    ax.plot(distances, max_speeds, color='black')  # Set line color to black
    
    # Adding title and labels
    ax.set_title('0~50s内第15条龙身前把手的速度变化')
    ax.set_xlabel('时间 (秒)')
    ax.set_ylabel('速度 (单位)')
    
    # Optionally, you can set the limits for better visualization
    ax.set_xlim([0, 50])
    # ax.set_ylim([min(max_speeds), max(max_speeds)])  # Uncomment to set y-axis limits based on data

    plt.show()
    
if __name__ == '__main__':
    main()
