#!/usr/bin/python
# -*- coding: utf-8 -*-

import re


class ArgvsParser(object):

    def __init__(self):

        self.help = 0
        self.speech = 1
        self.autoClass = 2
        self.listClass = 3
        self.englishTest = 4
        self.login = 5
        self.notifySpeech = 6
        self.wechatLogin = 7
        self.quit = 8

        self.listPattern = re.compile('list=(.*)?')

    def parse(self, command):
            if command in ['help', 'h']:
                return self.help
            if command in ['speech', 's']:
                return self.speech
            if re.search(self.listPattern, command):
                return self.listClass
            if command in ['class', 'c']:
                return self.autoClass
            if command in ['englishTest', 'et']:
                return self.englishTest
            if command in ['login', 'l']:
                return self.login
            if command in ['notifySpeech', 'ns']:
                return self.notifySpeech
            if command in ['wechatLogin', 'wl']:
                return self.wechatLogin
            if command in ['quit', 'q']:
                return self.quit
