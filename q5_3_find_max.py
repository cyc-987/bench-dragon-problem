import numpy as np
import matplotlib.pyplot as plt
import q4_module
import map
from scipy.optimize import minimize

refMap = map.Map(1.7)
map1 = q4_module.Map_dist(refMap)
boat1 = q4_module.boat(map1)

def find_max_speed(dist):
    print("finding: ", dist)
    boat1.updateLocation(dist)
    return -boat1.findMaxLineSpeed()

result = minimize(find_max_speed, 14.3, bounds=[(14, 15)])
print(result)