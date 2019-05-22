# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'saveform.ui',
# licensing of 'saveform.ui' applies.
#
# Created: Sun May 19 16:06:36 2019
#      by: pyside2-uic  running on PySide2 5.12.3
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(412, 115)
        self.saveOnlyButton = QtWidgets.QPushButton(Form)
        self.saveOnlyButton.setGeometry(QtCore.QRect(90, 80, 91, 31))
        self.saveOnlyButton.setObjectName("saveOnlyButton")
        self.bothButton = QtWidgets.QPushButton(Form)
        self.bothButton.setGeometry(QtCore.QRect(270, 80, 131, 32))
        self.bothButton.setObjectName("bothButton")
        self.playOnlyButton = QtWidgets.QPushButton(Form)
        self.playOnlyButton.setGeometry(QtCore.QRect(180, 80, 91, 32))
        self.playOnlyButton.setObjectName("playOnlyButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 20, 371, 51))
        self.label.setIndent(0)
        self.label.setObjectName("label")
        self.action_store = QtWidgets.QAction(Form)
        self.action_store.setCheckable(True)
        self.action_store.setObjectName("action_store")
        self.action_play = QtWidgets.QAction(Form)
        self.action_play.setCheckable(True)
        self.action_play.setObjectName("action_play")
        self.action_save_play = QtWidgets.QAction(Form)
        self.action_save_play.setCheckable(True)
        self.action_save_play.setObjectName("action_save_play")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "完成！", None, -1))
        self.saveOnlyButton.setText(QtWidgets.QApplication.translate("Form", "仅保存", None, -1))
        self.bothButton.setText(QtWidgets.QApplication.translate("Form", "保存文件并演示", None, -1))
        self.playOnlyButton.setText(QtWidgets.QApplication.translate("Form", "仅演示", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "TextLabel", None, -1))
        self.action_store.setText(QtWidgets.QApplication.translate("Form", "保存", None, -1))
        self.action_store.setShortcut(QtWidgets.QApplication.translate("Form", "Ctrl+1", None, -1))
        self.action_play.setText(QtWidgets.QApplication.translate("Form", "演示", None, -1))
        self.action_play.setShortcut(QtWidgets.QApplication.translate("Form", "Ctrl+2", None, -1))
        self.action_save_play.setText(QtWidgets.QApplication.translate("Form", "保存并演示", None, -1))
        self.action_save_play.setShortcut(QtWidgets.QApplication.translate("Form", "Ctrl+3", None, -1))

