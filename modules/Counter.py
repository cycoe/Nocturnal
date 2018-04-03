#!/usr/bin/python
# -*- coding: utf-8 -*-

class Counter(object):

    _max_loop = 1
    _current_loop = 0

    @staticmethod
    def set_max_loop(max_loop=1):
        Counter._max_loop = max_loop
        return Counter

    @staticmethod
    def init_current_loop():
        Counter._current_loop = 0
        return Counter

    @staticmethod
    def loop():
        Counter._current_loop += 1
        return Counter._current_loop <= Counter._max_loop

    @staticmethod
    def up_to_max():
        return Counter._current_loop > Counter._max_loop