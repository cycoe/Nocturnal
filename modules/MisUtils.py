#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import time
import os
import re
import sys
import platform
from PIL import Image
from modules.Logger import Logger
from modules.String import String


def getRandomTime(sleepTime):
    def wrapper():
        return sleepTime * random.random()
    return wrapper


class MisUtils(object):
    """
    管理配置的类
    """

    # 参数设置
    refreshSleep = getRandomTime(10)    # 刷新的间隔时间
    wechatPushSleep = getRandomTime(1)  # 发送两条微信消息之间的间隔
    animationSleep = 0.5                # 等待动画的刷新时间
    timeout = 10                        # 连接超时时间
    maxAttempt = 100					# 最大递归次数
    attempt = maxAttempt

    # wechatGroup_ = ['研究生的咸♂鱼生活']		# 讲座推送的微信群名称
    # wechatUser_ = ['邱大帅全宇宙粉丝后援会']	# 讲座推送的用户名称

    version = 'V 3.0'
    author = 'Cycoe'				# 作者
    platform = platform.system()    # 运行平台
    confFile = 'robber.conf'		# 配置文件路径
    blackList = 'blackList'			# 报告黑名单文件路径

    wechatURI = 'wxp://f2f0PYx27X0CWU1yiBhSKeHHgYzfA27iOicM'    # 微信二维码 URI
    alipayURI = 'HTTPS://QR.ALIPAY.COM/FKX01669SBV7NA4ALTVPE8'  # 支付宝二维码 URI

    confDict = {
        'userName': '',
        'password': '',
        'receiver': '',
        'sender': 'class_robber@cycoe.cc',
        'sender_password': 'class_robber',
        'sender_host': 'smtp.ym.163.com',
        'sender_port': '25',
    }

    pattern = {
        'receiver': '.+@.+(\..+)+',
        'sender': '.+@.+(\..+)+',
        'sender_password': '.*',
        'sender_host': 'smtp(\..+)+',
        'sender_port': '\d+',
    }

    @staticmethod
    def checkConfFile():
        return os.path.exists(MisUtils.confFile)

    @staticmethod
    def loadConfFile():
        with open(MisUtils.confFile) as fr:
            content_ = fr.readlines()
            for content in content_:
                pair_ = content.split(':')
                pair_ = [pair.strip() for pair in pair_]
                if len(pair_) == 2:
                    MisUtils.confDict[pair_[0]] = pair_[1]
                elif len(pair_) == 1:
                    MisUtils.confDict[pair_[0]] = ''

    @staticmethod
    def dumpConfFile():
        with open(MisUtils.confFile, 'w') as fr:
            for key in MisUtils.confDict.keys():
                fr.write(str(key))
                fr.write(': ')
                fr.write(str(MisUtils.confDict[key]))
                fr.write('\n')

    @staticmethod
    def setEmailInfo():
        if MisUtils.checkConfFile():
            MisUtils.loadConfFile()
        for item in list(MisUtils.confDict.keys())[2:]:
            current = MisUtils.confDict[item]
            while True:
                buffer = MisUtils.read_line('> ' + String[item] + '(' + String['current'] + ': ' + current + '): ')
                if not buffer and current:
                    break
                elif re.search(MisUtils.pattern[item], buffer):
                    MisUtils.confDict[item] = buffer
                    break
                else:
                    print(Logger.log(String['check_spell'], level=Logger.warning))

    @staticmethod
    def initAttempt():
        MisUtils.attempt = MisUtils.maxAttempt

    @staticmethod
    def descAttempt():
        MisUtils.attempt -= 1
        return MisUtils.get_attempt()

    @staticmethod
    def get_attempt():
        return MisUtils.attempt > 0

    @staticmethod
    def getSelected():
        if os.path.exists(MisUtils.blackList):
            with open(MisUtils.blackList) as fr:
                return [selected.strip() for selected in fr.readlines()]
        else:
            return []

    @staticmethod
    def mergeSelected(newSelected_):
        if os.path.exists(MisUtils.blackList):
            with open(MisUtils.blackList) as fr:
                oriSelected_ = [selected.strip() for selected in fr.readlines()]
        else:
            oriSelected_ = []
        oriSelected_.extend(newSelected_)
        oriSelected_ = set(oriSelected_)
        with open(MisUtils.blackList, 'w') as fr:
            for oriSelected in oriSelected_:
                fr.write(oriSelected + '\n')

    @staticmethod
    def show_qrcode(img_path):
        img = Image.open(img_path)
        img.show()

    @staticmethod
    def wait_animation(sleep_time):
        symbol = ['-', '\\', '|', '/']  # 动画显示的符号
        sep = ' '                       # 动画与光标之间的分隔
        for index in range(int(sleep_time / MisUtils.animationSleep)):
            sys.stdout.write(symbol[index % len(symbol)] + sep)
            sys.stdout.flush()          # 清空缓冲区
            time.sleep(MisUtils.animationSleep)
            sys.stdout.write('\b' * (len(symbol[index % len(symbol)] + sep)))
            sys.stdout.flush()
