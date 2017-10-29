#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

from Config import Config


level_ = ['<info>', '<warning>', '<error>']


class Logger(object):

    info = 0
    warning = 1
    error = 2

    @staticmethod
    def log(content, subContent_=None, level=info):
        if level == 0:
            output = '\033[0m'
        elif level == 1:
            output = '\033[1;34m'
        else:
            output = '\033[1;31m'
        output += time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
        output += ' ' + content
        if subContent_:
            output += '\n'
            subContent_ = ['-> ' + subContent for subContent in subContent_]
            output += '\n'.join(subContent_)
        output += '\033[0m'

        if level == 2:
            with open(Config.logPath, 'a') as fr:
                fr.write(output + '\n')

        return output
