#!/usr/bin/python
# -*- coding: utf-8 -*-

from ._Queue import Queue
from ._Timer import Timer

class Notifier(object):

    # 通知的重复类型
    INSTANT = 0 # 立马通知
    ONCE = 1    # 只通知一次
    REPEAT = 2  # 周期重复

    def __init__(self):
        self.method = lambda: None
        self.tasks_ = [] # 需要通知的任务列表
        self.instant_queue = Queue()

    def bind(self, method):
        """
        绑定通知方法的接口，可传入邮件发送、微信通知等回调函数
        :param method: 通知方法的回调函数
        :return: None
        """
        self.method = method

    def add_tasks(self, get_message, type, delay=5, pattern=None):
        """
        向 Notifier 中新增通知任务
        :param get_message: 获得通知内容的回调方法
        :param type: 通知的重复类型
        :param delay: 通知提前和延迟的时间冗余
        :param pattern: 通知的重复周期 类似于 '* */2 * *' 的格式
        :return:
        """
        self.tasks_.append((get_message, type, delay, pattern, Timer()))
        return True

    def parse(self, pattern, timer, current_timer):
        """
        :param pattern:
        :return:
        """
        pattern_ = pattern.split(' ')
        for rule_index in range(4):
            pass


    def run(self):
        pass

    def cycle(self):
        pass