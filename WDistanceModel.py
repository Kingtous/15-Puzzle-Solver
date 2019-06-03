from queue import Queue as queue
from numba import jit
import numpy as np
import copy

'''
Author: Kingtous
Description: Walking Distance 步行距离计算
Date: 2019-06-03
'''

#===================横纵向可能出现的种类(模拟小型Pattern Database)====================#
a0 = ((0, 0, 0, 4), (0, 0, 1, 3), (0, 0, 2, 2), (0, 0, 3, 1), (0, 0, 4, 0),
      (0, 1, 0, 3), (0, 1, 1, 2), (0, 1, 2, 1), (0, 1, 3, 0), (0, 2, 0, 2), (0, 2, 1, 1), (0, 2, 2, 0),
      (0, 3, 0, 1), (0, 3, 1, 0), (0, 4, 0, 0), (1, 0, 0, 3), (1, 0, 1, 2), (1, 0, 2, 1), (1, 0, 3, 0),
      (1, 1, 0, 2), (1, 1, 1, 1), (1, 1, 2, 0), (1, 2, 0, 1), (1, 2, 1, 0), (1, 3, 0, 0), (2, 0, 0, 2),
      (2, 0, 1, 1), (2, 0, 2, 0), (2, 1, 0, 1), (2, 1, 1, 0), (2, 2, 0, 0), (3, 0, 0, 1), (3, 0, 1, 0),
      (3, 1, 0, 0), (4, 0, 0, 0))
b0 = ((0, 0, 0, 3), (0, 0, 1, 2), (0, 0, 2, 1), (0, 0, 3, 0), (0, 1, 0, 2),
      (0, 1, 1, 1), (0, 1, 2, 0), (0, 2, 0, 1), (0, 2, 1, 0), (0, 3, 0, 0), (1, 0, 0, 2), (1, 0, 1, 1),
      (1, 0, 2, 0), (1, 1, 0, 1), (1, 1, 1, 0), (1, 2, 0, 0), (2, 0, 0, 1), (2, 0, 1, 0), (2, 1, 0, 0),
      (3, 0, 0, 0))
#========================================================#

record = {}

class WalkingDistance:
    """
    Walking Distance类
    """
    @jit
    def __init__(self):
        self.indexChanger = [0 for i in range(5)]
        self.array = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.dict_a = dict()
        self.dict_b = dict()

    @jit
    def calcIndex(self):
        '''
        :return: record对应的下标
        '''
        ret = 0
        for i in range(4):
            ret = ret * 35 + self.indexChanger[i]
        return ret

    @jit
    def getIndex(self, x):
        '''
        :param x: 下标
        :return: 无，计算出index，放入indexChanger中
        '''
        for i in range(4):
            self.indexChanger[3 - i] = x % 35
            x = x // 35

    @jit
    def initCal(self):
        """
        :return: 无，用于初始化计算
        """
        for i in range(35):
            self.dict_a[(a0[i][0], a0[i][1], a0[i][2])] = i
        for i in range(20):
            self.dict_b[(b0[i][0], b0[i][1], b0[i][2])] = i
        q = queue()

        self.indexChanger[0], self.indexChanger[1] = self.dict_a[(4, 0, 0)], self.dict_a[(0, 4, 0)]
        self.indexChanger[2], self.indexChanger[3] = self.dict_a[(0, 0, 4)], self.dict_b[(0, 0, 0)]

        startValue = self.calcIndex()
        record[startValue] = 0
        q.put(startValue)

        while not q.empty():
            value = q.get()
            self.getIndex(value)
            num2 = [0, 0, 0, 0]
            for i in range(4):
                for j in range(4):
                    if i == 3:
                        self.array[i][j] = b0[self.indexChanger[i]][j]
                    else:
                        self.array[i][j] = a0[self.indexChanger[i]][j]
                    num2[j] = num2[j] + self.array[i][j]
            emp = 0
            while emp < 4 and num2[emp] == 4:
                emp = emp + 1
            for i in range(-1, 2, 2):
                if 0 <= emp + i < 4:
                    for j in range(4):
                        if self.array[j][emp + i]:
                            self.array[j][emp + i] = self.array[j][emp + i] - 1
                            self.array[j][emp] = self.array[j][emp] + 1
                            for z in range(4):
                                if z == 3:
                                    self.indexChanger[z] = self.dict_b[(self.array[z][0], self.array[z][1], self.array[z][2])]
                                else:
                                    self.indexChanger[z] = self.dict_a[(self.array[z][0], self.array[z][1], self.array[z][2])]
                            newValue = self.calcIndex()
                            if record.get(newValue, -1) == -1:
                                record[newValue] = record[value] + 1
                                q.put(newValue)
                            self.array[j][emp + i] = self.array[j][emp + i] + 1
                            self.array[j][emp] = self.array[j][emp] - 1

    @jit
    def setArray(self, array, type):
        """
        :param array: numpy.ndarray
        :param type: 0对应a0,1对应a1
        :return 无
        """
        self.array = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        for i in range(16):
            v = array[i // 4][i % 4]
            if v > 0:
                if type == 1:
                    self.array[(v - 1) // 4][i // 4] = self.array[(v - 1) // 4][i // 4] + 1
                else:
                    self.array[(v - 1) % 4][i % 4] = self.array[(v - 1) % 4][i % 4] + 1

    @jit
    def getWDistance(self):
        """
        :return: 计算当前num的行走距离
        """
        for z in range(4):
            if z == 3:
                self.indexChanger[z] = self.dict_b[(self.array[z][0], self.array[z][1], self.array[z][2])]
            else:
                self.indexChanger[z] = self.dict_a[(self.array[z][0], self.array[z][1], self.array[z][2])]
        return record[self.calcIndex()]


#=============个人测试、Debug使用=============#
if __name__ == '__main__':
    d1 = WalkingDistance()
    d1.initCal()
    d2=copy.copy(d1)
    arr = np.array([[15, 7, 12, 11], [0, 4, 8, 13], [9, 6, 14, 10], [3, 5, 1, 2]])
    # arr = np.array([[5, 1, 2, 4], [9, 6, 3, 8], [13, 15, 10, 11], [14, 0, 7, 12]])
    d1.setArray(arr, 1)
    d2.setArray(arr, 2)
    print(d1.getWDistance() + d2.getWDistance())
