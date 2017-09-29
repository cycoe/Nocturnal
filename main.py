#!/usr/bin/python
# -*- coding: utf-8 -*-

from src.Robber import Robber
from src.ArgvsParser import ArgvsParser

argvsParser = ArgvsParser()
robber = Robber()


def main():
    outputWelcome()
    cycle()


def cycle():
    while True:
        print(">>> ", end='')
        command = input('')
        if argvsParser.parse(command) == argvsParser.help:
            outputHelp()
        elif argvsParser.parse(command) == argvsParser.speech:
            pass
        elif argvsParser.parse(command) == argvsParser.listClass:
            pass
        elif argvsParser.parse(command) == argvsParser.autoClass:
            robAllClass()
        elif argvsParser.parse(command) == argvsParser.englishTest:
            pass
        elif argvsParser.parse(command) == argvsParser.login:
            login()
        elif argvsParser.parse(command) == argvsParser.wechatLogin:
            wechatLogin()
        elif argvsParser.parse(command) == argvsParser.notifySpeech:
            notifySpeech()
        else:
            print("\nWrong arguments detected!\n")


def outputWelcome():
    print("**************************")
    print("*      Class Robber      *")
    print("*        by: cycoe       *")
    print("*    License: MIT 3.0    *")
    print("**************************")
    print("")


def outputHelp():
    print("\nhelp\t\tprint helps")
    print("speech\t\tspeech robbing mode")
    print("notifySpeech\tnotification with new speech available")
    print("class\t\tclass robbing mode\n")


def login():
    robber.login()


def wechatLogin():
    robber.wechatLogin()


def robAllClass():
    robber.getClassIdList(None)


def notifySpeech():
    robber.notifySpeech()


def robClass():
    robber.getClassIdList(argvsParser.listFile)


def robEnglish():
    robber.robEnglishTest()


if __name__ == "__main__":
    main()
