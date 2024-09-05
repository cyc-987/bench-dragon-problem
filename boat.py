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
        
        
    def updateLocation(self, headangle):
        '''
        angle: 龙头角度位置，单位为度
        '''
        self.board[0].head_degree = headangle
        self.board[0].updateStatus()
        for i in range(1, 223):
            print(i-1)
            print(self.board[i-1].head_degree, self.board[i-1].tail_degree)
            print(self.board[i-1].head_line_speed, self.board[i-1].tail_line_speed)
            self.board[i].head_degree = self.board[i-1].tail_degree
            self.board[i].head_line_speed = self.board[i-1].tail_line_speed
            self.board[i].updateStatus()



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