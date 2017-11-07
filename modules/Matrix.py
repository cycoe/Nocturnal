#!/usr/bin/python
# -*- coding: utf-8 -*-


def add(matrix1, matrix2):
    """

    :param matrix1: Matrix object
    :param matrix2: Matrix object
    :return: result Matrix
    """
    pass


class Matrix(object):

    def __init__(self, data):
        self.data = data

    def shape(self):
        return len(self.data), len(self.data[0])
