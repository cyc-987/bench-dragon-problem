import numpy as np
from scipy.optimize import brentq, brenth

# 创建等距螺线类
class Map:
    '''
    interval: 等距螺线的间隔，单位为m
    '''
    def __init__(self, interval): # interval为等距螺线的间隔，单位为m
        self.interval = interval
        self.scale = interval/360.0 
        self.interval = interval
        
    def angleToPos(self, angle):
        '''
        角度坐标到直角坐标的转换
        angle: 角度，单位为度
        '''
        netAngle = angle % 360
        assert netAngle >= 0 and netAngle < 360
        
        r = self.scale * angle
        x = r * np.cos(np.radians(netAngle))
        y = r * np.sin(np.radians(netAngle))
        
        return np.array([x, y])
    
    def angleToR(self, angle):
        '''
        角度坐标转换为距离原点距离
        angle: 角度，单位为度
        '''
        return self.interval * angle / 360.0
    
    def findAngle(self, angle, len, direction):
        '''
        寻找下一个点的角度
        angle: 角度，单位为度
        len: 距离，单位为m
        direction: 方向，1为逆时针方向，-1为顺时针方向
        '''
        location_origin = self.angleToPos(angle)
        a = location_origin[0]
        b = location_origin[1]
        
        def f(x):
            location = self.angleToPos(x)
            return (location[0] - a)**2 + (location[1] - b)**2 - len**2
        
        compare = -1
        for i in range(0, 360):
            if f(angle + direction*i) * compare < 0:
                break
        assert i < 359 and i != 0
        
        return brentq(f, angle, angle+direction*i, xtol=1e-6)
    
    def findCutAngle(self, angle):
        '''
        寻找该点切线的角度
        angle: 角度，单位为度
        '''
        # def x_func(a):
        #     return self.angleToPos(a)[0]
        
        # def y_func(a):
        #     return self.angleToPos(a)[1]
        
        # dx_da = derivative(x_func, angle, dx=1e-6)
        # dy_da = derivative(y_func, angle, dx=1e-6)
        
        # tangent_angle = np.degrees(np.arctan2(dy_da, dx_da))
        angle = np.radians(angle)
        
        tangent_angle_1 = np.sin(angle) + np.cos(angle) * angle
        tangent_angle_2 = np.cos(angle) - np.sin(angle) * angle
        tangent_angle = np.degrees(np.arctan2(tangent_angle_1, tangent_angle_2))
        
        return tangent_angle
    
    def curveLength(self, start_angle, end_angle):
        '''
        计算曲线长度
        start_angle: 起始角度，单位为度
        end_angle: 结束角度，单位为度
        '''
        start_angle = np.radians(start_angle)
        end_angle = np.radians(end_angle)
        
        def totalIntegral(a):
            return (self.scale*360/(4*np.pi)) * (a*np.sqrt(1+a**2) + np.log(a + np.sqrt(1+a**2)))
        
        return abs(totalIntegral(end_angle) - totalIntegral(start_angle))
    
    def move(self, start_angle, distance, direction):
        '''
        start_angle: 起始角度，单位为度
        distance: 距离，单位为m
        direction: 方向，1为逆时针方向，-1为顺时针方向
        '''
        location_origin = self.angleToPos(start_angle)
        a = location_origin[0]
        b = location_origin[1]
        
        def f(x):
            return self.curveLength(start_angle, x) - distance
        
        compare = -1
        for i in range(0, int(start_angle)+361):
            if f(start_angle + direction*i) * compare < 0:
                break
        if i == int(start_angle)+360 or i == 0:
            print("Warning: move may fail")
            # return start_angle
        
        return brentq(f, start_angle, start_angle+direction*i, xtol=1e-6) 
        