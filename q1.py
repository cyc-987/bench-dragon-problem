import numpy as np
import matplotlib.pyplot as plt
import map
import boat

map1 = map.Map(0.55)
start_degree = 16*360
boat1 = boat.boat(start_degree, map1)
boat1.saveCurrentStatus("results/0.csv")

# 给出0 s、60 s、120 s、180 s、240 s、300 s
boat1.updateLocation(map1.move(start_degree, 60, -1))
boat1.saveCurrentStatus("results/60.csv")

boat1.updateLocation(map1.move(start_degree, 120, -1))
boat1.saveCurrentStatus("results/120.csv")

boat1.updateLocation(map1.move(start_degree, 180, -1))
boat1.saveCurrentStatus("results/180.csv")

boat1.updateLocation(map1.move(start_degree, 240, -1))
boat1.saveCurrentStatus("results/240.csv")

boat1.updateLocation(map1.move(start_degree, 300, -1))
boat1.saveCurrentStatus("results/300.csv")

# degree = np.linspace(0, 360*16, 5000)
# y = np.array([map1.angleToPos(i) for i in degree])

# fig, ax = plt.subplots()
# ax.grid(True)
# ax.plot(y.T[0], y.T[1])
# plt.show()