from queue import Queue as queue
import numpy as np
import copy

'''
Author: Kingtous
Description: Walking Distance 步行距离计算
Date: 2019-06-03
'''

#===================横纵向可能出现的种类(模拟小型Pattern Database)====================#
# 第1-3行或者第1-3列，有AAAA,BBBB,CCCC,DDDD四种情况
a1_3 = ((0, 0, 0, 4), (0, 0, 1, 3), (0, 0, 2, 2), (0, 0, 3, 1), (0, 0, 4, 0),
        (0, 1, 0, 3), (0, 1, 1, 2), (0, 1, 2, 1), (0, 1, 3, 0), (0, 2, 0, 2), (0, 2, 1, 1), (0, 2, 2, 0),
        (0, 3, 0, 1), (0, 3, 1, 0), (0, 4, 0, 0), (1, 0, 0, 3), (1, 0, 1, 2), (1, 0, 2, 1), (1, 0, 3, 0),
        (1, 1, 0, 2), (1, 1, 1, 1), (1, 1, 2, 0), (1, 2, 0, 1), (1, 2, 1, 0), (1, 3, 0, 0), (2, 0, 0, 2),
        (2, 0, 1, 1), (2, 0, 2, 0), (2, 1, 0, 1), (2, 1, 1, 0), (2, 2, 0, 0), (3, 0, 0, 1), (3, 0, 1, 0),
        (3, 1, 0, 0), (4, 0, 0, 0))
# 最后一行或者一列，只能出现 AAA,BBB,CCC,DDD(含有一个空格)
a4 = ((0, 0, 0, 3), (0, 0, 1, 2), (0, 0, 2, 1), (0, 0, 3, 0), (0, 1, 0, 2),
      (0, 1, 1, 1), (0, 1, 2, 0), (0, 2, 0, 1), (0, 2, 1, 0), (0, 3, 0, 0), (1, 0, 0, 2), (1, 0, 1, 1),
      (1, 0, 2, 0), (1, 1, 0, 1), (1, 1, 1, 0), (1, 2, 0, 0), (2, 0, 0, 1), (2, 0, 1, 0), (2, 1, 0, 0),
      (3, 0, 0, 0))
#========================================================#

"""
record存放计算所得的Walking Distance，通过key访问value
"""
record = {}

class WalkingDistance:
    """
    Walking Distance类
    """
    def __init__(self):
        self.indexChanger = [0 for i in range(5)]
        self.array = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.dict_a1_3 = dict()
        self.dict_a4 = dict()

    def calcIndex(self):
        """
        :return: record对应的下标
        """
        ret = 0
        for i in range(4):
            ret = ret * 35 + self.indexChanger[i]
        return ret

    def getIndex(self, x):
        """
        :param x: 下标
        :return: 无，计算出index，放入indexChanger中
        """
        for i in range(4):
            self.indexChanger[3 - i] = x % 35
            x = x // 35

    def initCal(self):
        """
        :return: 无，用于初始化计算
        """
        # 只需要记元组中前三个数即可表示四个数
        for i in range(35):
            self.dict_a1_3[(a1_3[i][0], a1_3[i][1], a1_3[i][2])] = i
        for i in range(20):
            self.dict_a4[(a4[i][0], a4[i][1], a4[i][2])] = i
        q = queue()
        # 计算目的结果
        self.indexChanger[0], self.indexChanger[1] = self.dict_a1_3[(4, 0, 0)], self.dict_a1_3[(0, 4, 0)]
        self.indexChanger[2], self.indexChanger[3] = self.dict_a1_3[(0, 0, 4)], self.dict_a4[(0, 0, 0)]

        start_value = self.calcIndex()
        record[start_value] = 0
        q.put(start_value)

        while not q.empty():
            value = q.get()
            self.getIndex(value)
            num2 = [0, 0, 0, 0]
            for i in range(4):
                for j in range(4):
                    if i == 3:
                        self.array[i][j] = a4[self.indexChanger[i]][j]
                    else:
                        self.array[i][j] = a1_3[self.indexChanger[i]][j]
                    num2[j] = num2[j] + self.array[i][j]
            point = 0
            # 找到不符合目的的point
            while point < 4 and num2[point] == 4:
                point = point + 1
            for i in range(-1, 2, 2):
                if 0 <= point + i < 4:
                    for j in range(4):
                        if self.array[j][point + i]:
                            self.array[j][point + i] = self.array[j][point + i] - 1
                            self.array[j][point] = self.array[j][point] + 1
                            for z in range(4):
                                if z == 3:
                                    self.indexChanger[z] = self.dict_a4[(self.array[z][0], self.array[z][1], self.array[z][2])]
                                else:
                                    self.indexChanger[z] = self.dict_a1_3[(self.array[z][0], self.array[z][1], self.array[z][2])]
                            newValue = self.calcIndex()
                            if record.get(newValue, -1) == -1:
                                record[newValue] = record[value] + 1
                                q.put(newValue)
                            self.array[j][point + i] = self.array[j][point + i] + 1
                            self.array[j][point] = self.array[j][point] - 1

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

    def getWDistance(self):
        """
        :return: 计算当前num的行走距离
        """
        for z in range(4):
            if z == 3:
                self.indexChanger[z] = self.dict_a4[(self.array[z][0], self.array[z][1], self.array[z][2])]
            else:
                self.indexChanger[z] = self.dict_a1_3[(self.array[z][0], self.array[z][1], self.array[z][2])]
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
