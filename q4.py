import numpy as np
import matplotlib.pyplot as plt
import q4_module
import map

refMap = map.Map(1.7)
map1 = q4_module.Map_dist(refMap)
boat1 = q4_module.boat(map1)