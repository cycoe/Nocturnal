#!/usr/bin/python
# -*- coding: utf-8 -*-


def find_one_in_list(item_to_find_, list_):
    for item in item_to_find_:
        if item in list_:
            return True
    return False


def is_same_neighbor(list_):
    for index in range(len(list_) - 1):
        if list_[index] == list_[index + 1]:
            return True
    return False
