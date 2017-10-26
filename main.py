#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules.Robber import Robber
from modules.ArgvsParser import ArgvsParser
from modules.OutputFormater import OutputFormater

argvsParser = ArgvsParser()
robber = Robber()


def main():
    outputWelcome()
    cycle()


def cycle():
    while True:
        command = input('>>> ')
        if argvsParser.parse(command) == argvsParser.help:
            outputHelp()
        elif argvsParser.parse(command) == argvsParser.speech:
            robSpeech()
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
        elif argvsParser.parse(command) == argvsParser.quit:
            quit()
        else:
            print("\nWrong arguments detected!\n")


def outputWelcome():
    print("+------------------------+")
    print("|      Class Robber      |")
    print("|        by: cycoe       |")
    print("|    License: MIT 3.0    |")
    print("+------------------------+")
    print("")


def outputHelp():
    print(OutputFormater.table([
        ['command', 'abbr', 'description'],
        ['help', 'h', 'print helps'],
        ['login', 'l', 'login web'],
        ['speech', 's', 'speech robbing mode'],
        ['class', 'c', 'class robbing mode'],
        ['quit', 'q', 'quit robber']
    ], gravity=OutputFormater.center, padding=2))


def login():
    robber.login()


def wechatLogin():
    robber.wechatLogin()


def robAllClass():
    robber.getClassIdList(None)


def notifySpeech():
    robber.notifySpeech()


def robSpeech():
    robber.robSpeech()


def robClass():
    robber.getClassIdList(argvsParser.listFile)


def robEnglish():
    robber.robEnglishTest()


def quit():
    exit(0)


if __name__ == "__main__":
    main()
