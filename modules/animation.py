#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time

from .Configer import Config


def wait_animation(wait_method):
    """
    function to output a rotating bar animation during a long time task
    :param wait_method: a method to check wait or break
    :return: None
    """
    frame = ['-', '\\', '|', '/']  # animation frame symbol
    sep = ' '  # separator between symbol and cursor

    while True:
        result = False
        for item in frame:
            result = wait_method()
            if result:
                sys.stdout.write(item + sep)
                sys.stdout.flush()  # 清空缓冲区
                time.sleep(Config.animation_relay)
                sys.stdout.write('\b' * (len(item + sep)))
                sys.stdout.flush()
            else:
                break
        if not result:
            sys.stdout.write('\n')
            sys.stdout.flush()
            break