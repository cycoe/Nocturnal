#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules.Robber import Robber
from modules.ArgvsParser import ArgvsParser
from modules.OutputFormater import OutputFormater
from modules.Logger import Logger
from modules.MisUtils import MisUtils
from modules.String import String
import pyqrcode

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


def main():
    outputWelcome()
    initArgvs()
    outputHelp()
    cycle()


def initArgvs():
    ArgvsParser.connect(['help', 'h'], outputHelp)
    ArgvsParser.connect(['report', 's'], robReport)
    ArgvsParser.connect(['class', 'c'], robAllClass)
    # ArgvsParser.connect(['englishTest', 'et'], robEnglish)
    ArgvsParser.connect(['login', 'l'], login)
    # ArgvsParser.connect(['notifyReport', 'ns'], notifyReport)
    # ArgvsParser.connect(['wechatLogin', 'wl'], wechatLogin)
    ArgvsParser.connect(['quit', 'q'], quit_)
    ArgvsParser.connect(['emailLogin', 'el'], emailLogin)
    ArgvsParser.connect(['donate', 'd'], printQRCode)


def cycle():
    while True:
        command = input('>>> ')
        if not ArgvsParser.run(command):
            print(Logger.log(String['wrong_argument'], level=Logger.error))


def outputWelcome():
    print(OutputFormater.table([
        ['Class Robber ' + MisUtils.version],
        ['By ' + MisUtils.author],
        ['Site: cycoe.cc'],
        ['License: MIT 3.0']
    ], padding=5, horizontalSpacer=False))


def outputHelp():
    print(OutputFormater.table([
        ['command', 'abbr.', 'description'],
        ['help', 'h', 'print helps'],
        ['login', 'l', 'login web'],
        ['emailLogin', 'el', 'login email to send notification'],
        ['report', 's', 'report robbing mode'],
        # ['class', 'c', 'class robbing mode'],
        ['donate', 'd', 'support developer a cup of coffee'],
        ['quit', 'q', 'quit robber']
    ], gravity=OutputFormater.center, padding=2))


def login():
    robber.login()


def wechatLogin():
    robber.wechatLogin()


def robAllClass():
    robber.getClassIdList(None)


def notifyReport():
    robber.notifyReport()


def robReport():
    robber.robReport()


# def robClass():
#     robber.getClassIdList(argvsParser.listFile)


def robEnglish():
    robber.robEnglishTest()


def emailLogin():
    robber.emailLogin()


def printQRCode():
    wechatURI = pyqrcode.create(MisUtils.wechatURI)
    alipayURI = pyqrcode.create(MisUtils.alipayURI)
    print(Logger.log(String['thanks_to_donate']))
    print(OutputFormater.table([['Via Wechat'], ['|'], ['V']], verticalSpacer=False, horizontalSpacer=False, padding=10))
    print(wechatURI.terminal(quiet_zone=1))
    print(OutputFormater.table([['Via Alipay'], ['|'], ['V']], verticalSpacer=False, horizontalSpacer=False, padding=10))
    print(alipayURI.terminal(quiet_zone=1))


def quit_():
    robber.clean()


if __name__ == "__main__":
    main()
