#!/usr/bin/python
# -*- coding: utf-8 -*-

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

    def robClass(self, classIdList):
        for classId in classIdList:
            self.spider.postClass(classId)

    def robEnglishTest(self):
        self.spider.getEnglishTest()
        print(self.spider.getEnglishTestStatus())
        self.spider.postEnglishTest()
        print(self.spider.getEnglishTestStatus())
