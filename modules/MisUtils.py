#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import time
import os
import re
import sys
import json
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
    timeout = 300                       # 连接超时时间
    maxAttempt = 100					# 最大递归次数
    attempt = maxAttempt

    # wechatGroup_ = ['研究生的咸♂鱼生活']		# 讲座推送的微信群名称
    # wechatUser_ = ['邱大帅全宇宙粉丝后援会']	# 讲座推送的用户名称

    version = 'V 4.0'
    author = 'Cycoe'				# 作者
    platform = platform.system()    # 运行平台
    confFile = 'robber.conf'		# 配置文件路径
    blackList = 'blackList.cache'	# 报告黑名单文件路径
    grade_cache_path = 'grade.cache'    # 成绩缓存文件
    class_cache_path = 'class.cache'    # class keys

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

    signal = {
        'report': False,
        'grade': False,
    }

    status = {
        'report': False,
        'grade': False,
    }


    @staticmethod
    def get_status():
        result = False
        for item in MisUtils.status.values():
            result = result or item
        return result

    @staticmethod
    def check_file_exists(path):
        return os.path.exists(path)

    @staticmethod
    def checkConfFile():
        return os.path.exists(MisUtils.confFile)

    @staticmethod
    def loadConfFile():
        try:
            with open(MisUtils.confFile, 'r') as fp:
                MisUtils.confDict = json.load(fp)
        except json.decoder.JSONDecodeError:
            os.remove(MisUtils.confFile)

    @staticmethod
    def dumpConfFile():
        with open(MisUtils.confFile, 'w') as fp:
            fp.write(json.dumps(MisUtils.confDict, indent=4))

    @staticmethod
    def setEmailInfo():
        if MisUtils.checkConfFile():
            MisUtils.loadConfFile()
        for item in list(MisUtils.confDict.keys())[2:]:
            current = MisUtils.confDict[item]
            while True:
                buffer = input('> ' + String[item] + '(' + String['current'] + ': ' + current + '): ')
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
    def dump_content(content, path):
        with open(path, 'w') as fp:
            fp.write(content)

    @staticmethod
    def load_content(path):
        if not os.path.exists(path):
            return ''
        with open(path, 'r') as fp:
            content = fp.readlines()
        content = '\n'.join(content)
        return content

    @staticmethod
    def dump_list(list_, path):
        with open(path, 'w') as fp:
            fp.write('\n'.join(list_))

    @staticmethod
    def load_list(path):
        list_ = []
        if not os.path.exists(path):
            return list_
        with open(path, 'r') as fp:
            list_ = fp.readlines()
        list_ = [item.strip('\n') for item in list_]
        return list_

    @staticmethod
    def dump_table(table, path):
        table = '\n'.join([', '.join(line) for line in table])
        with open(path, 'w') as fp:
            fp.write(table)

    @staticmethod
    def load_table(path):
        table = []
        if not os.path.exists(path):
            return table
        with open(path, 'r') as fp:
            table = fp.readlines()
        table = [line.split(', ') for line in table]
        table = [[item.strip('\n') for item in line] for line in table]
        return table

    @staticmethod
    def load_dict(path):
        dict_ = {}
        if not os.path.exists(path):
            return dict_
        try:
            with open(path, 'r') as fp:
                dict_ = json.load(fp)
        except json.decoder.JSONDecodeError:
            os.remove(MisUtils.grade_cache_path)

        return dict_

    @staticmethod
    def dump_dict(dict_, path):
        with open(path, 'w') as fp:
            fp.write(json.dumps(dict_, indent=4))
        return True

    @staticmethod
    def table_to_html(table):
        html = [''.join(['<td>' + item + '</td>' for item in line]) for line in table]
        html = ''.join(['<tr>' + line + '</tr>' for line in html])
        html = '<table border="1" bordercolor="#999999" border="1" style="background-color:#F0F0E8;\
        border-color:#999999;font-size:X-Small;width:100%;border-collapse:collapse;">' + html + '</table>'

        return html

    @staticmethod
    def show_qrcode(img_path):
        img = Image.open(img_path)
        img.show()

    @staticmethod
    def wait_animation(wait_method):
        symbol = ['-', '\\', '|', '/']  # 动画显示的符号
        sep = ' '                       # 动画与光标之间的分隔

        while True:
            result = False
            for item in symbol:
                result = wait_method()
                if result:
                    sys.stdout.write(item + sep)
                    sys.stdout.flush()  # 清空缓冲区
                    time.sleep(MisUtils.animationSleep)
                    sys.stdout.write('\b' * (len(item + sep)))
                    sys.stdout.flush()
                else:
                    break
            if not result:
                sys.stdout.write('\n')
                sys.stdout.flush()
                break

    # @staticmethod
    # def wait_animation(sleep_time):
    #     symbol = ['-', '\\', '|', '/']  # 动画显示的符号
    #     sep = ' '                       # 动画与光标之间的分隔
    #
    #     for index in range(int(sleep_time / MisUtils.animationSleep)):
    #         sys.stdout.write(symbol[index % len(symbol)] + sep)
    #         sys.stdout.flush()          # 清空缓冲区
    #         time.sleep(MisUtils.animationSleep)
    #         sys.stdout.write('\b' * (len(symbol[index % len(symbol)] + sep)))
    #         sys.stdout.flush()
