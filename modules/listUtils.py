#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import random

from modules.FileUtils import check_file_exists
from modules.Config import Config


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
    previous_table_ = filter_table_
    for key in key_:
        filter_table_ = []
        for line in previous_table_:
            flag = False
            for item in line:
                if re.search(key, item):
                    flag = True
                    break
            if flag:
                filter_table_.append(line)

        if not filter_table_:
            if key_.index(key) == 0:
                filter_table_ = []
            else:
                filter_table_ = previous_table_[:]
            break

        previous_table_ = filter_table_[:]

    return filter_table_


def sort_class(selectable_):
    first_index = 0
    wait = True
    for index in range(len(selectable_)):
        if selectable_[index][5] == '未满':
            first_index = index
            wait = False
            break

    return selectable_[first_index][0], wait


def getSelected():
    if check_file_exists(Config.file_name['report_blacklist']):
        with open(Config.file_name['report_blacklist']) as fr:
            return [selected.strip() for selected in fr.readlines()]
    else:
        return []


def mergeSelected(newSelected_):
    if check_file_exists(Config.file_name['report_blacklist']):
        with open(Config.file_name['report_blacklist']) as fr:
            oriSelected_ = [selected.strip() for selected in fr.readlines()]
    else:
        oriSelected_ = []
    oriSelected_.extend(newSelected_)
    oriSelected_ = set(oriSelected_)
    with open(Config.file_name['report_blacklist'], 'w') as fr:
        for oriSelected in oriSelected_:
            fr.write(oriSelected + '\n')
