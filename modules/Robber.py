#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import random
import threading

from modules.Spider import Spider
from modules.Logger import Logger
from modules.Mail import Mail
from modules.Config import Config
from modules.MisUtils import MisUtils
from modules.String import String
from modules.ClassTable import ClassTable
from modules.listUtils import filter_with_keys, sort_class


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
                self.output(Logger.log(String['login_first'], level=Logger.error))
        return return_wrapper
    return func_wrapper


def getLoginStatus():
    return Robber.loginStatus


def getWechatLoginStatus():
    return Robber.wechatLoginStatus


class Robber(object):

    loginStatus = False
    wechatLoginStatus = False

    def __init__(self, output):
        self.spider = Spider(output)
        self.output = output

        self.wechatId_ = []

    def login(self):
        self.spider.prepare_login()
        if Config.check_config_file():
            Config.load_user_config()

        # 是否需要重新输入用户名和密码
        if Config.user['userName'] == '' or Config.user['password'] == '':
            reInput = True
        else:
            reInput = False

        while True:
            if reInput:
                Config.user['userName'] = input("> " + String['username'])
                Config.user['password'] = input("> " + String['password'])
                reInput = False

            result = self.spider.login(Config.user['userName'], Config.user['password'])
            if result is Spider.NO_SUCH_A_USER:
                reInput = True
            elif result is Spider.WRONG_PASSWORD:
                reInput = True
            elif result is Spider.EMPTY_VERIFY_CODE:
                pass
            elif result is Spider.WRONG_VERIFY_CODE:
                pass
            elif result is Spider.LOGIN_SUCCESSFULLY:
                Config.dump_user_config()
                break

    # def wechatLogin(self):
    #     itchat.auto_login(enableCmdQR=2)
    #     for wechatGroup in MisUtils.wechatGroup_:
    #         self.wechatId_.append(itchat.search_chatrooms(wechatGroup)[0]['UserName'])
    #     for wechatUser in MisUtils.wechatUser_:
    #         self.wechatId_.append(itchat.search_friends(wechatUser)[0]['UserName'])
    #     Robber.wechatLoginStatus = True

    def emailLogin(self):
        self.output(Logger.log(String['change_mail']))
        MisUtils.setEmailInfo()
        self.output(Logger.log(String['sending_a_test_mail'], subContent_=[
            String['check_in_trash_box'],
            String['sender_mail_address'] + Config.user['sender'],
            String['nickname'] + 'class_robber'
        ], level=Logger.info))
        Mail.send_mail(String['just_test_connection'], String['test_connection'])
        if Mail.CONNECTED_TO_MAIL:
            Config.dump_user_config()

    # @checkStatus(getLoginStatus, getWechatLoginStatus)
    # def pushToAllGroup(self, msg):
    #     for wechatId in self.wechatId_:
    #         itchat.send(msg, toUserName=wechatId)
    #         time.sleep(MisUtils.wechatPushSleep())

    # @checkStatus(getLoginStatus)
    # def getClassIdList(self, listFile):
    #     classList = self.spider.fetchClassList()
    #     self.output(classList)

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
    #             self.output(OutputFormater.table(availableReportList))
    #         time.sleep(MisUtils.refreshSleep())

    # @checkStatus(getLoginStatus)
    def robReport(self, callback):
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
                    self.output(Logger.log(String['robbing_report'], level=Logger.warning))
                    flag = self.spider.postReport(buttonId)
                    if not flag:
                        break
                else:
                    self.output(Logger.log(String['dozing']))
                    time.sleep(MisUtils.refreshSleep())

                new_selected_ = [selected for selected in selected_ if selected[2] not in MisUtils.getSelected()]
                new_selected_item_ = [selected[2] for selected in new_selected_]
                if new_selected_item_:
                    MisUtils.mergeSelected(new_selected_item_)
                    self.output(Logger.log(String['robbed_new_reports'], subContent_=new_selected_item_, level=Logger.error))
                    selectedHtml = MisUtils.table_to_html(new_selected_)
                    if Mail.connectedToMail:
                        threading.Thread(target=Mail.send_mail, args=(String['robbed_new_reports'], selectedHtml,)).start()

                if not MisUtils.signal['report']:
                    break

            if not MisUtils.signal['report']:
                MisUtils.status['report'] = False
                self.clean()
                break

            self.clean()
            self.spider.open_session()
            result = self.spider.login(MisUtils.confDict['userName'], MisUtils.confDict['password'])
            if result is Spider.NO_SUCH_A_USER or result is Spider.WRONG_PASSWORD:
                MisUtils.status['report'] = False
                self.clean()
                break
        callback()

    def rob_class(self):
        while True:
            while True:
                flag = self.spider.fetchClassList()
                if flag is not False:
                    selectable_, selected_ = flag
                else:
                    break

                ClassTable.init_table()
                ClassTable.create_table(selectable_)

                class_key = MisUtils.load_table(MisUtils.class_cache_path)
                temp_selectable_ = []
                for key in class_key:
                    temp_selectable_.extend(filter_with_keys(selectable_, key))
                filter_selectable_ = []
                for line in temp_selectable_:
                    if line not in filter_selectable_:
                        filter_selectable_.append(line)

                if not filter_selectable_:
                    print(Logger.log('No class to rob', subContent_=['exiting...'], level=Logger.error))
                    return True
                print(filter_selectable_)

                button_id, wait = sort_class(filter_selectable_)
                print(button_id)
                print(Logger.log('Robbing class...', level=Logger.warning))
                flag = self.spider.postClass(button_id)
                if not flag:
                    break
                if wait:
                    print(Logger.log('dozing...', level=Logger.info))
                    time.sleep(MisUtils.refreshSleep())

            self.clean()
            self.spider.open_session()
            result = self.spider.login(MisUtils.confDict['userName'], MisUtils.confDict['password'])
            if result is Spider.NO_SUCH_A_USER or result is Spider.WRONG_PASSWORD:
                self.clean()
                break

        return False

    def fetchGrade(self, callback, output):
        MisUtils.status['grade'] = True
        while True:
            while True:
                flag = self.spider.fetchGrade()
                if flag:
                    grade = flag
                else:
                    break

                new_grade = [line for line in grade if line not in MisUtils.load_table(MisUtils.grade_cache_path)]
                if new_grade:
                    output(new_grade)
                    MisUtils.dump_table(grade, MisUtils.grade_cache_path)
                    if Mail.connectedToMail:
                        new_grade.insert(0, ['课程', '课程学分', '选修学期', '成绩'])
                        grade_html = MisUtils.table_to_html(new_grade)
                        threading.Thread(target=Mail.send_mail, args=('Fetched new grade', grade_html,)).start()

                else:
                    time.sleep(10)

                if not MisUtils.signal['grade']:
                    break

            if not MisUtils.signal['grade']:
                MisUtils.status['grade'] = False
                self.clean()
                break

            self.clean()
            self.spider.open_session()
            result = self.spider.login(MisUtils.confDict['userName'], MisUtils.confDict['password'])
            if result is Spider.NO_SUCH_A_USER or result is Spider.WRONG_PASSWORD:
                MisUtils.status['grade'] = False
                self.clean()
                break
        callback()

    # @checkStatus(getLoginStatus)
    # def robEnglishTest(self):
    #     self.spider.getEnglishTest()
    #     self.output(self.spider.getEnglishTestStatus())
    #     self.spider.postEnglishTest()
    #     self.output(self.spider.getEnglishTestStatus())

    def clean(self):
        self.spider.clean()
