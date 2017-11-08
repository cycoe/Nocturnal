#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import os
import random


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
        self.weight_remain = []
        self.x_ = []
        self.matrix_ = []
        self.tag_ = []
        self.delta_ = []
        self.rate = 0.9
        self.push = 0.7
        self.count = 0

    def load_matrix(self, matrix_=np.array([[1, 2, 3, 5, 3, 4, 3],
                                            [-1, 3, 4, 4, 2, 3, 1],
                                            [2, 5, 2, 4, 2, 4, 3]])):
        self.matrix_ = matrix_
        return self

    def load_tag(self, tag_=np.array([[1, 0],
                                      [0, 1],
                                      [1, 1]])):
        self.tag_ = tag_
        return self

    def set_structure(self, structure):
        structure.insert(0, len(self.matrix_[0]))
        structure.append(len(self.tag_[0]))
        for index in range(len(structure) - 1):
            self.weight_.append(np.random.random((structure[index + 1], structure[index])) * 2 - 1)
            self.weight_remain.append(0)
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

        return self.x_[-1]

    def backward(self, sample_index):
        for index in range(len(self.structure) - 2, -1, -1):
            output = self.x_[index + 1]
            if index == len(self.structure) - 2:
                delta = np.reshape((np.reshape(self.tag_[sample_index], (self.structure[index + 1], 1)) - output) * output * (1 - output), (self.structure[index + 1], 1))
            else:
                delta = np.reshape(output * (1 - output) * np.dot(self.weight_[index + 1].T, self.delta_[index + 1]), (self.structure[index + 1], 1))
            self.delta_[index] = delta
            self.weight_remain[index] = self.rate * (1+20000/(10000+self.count)) * np.outer(delta, self.x_[index]) + self.push * self.weight_remain[index]
            self.weight_[index] += self.weight_remain[index]
            self.count += 1

        return self

    def classify(self, sample):
        for index in range(len(self.structure)):
            if index == 0:
                self.x_[index] = np.reshape(sample, (self.structure[index], 1))
            else:
                self.x_[index] = np.reshape(sigmoid(np.dot(self.weight_[index - 1], self.x_[index - 1])), (self.structure[index], 1))

        return self.x_[-1]


def main():
    sample_matrix = []
    tag_ = []
    for tag in os.listdir('../training'):
        for sample_file in os.listdir('../training' + '/' + tag):
            sample = []
            with open('../training' + '/' + tag + '/' + sample_file) as fr:
                for char in fr.readline().strip():
                    sample.append(float(char))
            sample_matrix.append(sample)
            tag_temp = [float(i) for i in bin(ord(tag))[2:]]
            if len(tag_temp) < 7:
                tag_temp.insert(0, 0.0)
            tag_.append(tag_temp)
    network = Network()
    network.load_matrix(np.array(sample_matrix)).load_tag(np.array(tag_)).set_structure([20])

    # training
    sample_count = 4000
    cycle_count = 5000
    for i in range(cycle_count):
        shuff = list(zip(sample_matrix, tag_))
        random.shuffle(shuff)
        sample_matrix = [item[0] for item in shuff]
        tag_ = [item[1] for item in shuff]
        count = 0
        errors = 0
        for j in range(sample_count):
            output = network.forward(j)
            network.backward(j)
            output = [int(i + 0.5) for i in output]
            target = [int(i) for i in network.tag_[j]]
            for bit in range(len(output)):
                if output[bit] != target[bit]:
                    errors += 1
                    break
            count += 1

        print('(' + str(int(i/cycle_count*100)) + '%) ' + 'error rate = ' + str(errors / count))

    # recall


if __name__ == '__main__':
    main()
