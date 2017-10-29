#!/usr/bin/python
# -*- coding: utf-8 -*-


class ArgvsParser(object):

    argvsDict = {}

    @staticmethod
    def run(command):
        try:
            ArgvsParser.argvsDict[command]()
        except KeyError:
            return False
        return True

    @staticmethod
    def connect(command_, func):
        for command in command_:
            ArgvsParser.argvsDict[command] = func


