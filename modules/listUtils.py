#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import random


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


def filter_with_keys(table_, key_):
    filter_table_ = table_[:]
    for key in key_:
        ori_table_ = filter_table_[:]
        filter_table_ = []
        for line in ori_table_:
            flag = False
            for item in line:
                if re.search(key, item):
                    flag = True
                    break
            if flag:
                filter_table_.append(line)

        if not filter_table_:
            filter_table_ = ori_table_[:]
            break

    return filter_table_


def sort_class(selectable_):
    random.shuffle(selectable_)
    first_index = 0
    wait = True
    for index in range(len(selectable_)):
        if selectable_[index][5] == '未满':
            first_index = index
            wait = False
            break

    return selectable_[first_index][0], wait
