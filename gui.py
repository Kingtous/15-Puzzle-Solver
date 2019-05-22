# This Python file uses the following encoding: utf-8
import os
import sys

import numpy as np
from PySide2.QtCore import QTime
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

from saveform import Ui_Form
from tableGenerator import genTable2array
from tableSolver import solveTable
from ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initMenu()
        self.initBox()
        self.ui.action_gen.triggered.connect(self.action_triggered)
        self.ui.action_solve.triggered.connect(self.action_triggered)
        self.ui.action_load.triggered.connect(self.action_triggered)
        self.ui.action_store.triggered.connect(self.action_triggered)
        self.narray = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
        self.result = None

    def changeStatus(self, arr):
        pass

    def initMenu(self):
        pass

    def initBox(self):
        pass

    def fail(self):
        message = QMessageBox()
        message.setText('无解')
        message.exec_()

    def action_triggered(self):
        sender = self.sender()
        if sender == self.ui.action_gen:
            narray = genTable2array()
            self.narray = narray
            self.setArray(narray)
        elif sender == self.ui.action_solve:
            # 判断是否有解
            cnt = 0
            narray_tmp = np.copy(self.narray).reshape(1, 16)

            posy = int(np.where(narray_tmp == 0)[1][0])

            narray_tmp = np.delete(narray_tmp, posy)
            length = narray_tmp.shape[0]
            for i in range(length):
                for p in range(i + 1, length):
                    if narray_tmp[i] > narray_tmp[p]:
                        cnt = cnt + 1
            if cnt % 2 == 0:
                # inversion为偶数，另外还需要空白在从下往上数第奇数行
                if int(self.narray.shape[0] - np.where(self.narray == 0)[0][0]) % 2 != 0:
                    self.result = solveTable(self.narray)
                    self.processResult(self.result)
                else:
                    self.fail()
            else:
                # inversion为奇数，另外还需要空白在从下往上数第偶数行
                if int(self.narray.shape[0] - np.where(self.narray == 0)[0][0]) % 2 == 0:
                    self.result = solveTable(self.narray)
                    self.processResult(self.result)
                else:
                    self.fail()

        elif sender == self.ui.action_load:
            fileDialog = QFileDialog()
            fileDialog.setDirectory('.')
            # fileDialog.setFilter("15-Puzzle Data File(*.data)")
            url = fileDialog.getOpenFileUrl(filter='15-Puzzle Data File(*.data)')
            # 载入data
            narray_backup = np.copy(self.narray)
            if url != None:
                path = url[0].path()
                try:
                    if os.path.exists(os.path.dirname(path)):
                        narray = np.loadtxt(path).astype(int)
                        self.setArray(narray)
                    else:
                        self.ui.statusbar.showMessage('载入失败', 3000)
                except:
                    message = QMessageBox()
                    message.setText(path + ' 不是一个有效的文件')
                    message.exec_()
                    self.narray = narray_backup

        elif sender == self.ui.action_store:
            # 保存当前状态
            self.saveResult()

    def saveResult(self):
        if self.result == None:
            message = QMessageBox(self)
            message.setText('没有结果显示，请先执行出解决方案')
            message.show()
        else:
            filedialog = QFileDialog(self)
            url = filedialog.getSaveFileUrl(filter='15-Puzzle Data File(*.data)')

            path = url[0].path()

            if os.path.exists(os.path.dirname(path)):
                file = open(path, 'w')
                for m in self.result:
                    file.write(m + '\n')
                file.close()
                self.ui.statusbar.showMessage('保存成功：' + path, 3000)

            else:
                message = QMessageBox()
                message.setText('路径有误，保存失败')

    def processResult(self, result):
        form = Ui_Form()
        win = QMainWindow(self)
        win.ui = form
        form.setupUi(win)

        # 设置结果文字
        win.ui.label.setText('搜索到结果，共 ' + str(len(result)) + ' 项(包括初始状态)，接下来...')

        # 设置槽
        win.ui.saveOnlyButton.clicked.connect(self.saveResult)
        win.ui.playOnlyButton.clicked.connect(self.playResult)
        win.ui.bothButton.clicked.connect(self.save_play)

        win.show()

    def save_play(self):
        self.saveResult()
        self.playResult()

    def playResult(self):
        if self.result != None:
            cnt = 1
            for step in self.result:
                file = open('tmp', 'w')
                step = step.replace('[', '').replace(']', '')
                file.write(step)
                file.close()
                self.setArray(np.loadtxt('tmp').astype(int),
                              preText='(' + str(cnt) + '/' + str(len(self.result)) + ')')
                cnt = cnt + 1
                t = QTime()
                t.start()
                while t.elapsed() < 100:
                    QApplication.processEvents()

    def setArray(self, narray, preText=''):
        self.narray = narray
        self.ui.statusbar.showMessage(preText + '生成：' + np.array2string(narray), 8000)
        for j in range(narray.shape[0]):
            for k in range(narray.shape[1]):
                num = int(narray[j][k])
                if num == 0:
                    eval('self.ui.pushButton_' + str(j * 4 + k + 1) + '.setText(str(num))')
                    eval('self.ui.pushButton_' + str(j * 4 + k + 1) +
                         ".setStyleSheet('background-color : rgb(255,255,255)')")
                else:
                    eval('self.ui.pushButton_' + str(j * 4 + k + 1) + '.setText(str(num))')
                    eval('self.ui.pushButton_' + str(j * 4 + k + 1) +
                         ".setStyleSheet('background-color : rgb(46,139,87)')")

    def exchange(self, btn_1, btn_2):
        # TODO 拖拽传值，看看行不行
        pass

    def press(self):
        # TODO 点按互换位置

        pass


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
