#!/usr/bin/python
# -*- coding: utf-8 -*-


class OutputFormater(object):

    def __init__(self, content):
        self.content = content
        self.header = ''
        self.footer = ''

    def setHeader(self, header):
        self.header = header

        return self

    def setFooter(self, footer):
        self.footer = footer

        return self

    def output(self):
        outputContent = ""
        outputContent += self.header + '\n\n'
        for row in self.content:
            outputContent += '|'
            for item in range(len(row)):
                outputContent += ' ' + row[item] + ' |'
            outputContent += '\n'
        outputContent += '\n' + self.footer

        return outputContent

