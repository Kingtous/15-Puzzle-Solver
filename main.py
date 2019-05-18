# This Python file uses the following encoding: utf-8
import sys

import numpy as np
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog

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
        self.narray=np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])

    def changeStatus(self, arr):
        pass

    def initMenu(self):
        pass

    def initBox(self):
        pass

    def action_triggered(self):
        sender = self.sender()
        if sender == self.ui.action_gen:
            narray=genTable2array()
            self.narray=narray
            self.setArray(narray)
        elif sender==self.ui.action_solve:
            solveTable(self.narray)
            pass
        elif sender==self.ui.action_load:
            fileDialog=QFileDialog()
            fileDialog.setDirectory('.')
            # fileDialog.setFilter("15-Puzzle Data File(*.data)")
            url=fileDialog.getOpenFileUrl(filter='15-Puzzle Data File(*.data)')
            # TODO 载入
            if url!=None:
                pass

    def setArray(self,narray):
        self.ui.statusbar.showMessage('随机生成器：生成4x4矩阵：'+np.array2string(narray),8000)
        for j in range(narray.shape[0]):
            for k in range(narray.shape[1]):
                num = int(narray[j][k])
                if num==0:
                    eval('self.ui.pushButton_' + str(j * 4 + k + 1) + '.setText(str(num))')
                    eval('self.ui.pushButton_' + str(j * 4 + k + 1) +
                         ".setStyleSheet('background-color : rgb(255,255,255)')")
                else:
                    eval('self.ui.pushButton_' + str(j * 4 + k + 1) + '.setText(str(num))')
                    eval('self.ui.pushButton_' + str(j * 4 + k + 1) +
                         ".setStyleSheet('background-color : rgb(46,139,87)')")
    def exchange(self,btn_1,btn_2):
        # TODO 拖拽传值，看看行不行
        pass


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
