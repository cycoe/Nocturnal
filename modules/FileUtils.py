#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json


def check_file_exists(path):
    return os.path.exists(path)


def dump_string(content, path):
    with open(path, 'w') as fp:
        fp.write(content)


def load_string(path):
    if not os.path.exists(path):
        return ''
    with open(path, 'r') as fp:
        content = fp.readlines()
    content = '\n'.join(content)
    return content


def dump_list(list_, path):
    with open(path, 'w') as fp:
        fp.write('\n'.join(list_))


def load_list(path):
    list_ = []
    if not os.path.exists(path):
        return list_
    with open(path, 'r') as fp:
        list_ = fp.readlines()
    list_ = [item.strip('\n') for item in list_]
    return list_


def dump_table(table, path):
    table = '\n'.join([', '.join(line) for line in table])
    with open(path, 'w') as fp:
        fp.write(table)


def load_table(path):
    table = []
    if not os.path.exists(path):
        return table
    with open(path, 'r') as fp:
        table = fp.readlines()
    table = [line.split(', ') for line in table]
    table = [[item.strip('\n') for item in line] for line in table]
    return table


def load_dict(path):
    dict_ = {}
    if not os.path.exists(path):
        return dict_
    try:
        with open(path, 'r') as fp:
            dict_ = json.load(fp)
    except json.decoder.JSONDecodeError:
        os.remove(path)
    return dict_


def dump_dict(dict_, path):
    with open(path, 'w') as fp:
        fp.write(json.dumps(dict_, indent=4))
    return True