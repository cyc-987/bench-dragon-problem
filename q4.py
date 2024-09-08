import numpy as np
import matplotlib.pyplot as plt
import q4_module
import map
import tqdm
import pandas as pd

refMap = map.Map(1.7)
map1 = q4_module.Map_dist(refMap)
boat1 = q4_module.boat(map1)
boat1.saveResult("results/q4_0.csv")

result = np.zeros((448, 201))
speed = np.zeros((224, 201))

for i in tqdm.tqdm(range(-100, 101), desc="Processing", ncols=100):
    boat1.updateLocation(i)
    result[:, i+100] = boat1.outputFormatPosition()
    speed[:, i+100] = boat1.outputFormatSpeed()
    

data_pd = pd.DataFrame(result)
data_pd2 = pd.DataFrame(speed)

data_pd.to_excel('Excel_output/q4_pos.xlsx', float_format="%.6f")
data_pd2.to_excel('Excel_output/q4_speed.xlsx', float_format="%.6f")

# boat1.updateLocation(-100)
# boat1.saveResult("results/q4_-100.csv")

# boat1.updateLocation(-50)
# boat1.saveResult("results/q4_-50.csv")

# boat1.updateLocation(50)
# boat1.saveResult("results/q4_50.csv")

# boat1.updateLocation(100)
# boat1.saveResult("results/q4_100.csv")