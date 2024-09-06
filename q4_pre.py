import numpy as np
import matplotlib.pyplot as plt
import map
import boat

map1 = map.Map(1.7)
start_degree = 16*360
boat1 = boat.boat(start_degree, map1)

boat1.updateLocation(4.5/map1.scale)
print("head_degree:", boat1.board[0].head_degree)
r = map1.angleToR(boat1.board[0].head_degree)
print("r:", r)
[x,y] = map1.angleToPos(boat1.board[0].head_degree)
print("x:", x, "y:", y)
boat1.saveCurrentStatus("q4_pre.csv")

v_cut_degree = abs(boat1.board[0].head_cut_degree)
print("v_cut_degree:", v_cut_degree)
cut_location_degree = np.degrees(np.arctan2(-y, -x))
print("cut_location_degree:", cut_location_degree)
base_angle_degree = cut_location_degree - (90 - v_cut_degree)
base_angle_rad = np.radians(base_angle_degree)
print("base_angle_degree:", base_angle_degree)
r1 = 3/np.cos((base_angle_rad))
r2 = r1/2
print("r1:", r1, "r2:", r2)

ax, ay = x, y
bx, by = -x, -y
px, py = x+2/3*(-2*x), y+2/3*(-2*y)

h1x, h1y = (px+ax)/2, (py+ay)/2
h2x, h2y = (px+bx)/2, (py+by)/2

o1x, o1y = h1x + r1*np.sin(base_angle_rad)*np.cos(base_angle_rad), h1y - r1*np.sin(base_angle_rad)*np.sin(base_angle_rad)
o2x, o2y = h2x - r2*np.sin(base_angle_rad)*np.cos(base_angle_rad), h2y + r2*np.sin(base_angle_rad)*np.sin(base_angle_rad)
print("o1x:", o1x, "o1y:", o1y)
print("o2x:", o2x, "o2y:", o2y) 