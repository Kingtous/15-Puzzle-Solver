import os
import numpy as np
from PySide2.QtCore import SLOT

'''
Author: Kingtous
Date: 2019-05-16
Description:生成num个的15-puzzle盘，保存为xx.data(01,02...)
'''
# 生成的文件夹
folder = 'data'


# 定义槽函数
def genTable2array():
    '''
    :return: 生成一个puzzle，通过numpy的ndarray返回
    '''
    return np.random.choice(range(0, 16), 16, False).reshape(4, 4).astype(int)


def genTable(num):
    '''
    :param num: 生成数量
    :return: 写入文件
    '''
    for times in range(num):
        mat = np.random.choice(range(0, 16), 16, False).reshape(4, 4)
        np.savetxt(folder + '/' + str(times) + '.data', mat)


if __name__ == '__main__':
    # 创建out目录
    if not os.path.exists(folder):
        os.mkdir(folder)
    # 生成图的数量，0表示空格
    genTable(100)
