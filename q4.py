import numpy as np
import matplotlib.pyplot as plt
import q4_module
import map

refMap = map.Map(1.7)
map1 = q4_module.Map_dist(refMap)
boat1 = q4_module.boat(map1)
boat1.saveResult("results/q4_0.csv")

boat1.updateLocation(-100)
boat1.saveResult("results/q4_-100.csv")

boat1.updateLocation(-50)
boat1.saveResult("results/q4_-50.csv")

boat1.updateLocation(50)
boat1.saveResult("results/q4_50.csv")

boat1.updateLocation(100)
boat1.saveResult("results/q4_100.csv")