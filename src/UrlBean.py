#!/usr/bin/python
# -*- coding: utf-8 -*-


class UrlBean(object):

    def __init__(self):

        self.studentID = "2017200276"
        self.jwglPassword = "zhiwen.COM"
        # self.username = #姓名
        # self.major = '0202高分子材料与工程'

        self.verifyCodeUrl = "http://graduate.buct.edu.cn:8080/pyxx/PageTemplate/NsoftPage/yzm/IdentifyingCode.aspx"  # 验证码获取地址
        self.jwglOriginUrl = "http://graduate.buct.edu.cn:8080"
        self.jwglLoginUrl = "http://graduate.buct.edu.cn:8080/pyxx/login.aspx"  # 教务网登录地址
        self.jwglLoginDoneUrl = "http://graduate.buct.edu.cn:8080/pyxx/Default.aspx"  # 教务网登录成功地址
        self.fetchClassListUrl = "http://graduate.buct.edu.cn:8080/pyxx/pygl/pyjhxk.aspx"   # 选课地址
        self.leftMenuReferer = "http://graduate.buct.edu.cn:8080/pyxx/leftmenu.aspx"    # 左侧菜单地址
        self.fetchScheduleUrl = "http://graduate.buct.edu.cn:8080/pyxx/pygl/kbcx_xs.aspx"   # 课程表获取地址
        self.englishTestUrl = "http://graduate.buct.edu.cn:8080/pyxx/grgl/djkssq.aspx"  # 英语等级考试地址
        self.fetchSpeechListUrl = "http://graduate.buct.edu.cn:8080/pyxx/txhdgl/hdlist.aspx"    # 讲座列表获取地址
        self.fetchGradeUrl = "http://jwgl.buct.edu.cn/xscjcx.aspx"  # 成绩获取地址
