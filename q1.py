import numpy as np
import matplotlib.pyplot as plt
import map
import boat
import tqdm
import pandas as pd

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

result = np.zeros((448, 301))
speed = np.zeros((224, 301))

for i in tqdm.tqdm(range(0, 301), desc="Processing", ncols=100):
    boat1.updateLocation(map1.move(start_degree, i, -1))
    result[:, i] = boat1.outputFormatPosition()
    speed[:, i] = boat1.outputFormatSpeed()
    

data_pd = pd.DataFrame(result)
data_pd2 = pd.DataFrame(speed)

data_pd.to_excel('Excel_output/q1.xlsx', float_format="%.6f")
data_pd2.to_excel('Excel_output/q1_speed.xlsx', float_format="%.6f")