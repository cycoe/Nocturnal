#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time
import itchat
import random
from modules.Spider import Spider
from modules.OutputFormater import OutputFormater
from modules.Logger import Logger
from modules.listUtils import find_all_in_list
from Config import Config


def checkStatus(check_):
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
    def wrapper():
        return Robber.loginStatus
    return wrapper


def getWechatLoginStatus():
    def wrapper():
        return Robber.wechatLoginStatus
    return wrapper


class Robber(object):

    loginStatus = False
    wechatLoginStatus = False

    def __init__(self):
        self.spider = Spider()

        self.wechatId_ = []

    def login(self):
        self.spider.login()
        Robber.loginStatus = True

    def wechatLogin(self):
        itchat.auto_login(enableCmdQR=2)
        for wechatGroup in Config.wechatGroup_:
            self.wechatId_.append(itchat.search_chatrooms(wechatGroup)[0]['UserName'])
        for wechatUser in Config.wechatUser_:
            self.wechatId_.append(itchat.search_friends(wechatUser)[0]['UserName'])
        Robber.wechatLoginStatus = True

    @checkStatus([getLoginStatus, getWechatLoginStatus])
    def pushToAllGroup(self, msg):
        for wechatId in self.wechatId_:
            itchat.send(msg, toUserName=wechatId)
            time.sleep(Config.wechatPushSleep())

    @checkStatus([getLoginStatus])
    def getClassIdList(self, listFile):
        classList = self.spider.fetchClassList()
        print(classList)

    @checkStatus([getLoginStatus, getWechatLoginStatus])
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

            if availableSpeechList and not find_all_in_list([item[1] for item in availableSpeechList], [item[1] for item in availableSpeechListCache]):
                availableSpeechListCache = availableSpeechList[:]
                availableSpeechList.insert(0, ['报告类别', '报告名称', '报告时间', '报告地点', '余量'])
                # self.pushToAllGroup(OutputFormater.output(availableSpeechList, header='有报告余量！'))
                print(OutputFormater.output(availableSpeechList, header='有报告余量！'))
            time.sleep(Config.refreshSleep())

    @checkStatus([getLoginStatus])
    def robSpeech(self):
        originalNum = 0
        while True:
            selected_, selectable_ = self.spider.fetchSpeechList()
            if len(selected_) > originalNum:
                originalNum = len(selected_)
                print(OutputFormater.output(selected_, header=Logger.log('Robbed a speech!', level=Logger.warning)))
            buttonId_ = [selectable[0] for selectable in selectable_ if int(selectable[6]) > int(selectable[7])]
            if buttonId_:
                random.shuffle(buttonId_)
                buttonId = buttonId_[0]
                print(Logger.log('Robbing speech...', level=Logger.info))
                self.spider.postSpeech(buttonId)
            if len(buttonId_) < 2:
                print(Logger.log('No speech to rob, dozing...', level=Logger.info))
                time.sleep(Config.refreshSleep())

    @checkStatus([getLoginStatus])
    def robClass(self, classIdList):
        for classId in classIdList:
            self.spider.postClass(classId)

    @checkStatus([getLoginStatus])
    def robEnglishTest(self):
        self.spider.getEnglishTest()
        print(self.spider.getEnglishTestStatus())
        self.spider.postEnglishTest()
        print(self.spider.getEnglishTestStatus())

