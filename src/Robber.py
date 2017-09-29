#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from src.Spider import Spider


class Robber(object):

    def __init__(self):
        self.spider = Spider()

        self.loginStatus = False

    def login(self):
        self.spider.jwglLogin(tryNum=100)
        self.loginStatus = True

    def getClassIdList(self, listFile):
        classList = self.spider.fetchClassList()
        print(classList)

    def notifySpeech(self):
        while True:
            availableSpeechList = []
            speechList = self.spider.fetchSpeechList()
            for speech in speechList[1:]:
                if int(speech[8]) < int(speech[7]):
                    availableSpeechList.append(speech)
            if availableSpeechList:
                print(availableSpeechList)
            time.sleep(5)

    def robClass(self, classIdList):
        for classId in classIdList:
            self.spider.postClass(classId)

    def robEnglishTest(self):
        self.spider.getEnglishTest()
        print(self.spider.getEnglishTestStatus())
        self.spider.postEnglishTest()
        print(self.spider.getEnglishTestStatus())
