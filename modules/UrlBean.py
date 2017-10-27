#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


class UrlBean(object):
    """
    管理爬虫所需的所有 url 的类
    """

    def __init__(self):
        self.userFile = 'password_'

        self.verifyCodeUrl = "http://graduate.buct.edu.cn:8080/pyxx/PageTemplate/NsoftPage/yzm/IdentifyingCode.aspx"  # 验证码获取地址
        self.jwglOriginUrl = "http://graduate.buct.edu.cn:8080"     # origin host
        self.jwglLoginUrl = "http://graduate.buct.edu.cn:8080/pyxx/login.aspx"  # 教务网登录地址
        self.jwglLoginDoneUrl = "http://graduate.buct.edu.cn:8080/pyxx/Default.aspx"  # 教务网登录成功地址
        self.fetchClassListUrl = "http://graduate.buct.edu.cn:8080/pyxx/pygl/pyjhxk.aspx"   # 选课地址
        self.leftMenuReferer = "http://graduate.buct.edu.cn:8080/pyxx/leftmenu.aspx"    # 左侧菜单地址
        self.fetchScheduleUrl = "http://graduate.buct.edu.cn:8080/pyxx/pygl/kbcx_xs.aspx"   # 课程表获取地址
        self.englishTestUrl = "http://graduate.buct.edu.cn:8080/pyxx/grgl/djkssq.aspx"  # 英语等级考试地址
        self.fetchSpeechListUrl = "http://graduate.buct.edu.cn:8080/pyxx/txhdgl/hdlist.aspx"    # 讲座列表获取地址
        self.speechDetailUrl = "http://graduate.buct.edu.cn:8080/pyxx/txhdgl/hdxxdetail.aspx"   # 讲座详情地址
        self.fetchGradeUrl = "http://jwgl.buct.edu.cn/xscjcx.aspx"  # 成绩获取地址

    def checkUserFile(self):
        return os.path.exists(self.userFile)

    def readUserInfo(self):
        with open(self.userFile) as fr:
            content = fr.readlines()
            self.userName = content[0].strip()
            self.password = content[1].strip()

    def dumpUserInfo(self):
        with open(self.userFile, 'w') as fr:
            fr.write(self.userName)
            fr.write('\n')
            fr.write(self.password)

    def cleanUserInfo(self):
        if self.checkUserFile():
            os.remove(self.userFile)
