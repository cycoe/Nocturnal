#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time
import itchat
from src.Spider import Spider
from src.OutputFormater import OutputFormater
from Config import Config


class Robber(object):

    def __init__(self):
        self.spider = Spider()
        self.config = Config()

        self.loginStatus = False
        self.speechFlag = False
        self.wechatId_ = []

    def login(self):
        self.spider.jwglLogin()
        self.loginStatus = True

    def wechatLogin(self):
        itchat.auto_login(enableCmdQR=2)
        for wechatGroup in self.config.wechatGroup_:
            self.wechatId_.append(itchat.search_chatrooms(wechatGroup)[0]['UserName'])
        for wechatUser in self.config.wechatUser_:
            self.wechatId_.append(itchat.search_friends(wechatUser)[0]['UserName'])

    def pushToAllGroup(self, msg):
        for wechatId in self.wechatId_:
            itchat.send(msg, toUserName=wechatId)
            time.sleep(self.config.wechatPushSleep())

    def getClassIdList(self, listFile):
        classList = self.spider.fetchClassList()
        print(classList)

    def notifySpeech(self, therhold=5):
        self.pushToAllGroup('开始报告余量监测...')

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
                if int(tempRow[4]) >= therhold:
                    availableSpeechList.append(tempRow)

            if availableSpeechList and len(availableSpeechList) != len(availableSpeechListCache):
                availableSpeechListCache = availableSpeechList[:]
                availableSpeechList.insert(0, ['报告类别', '报告名称', '报告时间', '报告地点', '余量'])
                self.pushToAllGroup(OutputFormater.output(availableSpeechList, header='有报告余量！'))
            time.sleep(self.config.refreshSleep)

    def robClass(self, classIdList):
        for classId in classIdList:
            self.spider.postClass(classId)

    def robEnglishTest(self):
        self.spider.getEnglishTest()
        print(self.spider.getEnglishTestStatus())
        self.spider.postEnglishTest()
        print(self.spider.getEnglishTestStatus())
