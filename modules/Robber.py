#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import random
import threading

from modules.Spider import Spider
from modules.Logger import Logger
from modules.Mail import Mail
from modules.listUtils import getSelected, mergeSelected, filter_with_keys, sort_class
from modules.Config import Config
from modules.MisUtils import MisUtils
from modules.String import String
from modules.ClassTable import ClassTable
from modules.htmlUtils import table_to_html
from modules.FileUtils import load_table, dump_table
from modules.StatusHandler import StatusHandler


def wait_for_response(sleep_time, get_signal):
    """
    a method to return a random from 0 to sleep time
    :param sleepTime:
    :return: <float> random time
    """
    frame = 1
    sleep_time = sleep_time * random.random()
    count = int(sleep_time/frame)
    for i in range(count):
        if get_signal():
            time.sleep(frame)
        else:
            return True
    return False


# def checkStatus(*check_):
#     """
#     decorator to check login status before request
#
#     :param check_: a list of status
#     :return: function wrapper
#     """
#     def func_wrapper(func):
#         def return_wrapper(self, *args):
#             flag = True
#             for check in check_:
#                 flag = flag and check()
#             if flag:
#                 func(self, *args)
#             else:
#                 self.output(Logger.log(String['login_first'], level=Logger.error))
#         return return_wrapper
#     return func_wrapper


# def getLoginStatus():
#     return Robber.loginStatus


# def getWechatLoginStatus():
#     return Robber.wechatLoginStatus


# def transfer_method(func):
#     """
#     register a method to a transfer method
#     :param func:
#     :return:
#     """
#     def wrapper():
#         func()
#     return wrapper
#
#
# def trigger(func):
#     """
#     register a method to a trigger
#     :param func:
#     :return:
#     """
#     def wrapper():
#         func()
#     return wrapper
#
#
# class Robber(object):
#
#     # status
#     INITIATE = 0
#     NOT_LOGGED = 1
#     LOGGED_IN = 2
#     FETCHED_REPORT = 3
#     ROB_REPORT = 4
#     DOZING = 5
#     STOPPED =6
#
#     TRIGGER_PARA = None
#     TRANSFER_PARA = None
#
#     @staticmethod
#     def trigger_para():
#         return Robber.TRIGGER_PARA
#
#     @staticmethod
#     def transfer_para():
#         return Robber.TRANSFER_PARA
#
#     def __init__(self, output):
#         self.output = output
#         self.init_trigger()
#         self.machine = Machine()
#         self.machine.set_entry(Robber.INITIATE)
#         self.machine.set_exit(Robber.STOPPED)
#         self.machine.set_rule_chain(
#             {
#                 Robber.INITIATE: [(self.always, self.init)],
#                 Robber.NOT_LOGGED: [(self.login_pressed, self.login)],
#                 Robber.LOGGED_IN: [(self.connect_error, self.clean), (self.rob_report_pressed, self.fetch_report)],
#                 Robber.FETCHED_REPORT: [(self.connect_error, self.clean), (self.have_one_report, self.rob_report), (self.no_report, self.dozing)]
#             }
#         )
#
#     def init_trigger(self):
#         self.LOGIN_PRESSED = False
#         self.ROB_REPORT_PRESSED = False
#         self.NO_REPORT =False
#         self.HAVE_ONE_REPORT = False
#         self.HAVE_TWO_REPORT = False
#         self.CONNECT_ERROR = False
#
#     @transfer_method
#     def init(self):
#         self.spider = Spider(self.output)
#         self.machine.status = Robber.NOT_LOGGED
#         self.output("init complete!")
#
#     @transfer_method
#     def login(self):
#         self.spider.prepare_login()
#         if Config.check_config_file():
#             Config.load_user_config()
#
#         # 是否需要重新输入用户名和密码
#         if Config.user['userName'] == '' or Config.user['password'] == '':
#             reInput = True
#         else:
#             reInput = False
#
#         while True:
#             if reInput:
#                 Config.user['userName'] = input("> " + String['username'])
#                 Config.user['password'] = input("> " + String['password'])
#                 reInput = False
#
#             result = self.spider.login(Config.user['userName'], Config.user['password'])
#             if result is Spider.NO_SUCH_A_USER:
#                 reInput = True
#             elif result is Spider.WRONG_PASSWORD:
#                 reInput = True
#             elif result is Spider.EMPTY_VERIFY_CODE:
#                 pass
#             elif result is Spider.WRONG_VERIFY_CODE:
#                 pass
#             elif result is Spider.LOGIN_SUCCESSFULLY:
#                 Config.dump_user_config()
#                 self.machine.status = Robber.LOGGED_IN
#                 self.output("login complete!")
#                 break
#
#     @transfer_method
#     def logout(self):
#         pass
#
#     @transfer_method
#     def fetch_report(self):
#         flag = self.spider.fetchReportList()
#         if flag:
#             selected_, selectable_ = flag
#         else:
#             self.CONNECT_ERROR = True
#             return
#
#         selectable_ = [selectable for selectable in selectable_ if selectable[2] not in getSelected()]
#         buttonId_ = [selectable[0] for selectable in selectable_ if int(selectable[6]) > int(selectable[7])]
#
#         self.TRIGGER_PARA = buttonId_
#         self.machine.status = Robber.FETCHED_REPORT
#
#         if buttonId_:
#             if len(buttonId_) == 1:
#                 self.HAVE_ONE_REPORT = True
#             else:
#                 self.HAVE_TWO_REPORT = True
#
#             random.shuffle(buttonId_)
#             buttonId = buttonId_[0]
#             self.output(Logger.log(String['robbing_report'], level=Logger.warning))
#             flag = self.spider.postReport(buttonId)
#             if not flag:
#                 self.CONNECT_ERROR = True
#                 return
#         else:
#             self.NO_REPORT = True
#         #
#         # new_selected_ = [selected for selected in selected_ if selected[2] not in getSelected()]
#         # new_selected_item_ = [selected[2] for selected in new_selected_]
#
#     @transfer_method
#     def rob_report(self):
#         pass
#
#     @transfer_method
#     def dozing(self):
#         pass
#
#     @transfer_method
#     def clean(self):
#         pass
#
#     @trigger
#     def return_trigger(self, trigger):
#         flag = trigger
#
#     @trigger
#     def always(self):
#         return True
#
#     @trigger
#     def login_pressed(self):
#         return self.LOGIN_PRESSED
#
#     @trigger
#     def rob_report_pressed(self):
#         return self.ROB_REPORT_PRESSED
#
#     @trigger
#     def rob_report(self):
#         pass
#
#     @trigger
#     def no_report(self):
#         pass
#
#     @trigger
#     def have_one_report(self):
#         return self.HAVE_ONE_REPORT
#
#     @trigger
#     def have_two_report(self):
#         return self.HAVE_TWO_REPORT
#
#     @trigger
#     def connect_error(self):
#         return self.CONNECT_ERROR


class Robber(object):

    def __init__(self, output):
        self.output = output
        StatusHandler.add_event('report', False, False)
        StatusHandler.add_event('grade', False, False)

    def init_spider(self):
        self.spider = Spider(self.output)
        return self

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
        Mail.setEmailInfo(lambda item, current: input('> ' + String[item] + '(' + String['current'] + ': ' + current + '): '), print)
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
        StatusHandler.status['report'] = True
        while True:
            while True:
                flag = self.spider.fetchReportList()
                if flag:
                    selected_, selectable_ = flag
                else:
                    break
                selectable_ = [selectable for selectable in selectable_ if selectable[2] not in getSelected()]
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
                    if wait_for_response(Config.report_refresh_relay, StatusHandler.get_signal('report')):
                        break

                new_selected_ = [selected for selected in selected_ if selected[2] not in getSelected()]
                new_selected_item_ = [selected[2] for selected in new_selected_]
                if new_selected_item_:
                    mergeSelected(new_selected_item_)
                    self.output(Logger.log(String['robbed_new_reports'], subContent_=new_selected_item_, level=Logger.error))
                    selectedHtml = table_to_html(new_selected_)
                    if Mail.CONNECTED_TO_MAIL:
                        threading.Thread(target=Mail.send_mail, args=(String['robbed_new_reports'], selectedHtml,)).start()

            if not StatusHandler.signal['report']:
                StatusHandler.status['report'] = False
                self.clean()
                break

            self.clean()
            self.spider.open_session()
            result = self.spider.login(Config.user['userName'], Config.user['password'])
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

                class_key = load_table(Config.file_name['class_key_cache'])
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
                    time.sleep(Config.class_refresh_relay)

            self.clean()
            self.spider.open_session()
            result = self.spider.login(Config.user['userName'], Config.user['password'])
            if result is Spider.NO_SUCH_A_USER or result is Spider.WRONG_PASSWORD:
                self.clean()
                break

        return False

    def fetchGrade(self, callback, output):
        StatusHandler.status['grade'] = True
        while True:
            while True:
                flag = self.spider.fetchGrade()
                if flag:
                    grade = flag
                else:
                    break

                new_grade = [line for line in grade if line not in load_table(Config.file_name['grade_cache'])]
                if new_grade:
                    output(new_grade)
                    dump_table(grade, Config.file_name['grade_cache'])
                    if Mail.CONNECTED_TO_MAIL:
                        new_grade.insert(0, ['课程', '课程学分', '选修学期', '成绩'])
                        grade_html = table_to_html(new_grade)
                        threading.Thread(target=Mail.send_mail, args=('Fetched new grade', grade_html,)).start()

                else:
                    if wait_for_response(Config.grade_refresh_relay, StatusHandler.get_signal('grade')):
                        break

            if not StatusHandler.signal['grade']:
                StatusHandler.status['grade'] = False
                self.clean()
                break

            self.clean()
            self.spider.open_session()
            result = self.spider.login(Config.user['userName'], Config.user['password'])
            if result is Spider.NO_SUCH_A_USER or result is Spider.WRONG_PASSWORD:
                StatusHandler.status['grade'] = False
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


