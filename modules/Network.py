#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np


def sigmoid(sigma):
    """
    sigmoid 激活函数

    :param sigma: 求和值
    :return: 激活值
    """
    return 1.0 / (1 + np.exp(- sigma))


def norm2(point):
    """
    欧几里得范数

    :param point: 输出向量
    :return: 范数值
    """
    return np.vdot(point, point)


def classify(output, tag_set):
    """
    分类函数
    :param output: 输出向量
    :param tag_set: 类别向量的集合
    :return: 类别
    """
    min_index = 0
    for i in range(len(tag_set)):
        if norm2(output - tag_set[i]) < norm2(output - tag_set[min_index]):
            min_index = i
    return tag_set[min_index]


class Network(object):

    def __init__(self):
        self.structure = []
        self.weight_ = []
        self.x_ = []
        self.matrix_ = []
        self.tag_ = []
        self.delta_ = []
        self.rate = 0.9

    def load_matrix(self, matrix_=np.array([[1, 2, 3],
                                            [-1, 3, 4],
                                            [2, 5, 2]])):
        self.matrix_ = matrix_
        return self

    def load_tag(self, tag_=np.array([[1],
                                      [0],
                                      [1]])):
        self.tag_ = tag_
        return self

    def set_structure(self, structure):
        structure.insert(0, len(self.matrix_[0]))
        structure.append(len(self.tag_[0]))
        for index in range(len(structure) - 1):
            self.weight_.append(np.random.random((structure[index + 1], structure[index])) * 2 - 1)
        self.structure = structure
        self.x_ = [0 for i in range(len(self.structure))]
        self.delta_ = [0 for i in range(len(self.structure) - 1)]
        return self

    def forward(self, sample_index):
        for index in range(len(self.structure)):
            if index == 0:
                self.x_[index] = np.reshape(self.matrix_[sample_index], (self.structure[index], 1))
            else:
                self.x_[index] = np.reshape(sigmoid(np.dot(self.weight_[index - 1], self.x_[index - 1])), (self.structure[index], 1))
        # print(self.x_)
        # print(self.weight_)
        return self

    def backward(self, sample_index):
        for index in range(len(self.structure) - 2, -1, -1):
            output = self.x_[index + 1]
            if index == len(self.structure) - 2:
                delta = np.reshape((self.tag_[sample_index] - output) * output * (1 - output), (self.structure[index + 1], 1))
            else:
                delta = np.reshape(output * (1 - output) * np.dot(self.weight_[index + 1].T, self.delta_[index + 1]), (self.structure[index + 1], 1))
            self.delta_[index] = delta
            self.weight_[index] += self.rate * np.outer(delta, self.x_[index])
        print(self.delta_)

    def classify(self, sample):
        for index in range(len(self.structure)):
            if index == 0:
                self.x_[index] = np.reshape(sample, (self.structure[index], 1))
            else:
                self.x_[index] = np.reshape(sigmoid(np.dot(self.weight_[index - 1], self.x_[index - 1])), (self.structure[index], 1))
        return self.x_[-1]


def main():
    network = Network()
    network.load_matrix().load_tag().set_structure([7])
    for i in range(5000):
        network.forward(0)
        network.backward(0)
        network.forward(1)
        network.backward(1)
        network.forward(2)
        network.backward(2)
    print(network.classify(np.array([[1, 2, 3]])))
    print(network.classify(np.array([[-1, 3, 4]])))
    print(network.classify(np.array([[2, 5, 2]])))


if __name__ == '__main__':
    main()
