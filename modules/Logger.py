#!/usr/bin/python
# -*- coding: utf-8 -*-

import time


level_ = ['<i>', '<w>', '<e>']


class Logger(object):

    info = 0
    warning = 1
    error = 2

    log_path = 'robber.log'

    @staticmethod
    def log(content, subContent_=None, level=info):
        output = ''
        output += time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
        output += ' ' + level_[level] + ' ' + content
        if subContent_:
            output += '\n'
            subContent_ = ['-> ' + subContent for subContent in subContent_]
            output += '\n'.join(subContent_)

        if level in [Logger.error, Logger.warning]:
            with open(Logger.log_path, 'a') as fr:
                fr.write(output + '\n')

        return output
