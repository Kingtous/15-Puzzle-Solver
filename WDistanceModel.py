from queue import Queue as queue
from numba import jit
import numpy as np
import copy
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

record = {}


class WalkingDistance:
    @jit
    def __init__(self):
        self.cod = [0 for i in range(5)]
        self.num = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.dict_a = dict()
        self.dict_b = dict()

    @jit
    def encode(self):
        ret = 0
        for i in range(4):
            ret = ret * 35 + self.cod[i]
        return ret

    @jit
    def decode(self, x):
        for i in range(4):
            self.cod[3 - i] = x % 35
            x = x // 35

    @jit
    def initCal(self):
        for i in range(35):
            self.dict_a[(a0[i][0], a0[i][1], a0[i][2])] = i
        for i in range(20):
            self.dict_b[(b0[i][0], b0[i][1], b0[i][2])] = i
        q = queue()

        self.cod[0], self.cod[1] = self.dict_a[(4, 0, 0)], self.dict_a[(0, 4, 0)]
        self.cod[2], self.cod[3] = self.dict_a[(0, 0, 4)], self.dict_b[(0, 0, 0)]

        startValue = self.encode()
        record[startValue] = 0
        q.put(startValue)

        while not q.empty():
            value = q.get()
            self.decode(value)
            num2 = [0, 0, 0, 0]
            for i in range(4):
                for j in range(4):
                    if i == 3:
                        self.num[i][j] = b0[self.cod[i]][j]
                    else:
                        self.num[i][j] = a0[self.cod[i]][j]
                    num2[j] = num2[j] + self.num[i][j]
            emp = 0
            while emp < 4 and num2[emp] == 4:
                emp = emp + 1
            for i in range(-1, 2, 2):
                if 0 <= emp + i < 4:
                    for j in range(4):
                        if self.num[j][emp + i]:
                            self.num[j][emp + i] = self.num[j][emp + i] - 1
                            self.num[j][emp] = self.num[j][emp] + 1
                            for z in range(4):
                                if z == 3:
                                    self.cod[z] = self.dict_b[(self.num[z][0], self.num[z][1], self.num[z][2])]
                                else:
                                    self.cod[z] = self.dict_a[(self.num[z][0], self.num[z][1], self.num[z][2])]
                            newu = self.encode()
                            if record.get(newu, -1) == -1:
                                record[newu] = record[value] + 1
                                q.put(newu)
                            self.num[j][emp + i] = self.num[j][emp + i] + 1
                            self.num[j][emp] = self.num[j][emp] - 1

    def set_num(self, array, type):
        self.num = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        for i in range(16):
            v = array[i // 4][i % 4]
            if v > 0:
                if type == 1:
                    self.num[(v - 1) // 4][i // 4] = self.num[(v - 1) // 4][i // 4] + 1
                else:
                    self.num[(v - 1) % 4][i % 4] = self.num[(v - 1) % 4][i % 4] + 1

    @jit
    def get_wdistance(self):
        for z in range(4):
            if z == 3:
                self.cod[z] = self.dict_b[(self.num[z][0], self.num[z][1], self.num[z][2])]
            else:
                self.cod[z] = self.dict_a[(self.num[z][0], self.num[z][1], self.num[z][2])]
        return record[self.encode()]


if __name__ == '__main__':
    d1 = WalkingDistance()
    d1.initCal()
    d2=copy.deepcopy(d1)
    arr = np.array([[15, 7, 12, 11], [0, 4, 8, 13], [9, 6, 14, 10], [3, 5, 1, 2]])
    # arr = np.array([[5, 1, 2, 4], [9, 6, 3, 8], [13, 15, 10, 11], [14, 0, 7, 12]])
    d1.set_num(arr,1)
    d2.set_num(arr,2)
    print(d1.get_wdistance()+d2.get_wdistance())
