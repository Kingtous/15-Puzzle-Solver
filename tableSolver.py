import time
from WDistanceModel import WalkingDistance
from numba import jit
import numpy as np
import copy

'''
Author: Kingtous
Description: 解决器
Date: 2019-06-03
'''

# ===配置文件===#
maxStep = 80

# =====贪婪搜索开关(只适用于A*算法)=====#
greedyOptions = True

@jit
def calc_h(array):
    """
    :param array: numpy.ndarray
    :return: 一共有四种heuristic函数可供返回
    1. calc_h_1(array) 格子错位数
    2. calc_h_2(array) Manhattan距离
    3. calc_h_3(array) Manhattan距离+Linear Conflict
    3. calc_h_4(array) Walking Distance
    """
    return calc_h_3(array)


def solveWay(arr):
    """
    :param arr: numpy.ndarray
    :return: 通过方法解决出的问题
    解决方式：
    1. Astar(arr,0) -> A*算法
    2. IDA(arr) -> IDA*算法
    """
    return IDA(arr)


# ============以下内容不做更改============
goal = "[[ 1.  2.  3.  4.]\n [ 5.  6.  7.  8.]\n [ 9. 10. 11. 12.]\n [13. 14. 15.  0.]]"
goal2 = "[[ 1  2  3  4]\n [ 5  6  7  8]\n [ 9 10 11 12]\n [13 14 15  0]]"
state = []


def solveTable(arr):
    if checkIfSolvable(arr):
        return solveWay(arr)  # solve(arr, [], 0)
    else:
        print('无解')
        return None


@jit
def calc_h_1(array):
    '''
    h=相应错位的格子
    :param array:
    :return:
    '''
    tmp = array.reshape(1, 16)
    cnt = 0
    for index in range(tmp.size):
        if index == 0:
            continue
        if tmp[0, index] != (index + 1) % 16:
            cnt = cnt + 1
    return cnt


@jit
def calc_h_2(array):
    """
    h=曼哈顿距离
    :param array:
    :return:
    """
    cnt = 0
    for j in range(4):  # array.shape[0]):
        for k in range(4):  # array.shape[1]):
            num = int(array[j][k])
            if num == 0:
                continue
            if num != (j * 4 + k + 1):
                j2 = num // 4
                k2 = num % 4
                if k2 == 0:
                    j2 = j2 - 1
                    k2 = 3  # array.shape[1] - 1
                else:
                    k2 = k2 - 1
                # print(abs(j-j2)+abs(k-k2))
                cnt = cnt + abs(j - j2) + abs(k - k2)
    return cnt


@jit
def calc_h_3(array):
    """
    h=曼哈顿距离+Linear Confict
    """
    h = 0
    h = h + calc_h_2(array)
    # posx,posy=np.where(array == 0)
    # posx=int(posx[0])
    # posy=int(posy[0])
    # Debug
    tmp = 0
    # step.1 考虑行
    for row in range(4):  # array.shape[0]):
        tmp_row = array[row]
        # if row==posx:
        #     np.delete(tmp_row,posy)
        #     input()
        for j in range(4):  # tmp_row.shape[0]):
            for k in range(j + 1, 4):  # tmp_row.shape[0]):
                if tmp_row[j] == 0 or tmp_row[k] == 0:
                    continue
                # if j==k:
                #     continue
                if tmp_row[j] > tmp_row[k]:
                    # 如果两个都在本行，则颠倒+2，注意0
                    if (tmp_row[j] - 1) // 4 == row and (tmp_row[k] - 1) // 4 == row:
                        # print(row,j,"<->",row,k)
                        tmp = tmp + 2
                        h = h + 2
    # print('Linear Confict',str(tmp))

    return h

d1 = WalkingDistance()
d1.initCal()
d2 = WalkingDistance()
d2.initCal()

@jit
def calc_h_4(array):
    d1.setArray(array, 1)
    d2.setArray(array, 2)
    return d1.getWDistance() + d2.getWDistance()


@jit
def isPosLegal(tuple, maxNum):
    """
    :param tuple: (x坐标,y坐标)
    :param maxNum: 行列的最大值
    :return: True表示位置合法，False为非法
    """
    x = tuple[0]
    y = tuple[1]
    if x < 0 or y < 0 or x >= maxNum or y >= maxNum:
        return False
    else:
        return True


currentStep = {}
state_dict = {}
way_ing = []
way_booked = set()


def init():
    currentStep.clear()
    state_dict.clear()
    way_ing.clear()
    way_booked.clear()


@jit
def checkIfSolvable(narray):
    cnt = 0
    narray_tmp = np.copy(narray).reshape(1, 16)

    posy = int(np.where(narray_tmp == 0)[1][0])

    narray_tmp = np.delete(narray_tmp, posy)
    length = narray_tmp.shape[0]
    for i in range(length):
        for p in range(i + 1, length):
            if narray_tmp[i] > narray_tmp[p]:
                cnt = cnt + 1
    if cnt % 2 == 0:
        # inversion为偶数，另外还需要空白在从下往上数第奇数行
        if int(narray.shape[0] - np.where(narray == 0)[0][0]) % 2 != 0:
            return True
        else:
            return False
    else:
        # inversion为奇数，另外还需要空白在从下往上数第偶数行
        if int(narray.shape[0] - np.where(narray == 0)[0][0]) % 2 == 0:
            return True
        else:
            return False


def Astar(array, step):
    global way_ing
    global way_solution
    global maxStep
    global currentStep

    array = array.astype(int)
    h = calc_h(array)
    print(array, h)

    way_ing.append((h, array))
    state_dict[np.array2string(array.astype(int))] = None

    currentStep[np.array2string(array).replace('\n', '')] = 0

    while len(way_ing) != 0:
        # if step > maxStep:
        #     break

        (h, array) = way_ing[0]
        way_ing.remove(way_ing[0])

        if (calc_h(array) == 0):
            print('找到解')
            break

        # 开始查找子结点
        posx, posy = np.where(array == 0)
        posx = int(posx[0])
        posy = int(posy[0])

        # 四个方向
        dirL = []
        dirL.append((posx + 1, posy))
        dirL.append((posx - 1, posy))
        dirL.append((posx, posy + 1))
        dirL.append((posx, posy - 1))

        best_array = []

        # 四个方向，扩展
        for dir in dirL:
            if isPosLegal(dir, array.shape[0]):
                tmp_array = np.copy(array)
                tmp_array[posx, posy], tmp_array[dir[0], dir[1]] = \
                    tmp_array[dir[0], dir[1]], tmp_array[posx, posy]
                if way_booked.__contains__(np.array2string(tmp_array)) or \
                        currentStep.get(np.array2string(tmp_array), -1) != -1:
                    continue
                tmp_h = calc_h(tmp_array)

                cs = currentStep[np.array2string(array).replace('\n', '')]

                if not greedyOptions:
                    if cs > maxStep:
                        continue
                    total_h = cs + tmp_h
                else:
                    total_h = tmp_h

                # tmp_array 入 currentStep
                has_value = currentStep.get(np.array2string(tmp_array).replace('\n', ''), -1)
                if has_value == -1 or has_value > total_h:
                    # 不存在或者有劣质h
                    if has_value != -1:
                        # print('存在劣质解')
                        pass
                    currentStep[np.array2string(tmp_array).replace('\n', '')] = currentStep[
                                                                                    np.array2string(array).replace('\n',
                                                                                                                   '')] + 1
                    best_array.append((total_h, tmp_array))
                else:
                    if has_value <= total_h:
                        # 已经存在优质或相等h的点，不添加
                        # print('不添加')
                        continue
                    else:
                        best_array.append((total_h, tmp_array))
                # 构建路径，方便后续输出路径
                state_dict[np.array2string(tmp_array)] = np.array2string(array)
        # 将当前array加入已搜索过
        way_booked.add(np.array2string(array))

        # 排序
        way_ing = way_ing + best_array
        way_ing = sorted(way_ing, key=lambda x: x[0])
        # print('当前最小：' + str(way_ing[0][0]))
        # print(way_ing[0][1])

        step = step + 1

        # for solution in best_array:
        #     way_booked.add(np.array2string(solution[1]))
        #     solve(solution[1],solve_way+[np.array2string(solution[1])],step+1)
        # way_book.remove(np.array2string(solution[1]))
        # if(best_dir!=None):
        #     solve_way.append(best_dir)
        #     h=best_h
        #     array=best_array
        #     print(array,' ',h,'\n')
        # else:
        #     print('==============================回溯')
        #     break

    if calc_h(array) == 0:
        try:
            tmp = state_dict[goal]
        except:
            tmp = state_dict[goal2]
            pass
        state.append(goal2)
        while tmp != None:
            state.append(tmp)
            tmp = state_dict[tmp]
        state.reverse()
        print('共', str(len(state)), '步')
        if len(state) == 0:
            # 一步到位
            state.append(goal)
        output_terminal()

        # 清理状态
        state_dict.clear()
        way_ing.clear()
        way_booked.clear()

        return state
    else:
        print('无解')
        return None


def output_terminal():
    global state_dict
    global goal
    global state
    # 根据goal反推状态

    for st in state:
        print(st)


def cmp_rule(t1, t2):
    if t1[0] < t2[0]:
        return -1
    else:
        return 0


# ================IDA* Algorithm==================
IDA_MaxStep = 80
stepFound = -1
IDA_StateList = []
enuStep = None
num = 0


def dfs_IDA(arr, step, moveList, preDirInt):
    global enuStep, stepFound, IDA_StateList, num
    if step > enuStep:
        return False

    if step == enuStep:
        if calc_h(arr) == 0:
            stepFound = step
            IDA_StateList = moveList
            return True

    # 开始查找子结点
    posx, posy = np.where(arr == 0)
    posx = int(posx[0])
    posy = int(posy[0])

    # 四个方向
    dirL = []
    # append顺序不能更改，防止回退
    dirL.append((posx - 1, posy))  # left
    dirL.append((posx, posy + 1))  # up
    dirL.append((posx, posy - 1))  # down
    dirL.append((posx + 1, posy))  # right

    for i in range(len(dirL)):
        if isPosLegal(dirL[i], 4):  # arr.shape[0]):
            # 不回退
            if preDirInt is not None and i + preDirInt == 3:
                continue
            arr[posx, posy], arr[dirL[i][0], dirL[i][1]] = \
                arr[dirL[i][0], dirL[i][1]], arr[posx, posy]
            if step + calc_h(arr) <= enuStep:
                num = num + 1
                if dfs_IDA(arr, step + 1, moveList + [copy.copy(arr)], i):
                    return True
            arr[dirL[i][0], dirL[i][1]], arr[posx, posy] = \
                arr[posx, posy], arr[dirL[i][0], dirL[i][1]]
    else:
        return False


def IDA(arr):
    global stepFound, IDA_StateList, enuStep
    if checkIfSolvable(arr):
        enuStep = calc_h(arr)
        while enuStep <= IDA_MaxStep and not dfs_IDA(arr, 0, [], None):
            # 有解
            enuStep = enuStep + 1
            print('在最大深度为', enuStep, "中没找到解")
        return IDA_StateList
    else:
        print('无解')
        return None
    pass


# ================================================
if __name__ == '__main__':
    # goal=np.array([[1 2 3 4],[5 6 7 8],[9 10 11 12],[13 14 15 0]])

    # arr = np.array([[1,7,2,4], [3, 10, 8, 11], [6, 5, 15, 12], [9, 14, 0, 13]])

    # 50步样例
    # arr = np.array([[1, 13, 12, 2], [10, 14, 11, 15], [0, 3, 6, 4], [7, 9, 5, 8]])

    # arr = np.array([[8, 11, 2, 12], [0, 7, 3, 10], [6, 9, 15, 13], [4, 14, 5, 1]])
    t1 = time.time()

    # 14步样例
    arr = np.array([[5, 1, 2, 4], [9, 6, 3, 8], [13, 15, 10, 11], [14, 0, 7, 12]])

    # s=solveTable(arr)
    # while s==None:
    #     init()
    #     print ('step=',maxStep)
    #     s=solveTable(arr)
    # print(str(len(s)))
    # print(calc_h(arr))
    # input()
    st = IDA(arr)

    if st != None:
        for t in st:
            print(t)

    t2 = time.time()
    print(t2 - t1, "s")
    print(num)

    # print(arr)
    # print("h2:",str(calc_h_2(arr)))
    # print("h3:",str(calc_h_3(arr)))

    # cnt = 0
    # while os.path.exists(folder + '/' + str(cnt) + '.data'):
    #     array = np.loadtxt(folder + '/' + str(cnt) + '.data')
    #     solve(array.reshape(4, 4))
    #     cnt = cnt + 1

    # 1 13 12 2 10 14 11 15 0 3 6 4 7 9 5 8
    # 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0
