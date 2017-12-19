#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules.Robber import Robber
from modules.Logger import Logger
from modules.MisUtils import MisUtils
from modules.String import String
from tkinter import *
import pyqrcode
import threading


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


robber = Robber()


class Gui(object):

    def __init__(self):
        self.window = Tk()

    def set_property(self):
        self.window.title('Class Robber')
        self.window.geometry('800x600')

    def add_elements(self):
        li = ['C', 'python', 'php', 'html', 'SQL', 'java']
        movie = ['CSS', 'jQuery', 'Bootstrap']
        listb = Listbox(self.window)  # 创建两个列表组件
        listb2 = Listbox(self.window)
        for item in li:  # 第一个小部件插入数据
            listb.insert(0, item)

        for item in movie:  # 第二个小部件插入数据
            listb2.insert(0, item)

        listb.pack()  # 将小部件放置到主窗口中
        listb2.pack()
        self.window.mainloop()  # 进入消息循环


def main():
    gui = Gui()
    gui.set_property()
    gui.add_elements()


if __name__ == '__main__':
    main()
