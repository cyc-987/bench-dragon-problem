import numpy as np
import map

class boat:
    '''
    板凳龙建模
    '''
    def __init__(self, initDegree, map1:map.Map):
        '''
        initDegree: 初始角度，单位为度
        map1: 地图对象
        '''
        self.head_degree = initDegree
        self.map = map1
        self.head_len = 2.86
        self.body_len = 1.65
        
        # 创建板凳实例
        self.board = [board(self.head_degree, map1, self.body_len) for _ in range(223)]
        self.board[0].length = self.head_len
        
        self.updateLocation(initDegree)
        self.saveCurrentStatus("initial.csv")
        
        
    def updateLocation(self, headangle):
        '''
        angle: 龙头角度位置，单位为度
        '''
        self.board[0].head_degree = headangle
        self.head_degree = headangle
        self.board[0].updateStatus()
        for i in range(1, 223):
            self.board[i].head_degree = self.board[i-1].tail_degree
            self.board[i].head_line_speed = self.board[i-1].tail_line_speed
            self.board[i].updateStatus()
    
    def saveCurrentStatus(self, filename):
        '''
        保存当前状态
        '''
        with open (filename, 'w') as f:
            f.write('node,head_degree,tail_degree,stick_degree,head_cut_degree,tail_cut_degree,stick_speed,head_line_speed,tail_line_speed\n')
            
            for i in range(223):
                f.write(str(i) + ',' +
                        str(self.board[i].head_degree) + ',' + 
                        str(self.board[i].tail_degree) + ',' + 
                        str(self.board[i].stick_degree) + ',' + 
                        str(self.board[i].head_cut_degree) + ',' + 
                        str(self.board[i].tail_cut_degree) + ',' + 
                        str(self.board[i].stick_speed) + ',' + 
                        str(self.board[i].head_line_speed) + ',' + 
                        str(self.board[i].tail_line_speed) + '\n')

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
            [head_x, head_y] = self.map.angleToPos(self.board[i].head_degree)
            result.append(head_x)
            result.append(head_y)
        [tail_x, tail_y] = self.map.angleToPos(self.board[222].tail_degree)
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
            
                
    # def judgeHeadCollision_diatance(self):
    #     '''
    #     判断是否发生头部碰撞
    #     返回值：distance
    #     '''
        
    #     # 计算顶角位置
    #     degree_fix = np.degrees(np.arctan2(0.15, 0.275))
    #     head_stick_degree = self.board[0].stick_degree
    #     head_position_degree = self.board[0].head_degree
    #     [head_position_x, head_position_y] = self.map.angleToPos(head_position_degree)
        
    #     l = np.sqrt(0.15**2 + 0.275**2)
    #     corner_position_x = head_position_x + np.cos(np.radians(head_stick_degree + degree_fix-180)) * l
    #     corner_position_y = head_position_y + np.sin(np.radians(head_stick_degree + degree_fix-180)) * l
    #     # print(head_position_x, head_position_y, corner_position_x, corner_position_y)
        
    #     # 寻找外圈的一个点
    #     for i in range(1, 223):
    #         if self.board[i].head_degree < (head_position_degree+360) and self.board[i].tail_degree > (head_position_degree+360):
    #             break
    #     # print(i)
        
    #     # 计算点到直线距离
    #     out_head_position_degree = self.board[i].head_degree
    #     out_tail_position_degree = self.board[i].tail_degree
    #     [out_head_position_x, out_head_position_y] = self.map.angleToPos(out_head_position_degree)
    #     [out_tail_position_x, out_tail_position_y] = self.map.angleToPos(out_tail_position_degree)
    #     # print(out_head_position_x, out_head_position_y, out_tail_position_x, out_tail_position_y)
        
    #     # 计算直线方程
    #     k = (out_tail_position_y - out_head_position_y) / (out_tail_position_x - out_head_position_x)
    #     b = out_head_position_y - k * out_head_position_x
        
    #     # 计算点到直线距离
    #     distance = abs(k * corner_position_x - corner_position_y + b) / np.sqrt(k**2 + 1)
    #     # print(distance)
        
    #     # 判断是否发生碰撞
    #     return distance

    def createCollisionDetectFunc(self, board_index, head_or_tail):
        '''
        判断是否发生头部碰撞
        board_index: 板凳索引
        head_or_tail: 头部或尾部, 0表示头部，1表示尾部
        返回值：distance
        '''
        
        def f():
            # 计算顶角位置
            degree_fix = np.degrees(np.arctan2(0.15, 0.275))
            head_stick_degree = self.board[board_index].stick_degree
            
            if head_or_tail == 0:
                head_position_degree = self.board[board_index].head_degree
            else:
                head_position_degree = self.board[board_index].tail_degree
            [head_position_x, head_position_y] = self.map.angleToPos(head_position_degree)
            
            l = np.sqrt(0.15**2 + 0.275**2)
            
            if head_or_tail == 0:
                corner_position_x = head_position_x + np.cos(np.radians(head_stick_degree + degree_fix-180)) * l
                corner_position_y = head_position_y + np.sin(np.radians(head_stick_degree + degree_fix-180)) * l
            else:
                corner_position_x = head_position_x + np.cos(np.radians(head_stick_degree - degree_fix)) * l
                corner_position_y = head_position_y + np.sin(np.radians(head_stick_degree - degree_fix)) * l
            
            # 寻找外圈的一个点
            for i in range(1, 223):
                if self.board[i].head_degree < (head_position_degree+360) and self.board[i].tail_degree > (head_position_degree+360):
                    break
            
            # 计算点到直线距离
            def dist(index):
                out_head_position_degree = self.board[index].head_degree
                out_tail_position_degree = self.board[index].tail_degree
                [out_head_position_x, out_head_position_y] = self.map.angleToPos(out_head_position_degree)
                [out_tail_position_x, out_tail_position_y] = self.map.angleToPos(out_tail_position_degree)
                
                # 计算直线方程
                k = (out_tail_position_y - out_head_position_y) / (out_tail_position_x - out_head_position_x)
                b = out_head_position_y - k * out_head_position_x
                
                # 计算点到直线距离
                distance = abs(k * corner_position_x - corner_position_y + b) / np.sqrt(k**2 + 1)
                return distance
            
            dist1 = dist(i)
            dist2 = dist(i-1)
            dist3 = dist(i+1)
            distance = min(dist1, dist2, dist3)
            
            # 判断是否发生碰撞
            return distance
        return f



class board:
    '''
    每一个板凳建模类
    '''
    def __init__(self, headDegree, map1:map.Map, length):
        '''
        headDegree: 初始头角度，单位为度
        map1: 地图对象
        length: 板凳长度，单位为m
        '''
        # location
        self.head_degree = headDegree
        self.tail_degree = headDegree
        
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
        self.updateTailDegree()
        self.calculateStickDegree()
        self.calculateCutDegree()
        self.calculateSpeed()
    
    def updateTailDegree(self):
        result = self.map.findAngle(self.head_degree, self.length, 1)
        self.tail_degree = result
        return result
    
    def calculateStickDegree(self):
        assert self.head_degree != self.tail_degree
        [head_x, head_y] = self.map.angleToPos(self.head_degree)
        [tail_x, tail_y] = self.map.angleToPos(self.tail_degree)
        
        stick_radians = np.arctan2(tail_y - head_y, tail_x - head_x)
        self.stick_degree = np.degrees(stick_radians)
        # print(self.stick_degree)
        
    def calculateCutDegree(self):
        self.head_cut_degree = self.map.findCutAngle(self.head_degree)
        self.tail_cut_degree = self.map.findCutAngle(self.tail_degree)
        # print(self.head_cut_degree, self.tail_cut_degree)
        
    def calculateSpeed(self):
        degree_head = self.stick_degree - self.head_cut_degree
        self.stick_speed = self.head_line_speed * abs(np.cos(np.radians(degree_head)))
        # print(self.stick_speed)
        
        degree_tail = self.stick_degree - self.tail_cut_degree
        self.tail_line_speed = self.stick_speed / abs(np.cos(np.radians(degree_tail)))
        # print(self.tail_line_speed)