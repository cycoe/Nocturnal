#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

class Timer(object):

    def __init__(self):
        local_time = time.localtime(time.time())
        self.month = time.strftime('%m', local_time)
        self.day = time.strftime('%d', local_time)
        self.hour = time.strftime('%H', local_time)
        self.minute = time.strftime('%M', local_time)
        self.time = [self.month, self.day, self.hour, self.minute]
