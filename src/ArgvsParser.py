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

        self.listPattern = re.compile('list=(.*)?')

    def parse(self, command):
            if command == 'help':
                return self.help
            if command == 'speech':
                return self.speech
            if re.search(self.listPattern, command):
                return self.listClass
            if command == 'class':
                return self.autoClass
            if command == 'englishTest':
                return self.englishTest
            if command == 'login':
                return self.login
