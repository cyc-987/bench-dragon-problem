import numpy as np
import matplotlib.pyplot as plt
import q4_module
import map

refMap = map.Map(1.7)
map1 = q4_module.Map_dist(refMap)
boat1 = q4_module.boat(map1)

boat1.updateLocation(50)
y = np.zeros(223)
for i in range(223):
    y[i] = boat1.board[i].head_line_speed
    
fig, ax = plt.subplots()
ax.grid(True)
ax.plot(y)
plt.show()