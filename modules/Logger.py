#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

from Config import Config


level_ = ['<i>', '<w>', '<e>']


class Logger(object):

    info = 0
    warning = 1
    error = 2

    @staticmethod
    def log(content, subContent_=None, level=info):
        output = ''
        output += time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
        output += ' ' + level_[level] + ' ' + content
        if subContent_:
            output += '\n'
            subContent_ = ['-> ' + subContent for subContent in subContent_]
            output += '\n'.join(subContent_)

        if level == 2:
            with open(Config.logPath, 'a') as fr:
                fr.write(output + '\n')

        return output
