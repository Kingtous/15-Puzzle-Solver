import numpy as np
import os
from tableGenerator import folder
import copy
from numba import jit
import time
from numba import jit

# ===配置文件===#
maxStep = 90
goal = "[[ 1.  2.  3.  4.]\n [ 5.  6.  7.  8.]\n [ 9. 10. 11. 12.]\n [13. 14. 15.  0.]]"
goal2 = "[[ 1  2  3  4]\n [ 5  6  7  8]\n [ 9 10 11 12]\n [13 14 15  0]]"
state = []


# ============#
@jit(nopython=True)
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


@jit(nopython=True)
def calc_h_2(array):
    '''
    h=曼哈顿距离
    :param array:
    :return:
    '''
    cnt = 0
    for j in range(array.shape[0]):
        for k in range(array.shape[1]):
            if int(array[j][k]) == 0:
                continue
            if int(array[j][k]) != (j * 4 + k + 1):
                j2 = int(array[j][k]) // 4
                k2 = int(array[j][k]) % 4
                if k2 == 0:
                    j2 = j2 - 1
                    k2 = array.shape[1] - 1
                else:
                    k2 = k2 - 1
                # print(abs(j-j2)+abs(k-k2))
                cnt = cnt + abs(j - j2) + abs(k - k2)
    return cnt


@jit(nopython=True)
def calc_h_3(array):
    '''
    h=曼哈顿距离+Linear Confict
    '''
    h = 0
    h = h + calc_h_2(array)

    # posx,posy=np.where(array == 0)
    # posx=int(posx[0])
    # posy=int(posy[0])

    # Debug
    tmp = 0

    # step.1 考虑行
    for row in range(array.shape[0]):
        tmp_row = array[row]
        # if row==posx:
        #     np.delete(tmp_row,posy)
        #     input()
        for j in range(tmp_row.shape[0]):
            for k in range(j + 1, tmp_row.shape[0]):
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


@jit(nopython=True)
def calc_h(array):
    return calc_h_3(array)

@jit(nopython=True)
def isPosLegal(tuple, maxNum):
    '''
    :param tuple: (x坐标,y坐标)
    :param maxNum: 行列的最大值
    :return: True表示位置合法，False为非法
    '''
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

@jit(nopython=True)
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


def solve(array, solve_way, step):
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
            if (isPosLegal(dir, array.shape[0])):
                tmp_array = np.copy(array)
                tmp_array[posx, posy], tmp_array[dir[0], dir[1]] = \
                    tmp_array[dir[0], dir[1]], tmp_array[posx, posy]
                if way_booked.__contains__(np.array2string(tmp_array)) or \
                        currentStep.get(np.array2string(tmp_array), -1) != -1:
                    continue
                tmp_h = calc_h(tmp_array)

                cs = currentStep[np.array2string(array).replace('\n', '')]

                if cs > maxStep:
                    continue

                total_h = cs + tmp_h

                # tmp_array 入 currentStep
                has_value = currentStep.get(np.array2string(tmp_array).replace('\n', ''), -1)
                if has_value == -1 or has_value > total_h:
                    # 不存在或者有劣质h
                    if has_value != -1:
                        print('存在劣质解')
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


def solveTable(arr):
    if checkIfSolvable(arr):
        return solve(arr, [], 0)
    else:
        print('无解')
        return None


# ================IDA* Algorithm==================
IDA_MaxStep = 80
stepFound = -1
IDA_StateRecord=[]
IDA_StateList=[]
enuStep = None
num=0


def dfs_IDA(arr, step, moveList, preDirInt):
    global enuStep
    global stepFound
    global IDA_StateList
    global IDA_StateRecord
    global num
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
    # 顺序不能更改，防止回退
    dirL.append((posx - 1, posy))  # left
    dirL.append((posx, posy + 1))  # up
    dirL.append((posx, posy - 1))  # down
    dirL.append((posx + 1, posy))  # right

    for dir in dirL:
        if isPosLegal(dir, arr.shape[0]):
            # 不回退
            if preDirInt is not None and dirL.index(dir) + preDirInt == 3:
                continue
            arr[posx, posy], arr[dir[0], dir[1]] = \
                arr[dir[0], dir[1]], arr[posx, posy]
            if np.array2string(arr) in IDA_StateRecord:
                continue
            if step + calc_h(arr) <= enuStep:
                num=num+1
                IDA_StateRecord.append(np.array2string(arr))
                if dfs_IDA(arr, step + 1, moveList + [np.copy(arr)], dirL.index(dir)):
                    return True
                IDA_StateRecord.remove(np.array2string(arr))

            arr[dir[0], dir[1]], arr[posx, posy] = \
                arr[posx, posy], arr[dir[0], dir[1]]
    else:
        return False

def IDA(arr):
    global enuStep
    global IDA_StateRecord
    if checkIfSolvable(arr):
        enuStep = calc_h(arr)
        IDA_StateRecord.append(np.array2string(arr))
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
    arr = np.array([[1, 13, 12, 2], [10, 14, 11, 15], [0, 3, 6, 4], [7, 9, 5, 8]])
    t1 = time.time()

    # 14步样例
    # arr = np.array([[5, 1, 2, 4], [9, 6, 3, 8], [13, 15, 10, 11], [14, 0, 7, 12]])

    # s=solveTable(arr)
    # while s==None:
    #     init()
    #     print ('step=',maxStep)
    #     s=solveTable(arr)
    # print(str(len(s)))
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
