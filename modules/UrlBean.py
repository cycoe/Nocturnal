#!/usr/bin/python
# -*- coding: utf-8 -*-


class UrlBean(object):
    """
    管理爬虫所需的所有 url 的类
    """

    jwglOriginUrl = "http://202.4.152.190:8080"  # origin host
    verifyCodeUrl = jwglOriginUrl + "/pyxx/PageTemplate/NsoftPage/yzm/IdentifyingCode.aspx"  # 验证码获取地址
    jwglLoginUrl = jwglOriginUrl + "/pyxx/login.aspx"  # 教务网登录地址
    jwglLoginDoneUrl = jwglOriginUrl + "/pyxx/Default.aspx"  # 教务网登录成功地址
    fetchClassListUrl = jwglOriginUrl + "/pyxx/pygl/pyjhxk.aspx"   # 选课地址
    leftMenuReferer = jwglOriginUrl + "/pyxx/leftmenu.aspx"    # 左侧菜单地址
    fetchScheduleUrl = jwglOriginUrl + "/pyxx/pygl/kbcx_xs.aspx"   # 课程表获取地址
    englishTestUrl = jwglOriginUrl + "/pyxx/grgl/djkssq.aspx"  # 英语等级考试地址
    fetchReportListUrl = jwglOriginUrl + "/pyxx/txhdgl/hdlist.aspx"    # 讲座列表获取地址
    # reportDetailUrl = "http://graduate.buct.edu.cn:8080/pyxx/txhdgl/hdxxdetail.aspx"   # 讲座详情地址
    fetchGradeUrl = jwglOriginUrl + "/pyxx/grgl/xskccjcx.aspx"  # 成绩获取地址
