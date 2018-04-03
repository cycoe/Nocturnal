#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

from modules.Config import Config


class Machine(object):
    """Status Machine"""

    def __init__(self):
        self.status = None  # status handler
        self.exit = None  # exit status
        self.chain = None  # rule chain

    def set_entry(self, status):
        """
        set the initiate status as an entry
        :param status: initiate status
        :return self: <Machine>
        """
        self.status = status
        return self

    def set_exit(self, exit):
        self.exit = exit

    def set_rule_chain(self, chain):
        """
        set a rule chain (a 3-dim dict)
        there's a regular structure of rule chain below

        chain = {
            status 1: [(trigger1, method1), (trigger2, method2)],
            status 2: [(trigger3, method3), (trigger4, method4)],
        }

        1. rule chain composed with several status that the Machine can stay in
        2. every status is onto a list of tuples
        3. tuple is composed with a trigger and a method
        4. trigger is our input or a condition that in such a status Machine can receive
        5. method is executed when a trigger is activated
        6. triggers in a list is sorted by its priority

        :param chain: rule chain
        :return self: <Machine>
        """
        self.chain = chain
        return self

    def run(self):
        while True:
            for trigger, method in self.chain[self.status]:
                if trigger():
                    self.status = method()
                    break
            if self.status == self.exit:
                break
            time.sleep(Config.machine_relay)
