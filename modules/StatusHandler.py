#!/usr/bin/python
# -*- coding: utf-8 -*-


class StatusHandler(object):

    status = {}
    signal = {}

    @staticmethod
    def add_event(event, status, signal):
        """
        :param name:
        :param status:
        :param signal:
        :return:
        """
        StatusHandler.status[event] = status
        StatusHandler.signal[event] = signal

    @staticmethod
    def get_status(event):
        def wrapper():
            return StatusHandler.status[event]
        return wrapper

    @staticmethod
    def get_signal(event):
        def wrapper():
            return StatusHandler.signal[event]
        return wrapper