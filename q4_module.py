import numpy as np
from scipy.optimize import brentq
import map

# 用于q4&q5的分段曲线，使用距离为标定
class Map_dist:
    '''
    使用距离为标定的分段曲线，0为进入调头区间点
    '''
    def __init__(self, refMap:map.Map): # interval为等距螺线的间隔，单位为m
        self.interval = 1.7
        self.scale = self.interval/360.0
        self.refMap = refMap
        
        # 切点坐标
        self.Ax = -2.711855863706657
        self.Ay = -3.591077522761075
        self.Bx = -self.Ax
        self.By = -self.Ay
        
        # 底角与顶角
        self.base_angle_degree = 3.440778050098615
        self.summit_angle_degree = 180 - 2*self.base_angle_degree
        
        # 两圆半径
        self.r1 = 3.005417667789035
        self.r2 = 1.5027088338945176
        self.d1 = self.r1 * np.radians(self.summit_angle_degree)
        self.d2 = self.r2 * np.radians(self.summit_angle_degree)
        
        #两圆圆心坐标
        self.o1x = -0.7239015035743209
        self.o1y = -1.3578514104267826
        self.o2x = 1.717878683640489
        self.o2y = 2.3994644665939284
        
        # 频繁使用的中间变量
        self.so1_degree = 40.49960157951043
        self.so2_degree = 90 - (270 - self.so1_degree - self.summit_angle_degree)
        self.boundary_head_angle_degree = 952.9411764705882
        # 用于判断分界线
        self.boundary_12_pos = 0
        self.boundary_23_pos = self.d1
        self.boundary_34_pos = self.d1 + self.d2
        
    def distToPos(self, pos):
        '''
        距离坐标到直角坐标的转换
        pos: 距离，单位为m
        '''
        
        # 判断所处的曲线分段
        position_status = self.judgePosition(pos)
        angle = self.distToAngle(pos)
            
        # print("pos:", pos, "status:", position_status)
        
        if position_status == 1 or position_status == 4: # 螺线
            [x,y] = self.refMap.angleToPos(angle)
            if position_status == 4:
                x = -x
                y = -y
                
        elif position_status == 2: # 第一个圆
            x = self.o1x - self.r1 * np.sin(np.radians(angle + self.so1_degree))
            y = self.o1y - self.r1 * np.cos(np.radians(angle + self.so1_degree))
        elif position_status == 3: # 第二个圆
            x = self.o2x + self.r2 * np.sin(np.radians(angle - self.so2_degree))
            y = self.o2y - self.r2 * np.cos(np.radians(angle - self.so2_degree))
        
        return np.array([x, y])
    
    def judgePosition(self, pos):
        '''
        判断位置所在的曲线段
        pos: 位置，单位为m
        '''
        position_status = 1
        if pos < self.boundary_12_pos:
            position_status = 1
        elif pos < self.boundary_23_pos:
            position_status = 2
        elif pos < self.boundary_34_pos:
            position_status = 3
        else:
            position_status = 4
        return position_status
        
    def distToAngle(self, pos):
        '''
        距离坐标转换为角度坐标
        pos: 距离，单位为m
        '''
       # 判断所处的曲线分段
        position_status = self.judgePosition(pos)
        
        if position_status == 1 or position_status == 4: # 螺线
            # 寻找对应角度
            if position_status == 1:
                pos = -pos
            else:
                pos = pos - self.boundary_34_pos
            def f1(x):
                return self.refMap.curveLength(self.boundary_head_angle_degree, x) - pos
            
            i = 1
            while i < 6000:
                if f1(self.boundary_head_angle_degree + i) > 0:
                    break
                i += 30
            assert i < 5999 and i != 0
            
            angle = brentq(f1, self.boundary_head_angle_degree, self.boundary_head_angle_degree + i, xtol=1e-6) 
            
        elif position_status == 2: # 第一个圆
            pos = pos - self.boundary_12_pos
            angle = np.degrees(pos / self.r1)
            assert angle >= 0 and angle <= self.summit_angle_degree
        elif position_status == 3: # 第二个圆
            pos = pos - self.boundary_23_pos
            angle = np.degrees(pos / self.r2)
            assert angle >= 0 and angle <= self.summit_angle_degree
    
        return angle
    
    # def angleToR(self, angle, position_status: int=1):
    #     '''
    #     角度坐标转换为距离原点距离
    #     angle: 角度，单位为度
    #     '''
    #     if position_status == 1 or position_status == 4:
    #         return self.interval * angle / 360.0
    #     elif position_status == 2:
    #         return self.r1
    #     elif position_status == 3:
    #         return self.r2
    
    def findDist(self, pos, len, direction):
        '''
        寻找距离定长点的位置
        pos: 位置，单位为m
        len: 距离，单位为m
        direction: 方向，1为前进方向，-1为后退方向
        '''
    
        # 获取原始坐标
        location_origin = self.distToPos(pos)
        a = location_origin[0]
        b = location_origin[1]
        
        # 构造距离函数
        def f(x):
            location = self.distToPos(x)
            return (location[0] - a)**2 + (location[1] - b)**2 - len**2
        
        # 搜索
        i = 1
        while i < int(len*5)+1:
            if f(pos + direction*i) > 0:
                break
            i += 1
        assert i < int(len*5) and i != 0
        
        # 确定二分法边界范围
        
        result = brentq(f, pos, pos+direction*i, xtol=1e-6)
        return result
    
    def findCutAngle(self, pos):
        '''
        寻找该点切线的角度
        pos: 位置，单位为m
        '''
        position_status = self.judgePosition(pos)
        angle = self.distToAngle(pos)
        if position_status == 1 or position_status == 4:       
            angle = np.radians(angle)
            
            tangent_angle_1 = np.sin(angle) + np.cos(angle) * angle
            tangent_angle_2 = np.cos(angle) - np.sin(angle) * angle
            tangent_angle = np.degrees(np.arctan2(tangent_angle_1, tangent_angle_2))
        elif position_status == 2:
            tangent_angle = 180 - (self.so1_degree + angle)
        elif position_status == 3:
            tangent_angle = angle - self.so2_degree
        return tangent_angle
    
    def curveLength(self, start_pos, end_pos):
        '''
        计算曲线长度
        start_pos: 起始位置，单位为m
        end_pos: 终止位置，单位为m
        '''
        return abs(start_pos - end_pos)
    
    def move(self, start_pos, distance, direction):
        '''
        start_pos: 起始位置，单位为m
        distance: 距离，单位为m
        direction: 方向，1为前进方向，-1为后退方向
        '''
        return start_pos + direction * distance


class boat:
    '''
    板凳龙建模
    '''
    def __init__(self, map1:Map_dist):
        '''
        initDegree: 初始角度，单位为度
        map1: 地图对象
        '''
        self.head_pos = 0
        self.map = map1
        self.head_len = 2.86
        # self.head_len = 1.65
        self.body_len = 1.65
        
        # 创建板凳实例
        self.board = [board(self.head_pos, map1, self.body_len) for _ in range(223)]
        self.board[0].length = self.head_len
        
        self.updateLocation(0)
        self.saveCurrentStatus("initial_q4.csv")
        
        
    def updateLocation(self, head_pos):
        '''
        angle: 龙头角度位置，单位为度
        '''
        self.board[0].head_pos = head_pos
        self.head_pos = head_pos
        self.board[0].updateStatus()
        # print("test point")
        for i in range(1, 223):
            self.board[i].head_pos = self.board[i-1].tail_pos
            self.board[i].head_line_speed = self.board[i-1].tail_line_speed
            # print("processing", i)
            self.board[i].updateStatus()
    
    def saveCurrentStatus(self, filename):
        '''
        保存当前状态
        '''
        with open (filename, 'w') as f:
            f.write('node,head_pos,tail_pos,stick_degree,head_cut_degree,tail_cut_degree,stick_speed,head_line_speed,tail_line_speed\n')
            
            for i in range(223):
                f.write(str(i) + ',' +
                        str(self.board[i].head_pos) + ',' + 
                        str(self.board[i].tail_pos) + ',' + 
                        str(self.board[i].stick_degree) + ',' + 
                        str(self.board[i].head_cut_degree) + ',' + 
                        str(self.board[i].tail_cut_degree) + ',' + 
                        str(self.board[i].stick_speed) + ',' + 
                        str(self.board[i].head_line_speed) + ',' + 
                        str(self.board[i].tail_line_speed) + '\n')
    def saveResult(self, filename):
        '''
        保存结果
        '''
        with open (filename, 'w') as f:
            f.write('node,head_x,head_y,tail_x,tail_y,stick_speed,head_line_speed,tail_line_speed\n')

            for i in range(223):
                [head_x, head_y] = self.map.distToPos(self.board[i].head_pos)
                [tail_x, tail_y] = self.map.distToPos(self.board[i].tail_pos)
                f.write(str(i) + ',' +
                        str(head_x) + ',' + 
                        str(head_y) + ',' + 
                        str(tail_x) + ',' + 
                        str(tail_y) + ',' + 
                        str(self.board[i].stick_speed) + ',' + 
                        str(self.board[i].head_line_speed) + ',' + 
                        str(self.board[i].tail_line_speed) + '\n')
    
    def findMaxLineSpeed(self):
        '''
        寻找最大线速度
        '''
        max_speed = 0
        for i in range(223):
            max_speed = max(max_speed, self.board[i].head_line_speed)
        max_speed = max(max_speed, self.board[222].tail_line_speed)
        return max_speed
    
    def outputFormatPosition(self):
        '''
        按题目要求输出
        返回列向量：
            龙头x (m)
            龙头y (m)
            第1节龙身x (m)
            第1节龙身y (m)
            ...
        '''
        result = []
        for i in range(223):
            [head_x, head_y] = self.map.distToPos(self.board[i].head_pos)
            result.append(head_x)
            result.append(head_y)
        [tail_x, tail_y] = self.map.distToPos(self.board[222].tail_pos)
        result.append(tail_x)
        result.append(tail_y)
        return np.array(result)
    def outputFormatSpeed(self):
        '''
        按题目要求输出
        返回列向量：
            龙头速度 (m/s)
            第1节龙身速度 (m/s)
            ...
        '''
        result = []
        for i in range(223):
            result.append(self.board[i].head_line_speed)
        result.append(self.board[222].tail_line_speed)
        return np.array(result)

class board:
    '''
    每一个板凳建模类
    '''
    def __init__(self, headPos, map1:Map_dist, length):
        '''
        headPos: 初始头位置，单位为米
        map1: 地图对象
        length: 板凳长度，单位为m
        '''
        # location
        self.head_pos = headPos
        self.tail_pos = headPos
        
        # speed
        self.head_line_speed = 1.0 
        self.tail_line_speed = 1.0
        self.stick_speed = 1.0
        self.map = map1
        
        # degree
        self.stick_degree = 0
        self.head_cut_degree = 0
        self.tail_cut_degree = 0
        
        # property
        self.length = length
        
    def updateStatus(self):
        self.updateTailPos()
        self.calculateStickDegree()
        self.calculateCutDegree()
        self.calculateSpeed()
    
    def updateTailPos(self):
        result = self.map.findDist(self.head_pos, self.length, -1)
        self.tail_pos = result
        return result
    
    def calculateStickDegree(self):
        assert self.head_pos != self.tail_pos
        [head_x, head_y] = self.map.distToPos(self.head_pos)
        [tail_x, tail_y] = self.map.distToPos(self.tail_pos)
        
        stick_radians = np.arctan2(tail_y - head_y, tail_x - head_x)
        self.stick_degree = np.degrees(stick_radians)
        
    def calculateCutDegree(self):
        self.head_cut_degree = self.map.findCutAngle(self.head_pos)
        self.tail_cut_degree = self.map.findCutAngle(self.tail_pos)
        # print(self.head_cut_degree, self.tail_cut_degree)
        
    def calculateSpeed(self):
        degree_head = self.stick_degree - self.head_cut_degree
        self.stick_speed = self.head_line_speed * abs(np.cos(np.radians(degree_head)))
        # print(self.stick_speed)
        
        degree_tail = self.stick_degree - self.tail_cut_degree
        self.tail_line_speed = self.stick_speed / abs(np.cos(np.radians(degree_tail)))
        # print(self.tail_line_speed)