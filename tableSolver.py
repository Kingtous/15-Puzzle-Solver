import numpy as np
import os
from tableGenerator import folder
import copy

# ===配置文件===#
maxStep = 100000
goal="[[ 1  2  3  4]\n [ 5  6  7  8]\n [ 9 10 11 12]\n [13 14 15  0]]"
# ============#

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


def calc_h(array):
    return calc_h_2(array)


def isPosLegal(tuple,maxNum):
    '''
    :param tuple: (x坐标,y坐标)
    :param maxNum: 行列的最大值
    :return: True表示位置合法，False为非法
    '''
    x=tuple[0]
    y=tuple[1]
    if x<0 or y<0 or x>=maxNum or y>=maxNum:
        return False
    else:
        return True

state_dict={}
way_ing=[]
way_booked=set()
way_solution=[]



def solve(array,solve_way,step):
    global way_ing
    global way_solution
    global maxStep
    h = calc_h(array)
    print(array,h)

    way_ing.append((h,array))
    state_dict[np.array2string(array)]=None

    while len(way_ing) != 0:
        if step > maxStep:
            break

        (h,array)=way_ing[0]
        way_ing.remove(way_ing[0])

        if (calc_h(array)==0):
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

        best_array=[]

        # 四个方向，扩展
        for dir in dirL:
            if(isPosLegal(dir,array.shape[0])):
                tmp_array = np.copy(array)
                tmp_array[posx,posy],tmp_array[dir[0],dir[1]]=\
                    tmp_array[dir[0],dir[1]],tmp_array[posx,posy]
                if way_booked.__contains__(np.array2string(tmp_array)):
                    continue
                tmp_h=calc_h(tmp_array)

                best_array.append((tmp_h,tmp_array))

                # 构建路径，方便后续输出路径
                state_dict[np.array2string(tmp_array)]=np.array2string(array)


        # 将当前array加入已搜索过
        way_booked.add(np.array2string(array))

        # 排序
        way_ing=way_ing+best_array
        way_ing=sorted(way_ing,key=lambda x:x[0])
        print('当前最小：'+str(way_ing[0][0]))

        step=step+1


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

    if h==0:
        way_solution.append(solve_way)
        print(solve_way)
        output_terminal()
        return way_solution
    else:
        print('无解')
        return None

def output_terminal():
    global state_dict
    global goal
    # 根据goal反推状态
    state=[]

    tmp=state_dict[goal]

    while tmp!=None:
        state.append(tmp)
        tmp=state_dict[tmp]

    state.reverse()

    for st in state:
        print(st)
    print(goal)
    print('共',str(len(state)),'步')




def cmp_rule(t1,t2):
    if t1[0]<t2[0]:
        return -1
    else:
        return 0

def solveTable(arr):
    solve(arr,[],0)

if __name__ == '__main__':
    # goal=np.array([[1 2 3 4],[5 6 7 8],[9 10 11 12],[13 14 15 0]])
    # arr=np.array([[1,2,3,4],[5,6,8,7],[9,10,12,11],[0,13,14,15]])
    arr = np.array([[1, 13, 12, 2], [10, 14, 11, 15], [0, 3, 6, 4], [7, 9, 5, 8]])
    solve(arr,[],0)
    # cnt = 0
    # while os.path.exists(folder + '/' + str(cnt) + '.data'):
    #     array = np.loadtxt(folder + '/' + str(cnt) + '.data')
    #     solve(array.reshape(4, 4))
    #     cnt = cnt + 1
