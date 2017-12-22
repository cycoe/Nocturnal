#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from modules.Robber import Robber
from modules.Spider import Spider
from modules.MisUtils import MisUtils
from modules.String import String
from modules.Mail import Mail
import threading
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

        if MisUtils.checkConfFile():
            MisUtils.loadConfFile()

        self.label_ = {}
        self.inputLine_ = {}

        self.centralWidget = QtWidgets.QWidget(self)
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.controlLayout = QtWidgets.QGridLayout()
        self.messageLayout = QtWidgets.QGridLayout()

        self.loginButton = QtWidgets.QPushButton('登陆')
        self.emailLoginButton = QtWidgets.QPushButton('登陆邮箱')
        self.robReportButton = QtWidgets.QPushButton('抢报告')
        self.logShower = QtWidgets.QTextBrowser()

        self.robber = Robber(self.log_shower_callback)

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
        self.centralWidget.setLayout(self.mainLayout)

        self.mainLayout.addLayout(self.controlLayout)
        self.mainLayout.addLayout(self.messageLayout)

        for index in range(len(MisUtils.confDict.keys())):
            key = list(MisUtils.confDict.keys())[index]
            self.label_[key] = QtWidgets.QLabel(String[key])
            self.controlLayout.addWidget(self.label_[key], index, 0, 1, 1)
            self.inputLine_[key] = QtWidgets.QLineEdit(MisUtils.confDict[key])
            self.controlLayout.addWidget(self.inputLine_[key], index, 1, 1, 1)
            self.inputLine_[key].setFixedHeight(30)
            self.inputLine_[key].setMinimumWidth(200)

        self.controlLayout.addWidget(self.loginButton, 1, 2, 1, 1)
        self.controlLayout.addWidget(self.emailLoginButton, 6, 2, 1, 1)
        self.controlLayout.addWidget(self.robReportButton, 7, 0, 1, 3)

        self.messageLayout.addWidget(self.logShower, 0, 0, 1, 1)
        self.logShower.setReadOnly(True)

    def set_connect(self):
        self.loginButton.clicked.connect(self.login_button_clicked)
        self.emailLoginButton.clicked.connect(self.email_login_button_clicked)
        self.robReportButton.clicked.connect(self.rob_report_button_clicked)

    @QtCore.pyqtSlot()
    def rob_report_button_clicked(self):
        if self.robReportButton.text() == '抢报告':
            self.login_button_clicked()
            self.loginButton.setEnabled(False)
            MisUtils.signal['report'] = True
            self.robReportButton.setText('点击停止')
            threading.Thread(target=self.robber.robReport, args=(self.rob_report_button_callback,)).start()
        elif self.robReportButton.text() == '点击停止':
            self.robReportButton.setText('正在停止...')
            self.robReportButton.setEnabled(False)
            MisUtils.signal['report'] = False

    @QtCore.pyqtSlot()
    def login_button_clicked(self):
        self.loginButton.setEnabled(False)
        self.loginButton.setText('登陆中...')
        self.robber.spider.prepare_login()
        MisUtils.confDict['userName'] = self.inputLine_['userName'].text()
        MisUtils.confDict['password'] = self.inputLine_['password'].text()
        while True:
            result = self.robber.spider.login(MisUtils.confDict['userName'], MisUtils.confDict['password'])
            if result is Spider.NO_SUCH_A_USER:
                self.statusBar().showMessage('用户名不存在')
                break
            elif result is Spider.WRONG_PASSWORD:
                self.statusBar().showMessage('密码错误')
                break
            elif result is Spider.EMPTY_VERTIFY_CODE:
                pass
            elif result is Spider.WRONG_VERTIFY_CODE:
                pass
            elif result is Spider.LOGIN_SUCCESSFULLY:
                self.statusBar().showMessage('登陆成功')
                MisUtils.dumpConfFile()
                break
        self.loginButton.setText('登陆')
        self.loginButton.setEnabled(True)

    @QtCore.pyqtSlot()
    def email_login_button_clicked(self):
        self.emailLoginButton.setEnabled(False)
        self.emailLoginButton.setText('登陆中...')
        for key in list(MisUtils.confDict.keys())[2:]:
            MisUtils.confDict[key] = self.inputLine_[key].text()
        result = Mail.send_mail(String['just_test_connection'], String['test_connection'])
        if result is Mail.HAVE_SEND_A_MAIL:
            MisUtils.dumpConfFile()
            self.statusBar().showMessage(String['have_send_a_mail'])
        elif result is Mail.FAILED_SEND_EMAIL:
            self.statusBar().showMessage(String['failed_send_email'])
        elif result is Mail.CANNOT_HANDLE_DECODE:
            self.statusBar().showMessage(String['cannot_handle_decode'])
        elif result is Mail.HOST_ERROR:
            self.statusBar().showMessage(String['host_error'])
        elif result is Mail.ADDRESS_DOESNT_EXIST:
            self.statusBar().showMessage(String['address_doesnt_exist'])
        self.emailLoginButton.setText('登陆邮箱')
        self.emailLoginButton.setEnabled(True)

    def email_login_button_callback(self):
        self.emailLoginButton.setEnabled(True)

    def rob_report_button_callback(self):
        self.robReportButton.setText('抢报告')
        self.robReportButton.setEnabled(True)
        self.loginButton.setEnabled(True)

    def log_shower_callback(self, content):
        self.logShower.append(content)
        self.logShower.ensureCursorVisible()


def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.setup_ui()
    mainWindow.set_connect()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
