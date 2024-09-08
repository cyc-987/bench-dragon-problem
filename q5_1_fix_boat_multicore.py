import numpy as np
import matplotlib.pyplot as plt
import q4_module
import map
from multiprocessing import Pool

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
    distances = np.linspace(0, 50, 500)

    with Pool() as pool:
        max_speeds = pool.map(find_max_speed, distances)

    max_speeds = np.array(max_speeds)
    np.save('q5_data/0_50_board20_head_2.npy', [distances, max_speeds])

    # Plot the results
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.plot(distances, max_speeds)
    plt.show()
    
if __name__ == '__main__':
    main()