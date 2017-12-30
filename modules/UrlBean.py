#!/usr/bin/python
# -*- coding: utf-8 -*-


class UrlBean(object):
    """
    管理爬虫所需的所有 url 的类
    """
    
    verifyCodeUrl = "http://graduate.buct.edu.cn:8080/pyxx/PageTemplate/NsoftPage/yzm/IdentifyingCode.aspx"  # 验证码获取地址
    jwglOriginUrl = "http://graduate.buct.edu.cn:8080"     # origin host
    jwglLoginUrl = "http://graduate.buct.edu.cn:8080/pyxx/login.aspx"  # 教务网登录地址
    jwglLoginDoneUrl = "http://graduate.buct.edu.cn:8080/pyxx/Default.aspx"  # 教务网登录成功地址
    fetchClassListUrl = "http://graduate.buct.edu.cn:8080/pyxx/pygl/pyjhxk.aspx"   # 选课地址
    leftMenuReferer = "http://graduate.buct.edu.cn:8080/pyxx/leftmenu.aspx"    # 左侧菜单地址
    fetchScheduleUrl = "http://graduate.buct.edu.cn:8080/pyxx/pygl/kbcx_xs.aspx"   # 课程表获取地址
    englishTestUrl = "http://graduate.buct.edu.cn:8080/pyxx/grgl/djkssq.aspx"  # 英语等级考试地址
    fetchReportListUrl = "http://graduate.buct.edu.cn:8080/pyxx/txhdgl/hdlist.aspx"    # 讲座列表获取地址
    # reportDetailUrl = "http://graduate.buct.edu.cn:8080/pyxx/txhdgl/hdxxdetail.aspx"   # 讲座详情地址
    fetchGradeUrl = "http://graduate.buct.edu.cn:8080/pyxx/grgl/xskccjcx.aspx"  # 成绩获取地址
