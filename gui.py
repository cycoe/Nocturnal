#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from modules.Robber import Robber
from modules.Logger import Logger
from modules.MisUtils import MisUtils
from modules.String import String
import pyqrcode
import sys


#
#                            _ooOoo_
#                           o8888888o
#                           88" . "88
#                           (| -_- |)
#                           O\  =  /O
#                        ____/`---'\____
#                      .'  \\|     |//  `.
#                     /  \\|||  :  |||//  \
#                    /  _||||| -:- |||||-  \
#                    |   | \\\  -  /// |   |
#                    | \_|  ''\---/''  |   |
#                    \  .-\__  `-`  ___/-. /
#                  ___`. .'  /--.--\  `. . __
#               ."" '<  `.___\_<|>_/___.'  >'"".
#              | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#              \  \ `-.   \_ __\ /__ _/   .-` /  /
#         ======`-.____`-.___\_____/___.-`____.-'======
#                            `=---='
#        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                      Buddha Bless, No Bug !


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.windowWidth = 800
        self.windowHeight = 600
        self.screenWidth, self.screenHeight = self.get_screen_size()
        self.x = (self.screenWidth - self.windowWidth) // 2
        self.y = (self.screenHeight - self.windowHeight) // 2

        self.centralWidget = QtWidgets.QWidget(self)
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.controlLayout = QtWidgets.QGridLayout()
        self.messageLayout = QtWidgets.QGridLayout()
        self.usernameLabel = QtWidgets.QLabel('学号: ')
        self.passwordLabel = QtWidgets.QLabel('密码: ')
        self.usernameLine = QtWidgets.QLineEdit()
        self.passwordLine = QtWidgets.QLineEdit()
        self.loginButton = QtWidgets.QPushButton('登陆')

    def set_var(self):
        pass

    @staticmethod
    def get_screen_size():
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        return screen.width(), screen.height()

    def setup_ui(self):
        self.setGeometry(self.x, self.y, self.windowWidth, self.windowHeight)
        self.setMinimumSize(self.windowWidth, self.windowHeight)
        self.setWindowTitle('Class Robber')
        self.setCentralWidget(self.centralWidget)
        self.setLayout(self.mainLayout)

        self.mainLayout.addLayout(self.controlLayout)
        self.mainLayout.addLayout(self.messageLayout)
        self.controlLayout.addWidget(self.usernameLabel, 0, 0, 1, 1)
        self.controlLayout.addWidget(self.passwordLabel, 1, 0, 1, 1)
        self.controlLayout.addWidget(self.usernameLine, 0, 1, 1, 1)
        self.controlLayout.addWidget(self.passwordLine, 1, 1, 1, 1)
        self.controlLayout.addWidget(self.loginButton, 1, 2, 1, 1)
        self.usernameLine.setFixedHeight(30)
        self.passwordLine.setFixedHeight(30)
        self.usernameLine.setMinimumWidth(200)
        self.passwordLine.setMinimumWidth(200)


def main():
    robber = Robber()
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.setup_ui()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
