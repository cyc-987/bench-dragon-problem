import numpy as np
import matplotlib.pyplot as plt
import map
import boat
import tqdm

map1 = map.Map(0.55)
start_degree = 16*360
boat1 = boat.boat(start_degree, map1)

print(boat1.judgeHeadCollision_diatance())

numofpoints = 1500
end = 500
current_head_degree = start_degree
plus = end / numofpoints
x = np.linspace(0, end, numofpoints)
y = np.zeros(numofpoints)

for i in tqdm.tqdm(range(numofpoints)):
    y[i] = boat1.judgeHeadCollision_diatance() - 0.15
    if y[i] < 0:
        break
    boat1.updateLocation(map1.move(current_head_degree, plus, -1))
    current_head_degree = boat1.board[0].head_degree
    

fig, ax = plt.subplots()
ax.grid(True)
ax.plot(x, y)
plt.show()