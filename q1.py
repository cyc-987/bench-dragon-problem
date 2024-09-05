import numpy as np
import matplotlib.pyplot as plt
import map
import boat

map1 = map.Map(0.55)
boat1 = boat.boat(16*360, map1)


# degree = np.linspace(0, 360*16, 5000)
# y = np.array([map1.angleToPos(i) for i in degree])

# fig, ax = plt.subplots()
# ax.grid(True)
# ax.plot(y.T[0], y.T[1])
# plt.show()