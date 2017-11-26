#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time
import itchat
import random
import threading

from modules.Spider import Spider
from modules.OutputFormater import OutputFormater
from modules.Logger import Logger
from modules.Mail import Mail
from modules.listUtils import find_one_in_list
from modules.MisUtils import MisUtils


def checkStatus(*check_):
    """
    decorator to check login status before request

    :param check_: a list of status
    :return: function wrapper
    """
    def func_wrapper(func):
        def return_wrapper(self, *args):
            flag = True
            for check in check_:
                flag = flag and check()
            if flag:
                func(self, *args)
            else:
                print(Logger.log('Login first!', level=Logger.error))
        return return_wrapper
    return func_wrapper


def getLoginStatus():
    return Robber.loginStatus


def getWechatLoginStatus():
    return Robber.wechatLoginStatus


class Robber(object):

    loginStatus = False
    wechatLoginStatus = False

    def __init__(self):
        self.spider = Spider()

        self.wechatId_ = []

    def login(self):
        Robber.loginStatus = self.spider.login()

    def wechatLogin(self):
        itchat.auto_login(enableCmdQR=2)
        for wechatGroup in MisUtils.wechatGroup_:
            self.wechatId_.append(itchat.search_chatrooms(wechatGroup)[0]['UserName'])
        for wechatUser in MisUtils.wechatUser_:
            self.wechatId_.append(itchat.search_friends(wechatUser)[0]['UserName'])
        Robber.wechatLoginStatus = True

    def emailLogin(self):
        MisUtils.setEmailInfo()
        print(Logger.log('Sending a test mail to your mailbox...', subContent_=[
            'Check the trash box if you haven\'t received the test mail',
            'Sender mail address: class_robber@cycoe.win',
            'Nick name: class_robber'
        ], level=Logger.info))
        Mail.send_mail('Just test connection.', 'Test connection between class robber and mail server. No reply')

    @checkStatus(getLoginStatus, getWechatLoginStatus)
    def pushToAllGroup(self, msg):
        for wechatId in self.wechatId_:
            itchat.send(msg, toUserName=wechatId)
            time.sleep(MisUtils.wechatPushSleep())

    @checkStatus(getLoginStatus)
    def getClassIdList(self, listFile):
        classList = self.spider.fetchClassList()
        print(classList)

    @checkStatus(getLoginStatus, getWechatLoginStatus)
    def notifySpeech(self, threshold=3):
        # self.pushToAllGroup('开始报告余量监测...')

        timePattern = re.compile('(\d{1,2}:\d{2})?:\d{2}')
        availableSpeechListCache = []
        while True:
            availableSpeechList = []
            speechList = self.spider.fetchSpeechList()
            for row in speechList[1:]:
                tempRow = [row[0],
                           row[1],
                           row[2].split(' ')[0] + ' ' + re.findall(timePattern, row[2].split(' ')[1])[0] + '-' + re.findall(timePattern, row[3].split(' ')[1])[0],
                           row[4],
                           str(int(row[5]) - int(row[6]))]
                if int(tempRow[4]) >= threshold:
                    availableSpeechList.append(tempRow)

            if availableSpeechList and not find_one_in_list([item[1] for item in availableSpeechList], [item[1] for item in availableSpeechListCache]):
                availableSpeechListCache = availableSpeechList[:]
                availableSpeechList.insert(0, ['报告类别', '报告名称', '报告时间', '报告地点', '余量'])
                # self.pushToAllGroup(OutputFormater.output(availableSpeechList, header='有报告余量！'))
                print(OutputFormater.table(availableSpeechList))
            time.sleep(MisUtils.refreshSleep())

    @checkStatus(getLoginStatus)
    def robSpeech(self):
        # while True:
        #     flag = self.spider.fetchSpeechList()
        #     if flag:
        #         selectedHtml, selected_, selectable_ = flag
        #         selectable_ = [selectable for selectable in selectable_ if selectable[2] not in MisUtils.getSelected()]
        #     else:
        #         return None
        #     buttonId_ = [selectable[0] for selectable in selectable_ if int(selectable[6]) > int(selectable[7])]
        #     if buttonId_:
        #         random.shuffle(buttonId_)
        #         buttonId = buttonId_[0]
        #         print(Logger.log('Robbing speech...', level=Logger.warning))
        #         flag = self.spider.postSpeech(buttonId)
        #         if not flag:
        #             return None
        #     newSelected_ = [selected[2] for selected in selected_ if selected[2] not in MisUtils.getSelected()]
        #     if newSelected_:
        #         MisUtils.mergeSelected(newSelected_)
        #         print(Logger.log('Robbed a speech!', subContent_=newSelected_, level=Logger.error))
        #         if Mail.connectedToMail:
        #             threading.Thread(target=Mail.send_mail, args=('Robbed a new speech', selectedHtml,)).start()
        #     if len(buttonId_) < 2:
        #         print(Logger.log('No speech to rob, dozing...', level=Logger.info))
        #         time.sleep(MisUtils.refreshSleep())

        selectedHtml, selected_, selectable_ = self.spider.fetchSpeechList()
        selectable_ = [selectable for selectable in selectable_ if selectable[2] not in MisUtils.getSelected()]
        buttonId_ = [selectable[0] for selectable in selectable_ if int(selectable[6]) > int(selectable[7])]
        while True:
            if buttonId_:
                random.shuffle(buttonId_)
                buttonId = buttonId_[0]
                print(Logger.log('Robbing speech...', level=Logger.warning))
                selectedHtml, selected_, selectable_ = self.spider.postSpeech(buttonId)
                selectable_ = [selectable for selectable in selectable_ if selectable[2] not in MisUtils.getSelected()]
            else:
                selectedHtml, selected_, selectable_ = self.spider.fetchSpeechList()
                selectable_ = [selectable for selectable in selectable_ if selectable[2] not in MisUtils.getSelected()]
            newSelected_ = [selected[2] for selected in selected_ if selected[2] not in MisUtils.getSelected()]
            if newSelected_:
                MisUtils.mergeSelected(newSelected_)
                print(Logger.log('Robbed a speech!', subContent_=newSelected_, level=Logger.error))
                if Mail.connectedToMail:
                    threading.Thread(target=Mail.send_mail, args=('Robbed a new speech', selectedHtml,)).start()
            buttonId_ = [selectable[0] for selectable in selectable_ if int(selectable[6]) > int(selectable[7])]
            if not buttonId_:
                print(Logger.log('No speech to rob, dozing...', level=Logger.info))
                time.sleep(MisUtils.refreshSleep())

    @checkStatus(getLoginStatus)
    def robClass(self, classIdList):
        for classId in classIdList:
            self.spider.postClass(classId)

    @checkStatus(getLoginStatus)
    def robEnglishTest(self):
        self.spider.getEnglishTest()
        print(self.spider.getEnglishTestStatus())
        self.spider.postEnglishTest()
        print(self.spider.getEnglishTestStatus())

    def clean(self):
        self.spider.clean()
        print(Logger.log('Site clearing...', ['exiting...'], level=Logger.error))
        exit(0)

