import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brenth
import map
import boat

def optimize(scale):
    print("current scale:", scale)
    map1 = map.Map(scale)
    start_degree = 16*360
    boat1 = boat.boat(start_degree, map1)

    boat1.updateLocation(4.5/map1.scale)
    
    # 碰撞检测，合法性检测
    headCollectionDetect = boat1.createCollisionDetectFunc(0, 0)
    distance_collision = headCollectionDetect() - 0.15
    print("headCollectionDetect:", distance_collision+0.15)
    return distance_collision

boundary = brenth(optimize, 0.35, 0.45, rtol=8.88179e-16)
print(boundary)