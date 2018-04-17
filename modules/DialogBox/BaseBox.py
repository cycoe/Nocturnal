#!/usr/bin/python
# -*- coding: utf-8 -*-

import re


class BaseBox(object):
    """
    將命令行下常用的對話框封裝成 BaseBox，作爲其他所有類型對話框的基類
    對話框的基本形式如下：
    [標題]
    [提示符]: [輸入]
    """

    def __init__(self, title=None):
        self.title = title
        self.pattern = re.compile('.*')
        self.warning = 'Wrong input pattern!'
        self.prompt = ''
        self.default_output = ''

    def set_title(self, title):
        """
        設置對劃框的標題，一般而言是單獨一行顯示
        標題可以爲 None，則標題行不顯示
        :param title: 標題 String
        :return: self
        """
        self.title = title
        return self

    def set_pattern(self, pattern):
        """
        設置輸入字符串的匹配模式
        :param pattern: 模式字符串
        :return: self
        """
        self.pattern = re.compile(pattern)
        return self

    def set_warning(self, warning):
        """
        設置當輸入模式不匹配時顯示的警告 String
        :param warning: 警告 String
        :return: self
        """
        self.warning = warning
        return self

    def set_default_output(self, default_output):
        self.default_output = default_output
        return self

    def set_prompt(self, prompt):
        """
        設置輸入提示符，即爲 input 函數中的字符串
        :param prompt: 提示符 String
        :return: self
        """
        self.prompt = '> {0}: '.format(prompt)
        return self

    def show(self):
        """
        打印對話框
        :return: 輸入的合法字符串
        """
        # self.title 不爲空則打印標題行
        if self.title:
            print(self.title)

        result = self.input()
        return result

    def input(self):
        """
        處理輸入的匹配問題
        :return: 輸入結果
        """
        while True:
            result = input(self.prompt)
            # 當輸入爲空但缺省輸入非空時，直接返回缺省值，對應不對缺省值進行修改的情況
            if result == '' and self.default_output != '':
                return self.default_output

            # 此處使用 re.fullmatch 函數進行完全匹配
            if re.fullmatch(self.pattern, result):
                break
            else:
                print(self.warning)

        return result
