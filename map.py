import numpy as np
from scipy.optimize import brentq
from scipy.misc import derivative
from scipy.integrate import quad

# 创建等距螺线类
class Map:
    '''
    interval: 等距螺线的间隔，单位为m
    '''
    def __init__(self, interval): # interval为等距螺线的间隔，单位为m
        self.interval = interval
        self.scale = interval/360.0 
        
    def angleToPos(self, angle):
        '''
        angle: 角度，单位为度
        '''
        netAngle = angle % 360
        assert netAngle >= 0 and netAngle < 360
        
        r = self.scale * angle
        x = r * np.cos(np.radians(netAngle))
        y = r * np.sin(np.radians(netAngle))
        
        return np.array([x, y])
    
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
        
        compare = f(angle)
        for i in range(0, 360):
            if f(angle + direction*i) * compare <= 0:
                break
        
        return brentq(f, angle, angle+direction*i, xtol=1e-6)
    
    def findCutAngle(self, angle):
        '''
        寻找该点切线的角度
        angle: 角度，单位为度
        '''
        def x_func(a):
            return self.angleToPos(a)[0]
        
        def y_func(a):
            return self.angleToPos(a)[1]
        
        dx_da = derivative(x_func, angle, dx=1e-6)
        dy_da = derivative(y_func, angle, dx=1e-6)
        
        tangent_angle = np.degrees(np.arctan2(dy_da, dx_da))
        
        return tangent_angle
    
    def curveLength(self, start_angle, end_angle):
        '''
        计算曲线长度
        start_angle: 起始角度，单位为度
        end_angle: 结束角度，单位为度
        '''
        def integrand(angle):
            def x_func(a):
                return self.angleToPos(a)[0]
            
            def y_func(a):
                return self.angleToPos(a)[1]
            
            dx_da = derivative(x_func, angle, dx=1e-6)
            dy_da = derivative(y_func, angle, dx=1e-6)
            
            return np.sqrt(dx_da**2 + dy_da**2)
        
        length, _ = quad(integrand, start_angle, end_angle)
        return abs(length)
    
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
        
        compare = f(start_angle)
        for i in range(0, start_angle):
            if f(start_angle + direction*i) * compare < 0:
                break
        
        return brentq(f, start_angle, start_angle+direction*i, xtol=1e-6) 
        