#!/usr/bin/python
# -*- coding: utf-8 -*-


def find_all_in_list(itemToFind_, list_):
    for item in itemToFind_:
        if item in list_:
            return True
    return False
