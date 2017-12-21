#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import itchat
import random
import threading

from modules.Spider import Spider
from modules.Logger import Logger
from modules.Mail import Mail
from modules.MisUtils import MisUtils
from modules.String import String


def checkStatus(*check_):
    """
    decorator to check login status before request

    :param check_: a list of status
    :return: function wrapper
    """
    def func_wrapper(func):
        def return_wrapper(self, *args):
            flag = True
            for check in check_:
                flag = flag and check()
            if flag:
                func(self, *args)
            else:
                print(Logger.log(String['login_first'], level=Logger.error))
        return return_wrapper
    return func_wrapper


def getLoginStatus():
    return Robber.loginStatus


def getWechatLoginStatus():
    return Robber.wechatLoginStatus


class Robber(object):

    loginStatus = False
    wechatLoginStatus = False

    def __init__(self):
        self.spider = Spider()

        self.wechatId_ = []

    def login(self):
        self.spider.prepare_login()
        if MisUtils.checkConfFile():
            MisUtils.loadConfFile()

        # 是否需要重新输入用户名和密码
        if MisUtils.confDict['userName'] == '' or MisUtils.confDict['password'] == '':
            reInput = True
        else:
            reInput = False

        while True:
            if reInput:
                MisUtils.confDict['userName'] = input("> " + String['username'])
                MisUtils.confDict['password'] = input("> " + String['password'])
                reInput = False

            result = self.spider.login(MisUtils.confDict['userName'], MisUtils.confDict['password'])
            if result is Spider.NO_SUCH_A_USER:
                reInput = True
            elif result is Spider.WRONG_PASSWORD:
                reInput = True
            elif result is Spider.EMPTY_VERTIFY_CODE:
                pass
            elif result is Spider.WRONG_VERTIFY_CODE:
                pass
            elif result is Spider.LOGIN_SUCCESSFULLY:
                break

    def wechatLogin(self):
        itchat.auto_login(enableCmdQR=2)
        for wechatGroup in MisUtils.wechatGroup_:
            self.wechatId_.append(itchat.search_chatrooms(wechatGroup)[0]['UserName'])
        for wechatUser in MisUtils.wechatUser_:
            self.wechatId_.append(itchat.search_friends(wechatUser)[0]['UserName'])
        Robber.wechatLoginStatus = True

    @staticmethod
    def emailLogin():
        print(Logger.log(String['change_mail']))
        MisUtils.setEmailInfo()
        print(Logger.log(String['sending_a_test_mail'], subContent_=[
            String['check_in_trash_box'],
            String['sender_mail_address'] + MisUtils.confDict['sender'],
            String['nickname'] + 'class_robber'
        ], level=Logger.info))
        Mail.send_mail(String['just_test_connection'], String['test_connection'])
        if Mail.connectedToMail:
            MisUtils.dumpConfFile()

    @checkStatus(getLoginStatus, getWechatLoginStatus)
    def pushToAllGroup(self, msg):
        for wechatId in self.wechatId_:
            itchat.send(msg, toUserName=wechatId)
            time.sleep(MisUtils.wechatPushSleep())

    @checkStatus(getLoginStatus)
    def getClassIdList(self, listFile):
        classList = self.spider.fetchClassList()
        print(classList)

    # @checkStatus(getLoginStatus, getWechatLoginStatus)
    # def notifyReport(self, threshold=3):
    #     # self.pushToAllGroup('开始报告余量监测...')
    #
    #     timePattern = re.compile('(\d{1,2}:\d{2})?:\d{2}')
    #     availableReportListCache = []
    #     while True:
    #         availableReportList = []
    #         reportList = self.spider.fetchReportList()
    #         for row in reportList[1:]:
    #             tempRow = [row[0],
    #                        row[1],
    #                        row[2].split(' ')[0] + ' ' + re.findall(timePattern, row[2].split(' ')[1])[0] + '-' + re.findall(timePattern, row[3].split(' ')[1])[0],
    #                        row[4],
    #                        str(int(row[5]) - int(row[6]))]
    #             if int(tempRow[4]) >= threshold:
    #                 availableReportList.append(tempRow)
    #
    #         if availableReportList and not find_one_in_list([item[1] for item in availableReportList], [item[1] for item in availableReportListCache]):
    #             availableReportListCache = availableReportList[:]
    #             availableReportList.insert(0, ['报告类别', '报告名称', '报告时间', '报告地点', '余量'])
    #             # self.pushToAllGroup(OutputFormater.output(availableReportList, header='有报告余量！'))
    #             print(OutputFormater.table(availableReportList))
    #         time.sleep(MisUtils.refreshSleep())

    # @checkStatus(getLoginStatus)
    def robReport(self):
        MisUtils.status['report'] = True
        while True:
            while True:
                flag = self.spider.fetchReportList()
                if flag:
                    selected_, selectable_ = flag
                else:
                    break
                selectable_ = [selectable for selectable in selectable_ if selectable[2] not in MisUtils.getSelected()]
                buttonId_ = [selectable[0] for selectable in selectable_ if int(selectable[6]) > int(selectable[7])]

                if buttonId_:
                    random.shuffle(buttonId_)
                    buttonId = buttonId_[0]
                    print(Logger.log(String['robbing_report'], level=Logger.warning))
                    flag = self.spider.postReport(buttonId)
                    if not flag:
                        break
                else:
                    print(Logger.log(String['dozing']))
                    MisUtils.wait_animation(MisUtils.refreshSleep())

                new_selected_ = [selected for selected in selected_ if selected[2] not in MisUtils.getSelected()]
                new_selected_item_ = [selected[2] for selected in new_selected_]
                if new_selected_item_:
                    MisUtils.mergeSelected(new_selected_item_)
                    print(Logger.log(String['robbed_new_reports'], subContent_=new_selected_item_, level=Logger.error))
                    selectedHtml = [''.join(['<td>' + item + '</td>' for item in selected]) for selected in new_selected_]
                    selectedHtml = ''.join(['<tr>' + selected + '</tr>' for selected in selectedHtml])
                    selectedHtml = '<table border="1" bordercolor="#999999" border="1" style="background-color:#F0F0E8;\
                    border-color:#999999;font-size:X-Small;width:100%;border-collapse:collapse;">' + selectedHtml + '</table>'
                    if Mail.connectedToMail:
                        threading.Thread(target=Mail.send_mail, args=(String['robbed_new_reports'], selectedHtml,)).start()

                if not MisUtils.signal['report']:
                    MisUtils.status['report'] = False
                    self.clean()
                    return None
            self.clean()
            self.spider.open_session()
            self.login()

    @checkStatus(getLoginStatus)
    def robClass(self, classIdList):
        for classId in classIdList:
            self.spider.postClass(classId)

    @checkStatus(getLoginStatus)
    def robEnglishTest(self):
        self.spider.getEnglishTest()
        print(self.spider.getEnglishTestStatus())
        self.spider.postEnglishTest()
        print(self.spider.getEnglishTestStatus())

    def clean(self):
        self.spider.clean()
