import numpy as np
import os
import math

# from modules.Node import Node


def sigmoid(sigma):
    """
    sigmoid 激活函数

    :param sigma: 求和值
    :return: 激活值
    """
    return 1.0 / (1 + math.exp(- sigma))


def norm2(point):
    """
    欧几里得范数

    :param point: 输出向量
    :return: 范数值
    """
    return np.vdot(point, point)


def classify(output, tag1, tag2):
    """
    分类函数
    :param output: 输出向量
    :param tag1: 类别 1 的向量
    :param tag2: 类别 2 的向量
    :return: 类别
    """
    if norm2(output - tag1) > norm2(output - tag2):
        return tag2
    else:
        return tag1


class Network(object):

    def __init__(self):
        self.weight_ = []
        self.output_ = []
        self.matrix_ = []
        self.tag_ = []

    def load_matrix(self, matrix_=np.array([[1, 2, 3],
                                            [-1, 3, 4],
                                            [2, 5, 2]])):
        self.matrix_ = matrix_

    def load_tag(self,tag_=np.array([[1, 0],
                                     [0, 1],
                                     [0, 0]])):
        self.tag_ = tag_

    def set_structure(self, structure):
        if len(structure) <= 2:
            return False
        for index in range(len(structure) - 1):
            self.weight_.append(np.random.random((structure[index + 1], structure[index])))
        return True

    def forward(self):
        pass