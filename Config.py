#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import os


def getRandomTime(sleepTime):
    def wrapper():
        return sleepTime * (1 + random.random())
    return wrapper


class Config(object):
    """
    管理配置的类
    """

    refreshSleep = getRandomTime(5)   # 刷新的间隔时间
    wechatPushSleep = getRandomTime(1)     # 发送两条微信消息之间的间隔
    maxAttempt = 100
    selected_ = []

    # wechatGroup_ = ['研究生的咸♂鱼生活']     # 讲座推送的微信群名称
    # wechatUser_ = ['邱大帅全宇宙粉丝后援会']  # 讲座推送的用户名称

    attempt = maxAttempt
    logPath = 'robber.log'
    confFile = 'robber.conf'
    blackList = 'blackList'
    sender = 'class_robber@cycoe.win'
    emailPassword = 'class_robber'
    host = 'smtp.ym.163.com'

    confDict = {
        'userName': '',
        'password': '',
        'receiver': '',
    }

    @staticmethod
    def checkConfFile():
        return os.path.exists(Config.confFile)

    @staticmethod
    def loadConfFile():
        with open(Config.confFile) as fr:
            content_ = fr.readlines()
            for content in content_:
                pair_ = content.split(':')
                pair_ = [pair.strip() for pair in pair_]
                if len(pair_) == 2:
                    Config.confDict[pair_[0]] = pair_[1]
                elif len(pair_) == 1:
                    Config.confDict[pair_[0]] = ''

    @staticmethod
    def dumpConfFile():
        with open(Config.confFile, 'w') as fr:
            for key in Config.confDict.keys():
                fr.write(str(key))
                fr.write(': ')
                fr.write(str(Config.confDict[key]))
                fr.write('\n')

    @staticmethod
    def setEmailInfo():
        if Config.checkConfFile():
            Config.loadConfFile()
        Config.confDict['receiver'] = input('> receive email: ')

    @staticmethod
    def initAttempt():
        Config.attempt = Config.maxAttempt

    @staticmethod
    def descAttempt():
        Config.attempt -= 1
        if Config.attempt > 0:
            return True
        else:
            return False

    @staticmethod
    def getSelected():
        if os.path.exists(Config.blackList):
            with open(Config.blackList) as fr:
                return [selected.strip() for selected in fr.readlines()]
        else:
            return []

    @staticmethod
    def mergeSelected(newSelected_):
        if os.path.exists(Config.blackList):
            with open(Config.blackList) as fr:
                oriSelected_ = [selected.strip() for selected in fr.readlines()]
        else:
            oriSelected_ = []
        oriSelected_.extend(newSelected_)
        oriSelected_ = set(oriSelected_)
        with open(Config.blackList, 'w') as fr:
            for oriSelected in oriSelected_:
                fr.write(oriSelected + '\n')

