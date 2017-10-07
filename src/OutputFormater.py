#!/usr/bin/python
# -*- coding: utf-8 -*-


class OutputFormater(object):

    def __init__(self):
        pass

    @staticmethod
    def output(content, header='', footer=''):
        outputContent = ""
        outputContent += header + '\n\n'
        for row in content:
            outputContent += '|'
            for item in range(len(row)):
                outputContent += ' ' + row[item] + ' |'
            outputContent += '\n'
        outputContent += '\n' + footer

        return outputContent

