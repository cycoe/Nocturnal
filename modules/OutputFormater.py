#!/usr/bin/python
# -*- coding: utf-8 -*-


class OutputFormater(object):

    left = -1
    center = 0
    right = 1

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

    @staticmethod
    def table(content, gravity=center, padding=0):
        if not content:
            return ''
        maxLength_ = [0 for item in content[0]]
        for row in content:
            for item in row:
                if len(item) + padding > maxLength_[row.index(item)]:
                    maxLength_[row.index(item)] = len(item) + padding
        border = '+'
        for maxLength in maxLength_:
            border += '-' * maxLength
            border += '+'
        border += '\n'

        output_ = []
        for row in content:
            output = '|'
            for item in row:
                length = maxLength_[row.index(item)]
                if gravity == -1:
                    output += item + ' ' * (length - len(item))
                elif gravity == 0:
                    output += ' ' * int((length - len(item)) / 2) + item
                    output += ' ' * int(length - len(item) - int((length - len(item)) / 2))
                elif gravity == 1:
                    output += ' ' * (length - len(item)) + item
                output += '|'
            output += '\n'
            output_.append(output)
        output = border + border.join(output_) + border

        return output
