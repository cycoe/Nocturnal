#!/usr/bin/python
# -*- coding: utf-8 -*-

import random


class Config(object):
    """
    管理配置的类
    """

    def __init__(self):
        self.refreshSleep = 5   # 刷新的间隔时间
        self.wechatPushSleep = getRandomTime(1)     # 发送两条微信消息之间的间隔
        self.wechatGroup_ = []
        #self.wechatGroup_ = ['研究生的咸♂鱼生活']     # 讲座推送的微信群名称
        self.wechatUser_ = ['邱大帅全宇宙粉丝后援会']  # 讲座推送的用户名称


def getRandomTime(sleepTime):

    def wrap():

        return sleepTime + random.random()

    return wrap
