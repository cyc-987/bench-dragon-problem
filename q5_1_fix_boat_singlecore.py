import numpy as np
import matplotlib.pyplot as plt
import q4_module
import map
import tqdm

refMap = map.Map(1.7)
map1 = q4_module.Map_dist(refMap)
boat1 = q4_module.boat(map1)

def find_max_speed(dist):
    boat1.updateLocation(dist)
    # return boat1.findMaxLineSpeed()
    return boat1.board[15].head_line_speed


distances = np.linspace(0, 50, 500)

max_speeds = np.array([find_max_speed(dist) for dist in tqdm.tqdm(distances, ncols=100)])

np.save('q5_data/0_50_board15_head.npy', [distances, max_speeds])

# Plot the results
fig, ax = plt.subplots()
ax.grid(True)
ax.plot(distances, max_speeds)
plt.show()