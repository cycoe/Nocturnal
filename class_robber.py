#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules.Robber import Robber
from modules.ArgvsParser import ArgvsParser
from modules.OutputFormater import OutputFormater
from modules.Logger import Logger
from modules.MisUtils import MisUtils
from modules.String import String
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

def print_(content):
    pass


robber = Robber(print_)


def main():
    outputWelcome()
    initArgvs()
    outputHelp()
    cycle()


def initArgvs():
    ArgvsParser.connect(['help', 'h'], outputHelp)
    ArgvsParser.connect(['report', 'r'], rob_report)
    ArgvsParser.connect(['grade', 'g'], fetch_grade)
    ArgvsParser.connect(['class', 'c'], rob_class)
    ArgvsParser.connect(['quit', 'q'], quit_)
    ArgvsParser.connect(['emailLogin', 'el'], emailLogin)
    ArgvsParser.connect(['donate', 'd'], donate)
    ArgvsParser.connect(['stop'], stop_report)
    ArgvsParser.connect(['status', 's'], get_status)


def cycle():
    while True:
        command = input('[' + str(len([status for status in MisUtils.status.values() if status])) + '] >>> ')
        if not ArgvsParser.run(command):
            print(Logger.log(String['wrong_argument'], level=Logger.warning))


def outputWelcome():
    print(OutputFormater.table([
        ['Class Robber ' + MisUtils.version],
        ['By ' + MisUtils.author],
        ['Site: cycoe.cc'],
        ['GitHub: https://github.com/cycoe/class_robber'],
        ['License: MIT 3.0']
    ], padding=5, horizontalSpacer=False))


def outputHelp():
    print(OutputFormater.table([
        ['command', 'abbr.', 'description'],
        ['help', 'h', 'print helps'],
        ['emailLogin', 'el', 'login email to send notification'],
        ['report', 's', 'report robbing mode'],
        ['donate', 'd', 'support developer a cup of coffee'],
        ['quit', 'q', 'quit robber']
    ], gravity=OutputFormater.center, padding=2))


def rob_report():
    if not MisUtils.status['report']:
        MisUtils.signal['report'] = True
        robber.login()
        threading.Thread(target=robber.robReport, args=(lambda: None,)).start()



def fetch_grade():
    if not MisUtils.status['grade']:
        MisUtils.signal['grade'] = True
        robber.login()
        threading.Thread(target=robber.fetchGrade, args=(lambda: None, lambda x: None,)).start()


def rob_class():
    if not MisUtils.status['class']:
        MisUtils.signal['class'] = True
        robber.rob_class(lambda: None)


def stop_report():
    MisUtils.signal['report'] = False
    MisUtils.signal['grade'] = False
    print(Logger.log('正在关闭所有后台任务... '), end='')
    MisUtils.wait_animation(MisUtils.get_status)


def get_status():
    process = list(MisUtils.status.keys())
    status = ['running' if item else 'stop' for item in list(MisUtils.status.values())]
    print(OutputFormater.table(list(zip(process, status)), gravity=OutputFormater.left, padding=2))


def emailLogin():
    robber.emailLogin()


def donate():
    wechatURI = pyqrcode.create(MisUtils.wechatURI)
    alipayURI = pyqrcode.create(MisUtils.alipayURI)
    wechatURI.png('wechat.png', scale=10)
    alipayURI.png('alipay.png', scale=10)
    print(Logger.log(String['thanks_to_donate'], [
        '1. ' + String['alipay'],
        '2. ' + String['wechat'],
        '3. ' + String['not_now']]))
    while True:
        choice = input('> ')
        if choice == '1':
            MisUtils.show_qrcode('alipay.png')
            print(Logger.log(String['thanks_to_support']))
            break
        elif choice == '2':
            MisUtils.show_qrcode('wechat.png')
            print(Logger.log(String['thanks_to_support']))
            break
        elif choice == '3':
            print(Logger.log(String['remember_to_donate']))
            break
        else:
            print(Logger.log(String['wrong_argument'], level=Logger.warning))


def quit_():
    stop_report()
    robber.clean()
    print(Logger.log(String['site_cleaning'], [String['exiting']], level=Logger.error))
    exit(0)


if __name__ == "__main__":
    main()
