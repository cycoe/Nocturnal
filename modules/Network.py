#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import os
from img2Vector import img2Vector


def sigmoid(sigma):
    """
    sigmoid 激活函数

    :param sigma: 求和值
    :return: 激活值
    """
    return 1.0 / (1 + np.exp(- sigma))


def ReLu(sigma):
    for index in range(len(sigma)):
        if sigma[index][0] < 0:
            sigma[index][0] = 0
    return sigma


def sgn(sigma):
    for index in range(len(sigma)):
        if sigma[index][0] > 0:
            sigma[index][0] = 1
        else:
            sigma[index][0] = 0
    return sigma


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
        self.delta_weight = []
        self.x_ = []
        self.matrix_ = []
        self.tag_ = []
        self.delta_ = []
        self.rate = 0.01
        self.push = 0.007
        self.count = 0

    def load_matrix(self, matrix_=np.array([[0, 0],
                                            [1, 0],
                                            [0, 1],
                                            [1, 1]])):
        self.matrix_ = matrix_
        return self

    def load_tag(self, tag_=np.array([[0],
                                      [0],
                                      [0],
                                      [1]])):
        self.tag_ = tag_
        return self

    def set_structure(self, structure):
        structure.insert(0, len(self.matrix_[0]))
        structure.append(len(self.tag_[0]))
        for index in range(len(structure) - 1):
            self.weight_.append(np.random.random((structure[index + 1], structure[index] + 1)) * 0.2 - 0.1)
            self.delta_weight.append(0)
        self.structure = structure
        self.x_ = [0 for i in range(len(self.structure))]
        self.delta_ = [0 for i in range(len(self.structure) - 1)]

        return self

    def forward(self, sample_index):
        for index in range(len(self.structure)):
            if index == 0:
                self.x_[index] = np.reshape(self.matrix_[sample_index], (self.structure[index], 1))
            else:
                self.x_[index] = np.tanh(np.reshape(np.dot(self.weight_[index - 1], np.insert(self.x_[index - 1], -1, 1)), (self.structure[index], 1)))

        return self.x_[-1]

    def backward(self, sample_index):
        for index in range(len(self.structure) - 2, -1, -1):
            output = self.x_[index + 1]
            if index == len(self.structure) - 2:
                delta = np.reshape((np.reshape(self.tag_[sample_index], (self.structure[index + 1], 1)) - output) * (1 - output * output), (self.structure[index + 1], 1))
            else:
                delta = np.reshape((1 - output * output) * np.dot(np.delete(self.weight_[index + 1], -1, 1).T, self.delta_[index + 1]), (self.structure[index + 1], 1))
            self.delta_weight[index] = self.rate * np.outer(delta, np.insert(self.x_[index], -1, 1)) + self.push * self.delta_weight[index]
            self.delta_[index] = delta
            self.weight_[index] += self.delta_weight[index]
            self.count += 1

        return self

    def classify(self, sample):
        for index in range(len(self.structure)):
            if index == 0:
                self.x_[index] = np.reshape(sample, (self.structure[index], 1))
            else:
                self.x_[index] = np.tanh(np.reshape(np.dot(self.weight_[index - 1], np.insert(self.x_[index - 1], -1, 1)), (self.structure[index], 1)))

        return self.x_[-1]

    def dump_weight(self):
        if not os.path.exists('weight'):
            os.mkdir('weight')
        for index in range(len(self.weight_)):
            np.save('weight/' + str(index), self.weight_[index])

        return self

    def load_weight(self):
        if not os.path.exists('weight'):
            return False
        for index in range(len(self.weight_)):
            weight = np.load('weight/' + str(index) + '.npy')
            if np.shape(self.weight_[index]) == np.shape(weight):
                self.weight_[index] = weight


def main():
    training_matrix = []
    fitting_matrix = []
    training_tag_ = []
    fitting_tag_ = []
    for tag in os.listdir('../training'):
        files_ = os.listdir('../training' + '/' + tag)
        tag_temp = [float(i) for i in bin(ord(tag))[2:]]
        if len(tag_temp) < 7:
            tag_temp.insert(0, 0.0)
        for sample_file in range(len(files_)):
            sample = []
            with open('../training' + '/' + tag + '/' + files_[sample_file]) as fr:
                for char in fr.readline().strip():
                    sample.append(float(char))
            if sample_file < 0.7 * len(files_):
                training_matrix.append(sample)
                training_tag_.append(tag_temp)
            else:
                fitting_matrix.append(sample)
                fitting_tag_.append(tag_temp)
    # training_matrix = np.array([[0, 0],
    #                             [0, 1],
    #                             [1, 0],
    #                             [1, 1]])
    # training_tag_ = np.array([[0],
    #                           [0],
    #                           [0],
    #                           [1]])
    # fitting_matrix = np.array([[0, 0],
    #                             [0, 1],
    #                             [1, 0],
    #                             [1, 1]])
    # fitting_tag_ = np.array([[0],
    #                           [0],
    #                           [0],
    #                           [1]])

    network = Network()
    network.load_matrix(np.array(training_matrix)).load_tag(np.array(training_tag_)).set_structure([40, 20]).load_weight()
    # network.load_matrix().load_tag().set_structure([3])

    # training
    sample_count = len(training_tag_)
    cycle_count = 50000
    for i in range(cycle_count):
        # shuff = list(zip(training_matrix, training_tag_))
        # random.shuffle(shuff)
        # training_matrix = [item[0] for item in shuff]
        # training_tag_ = [item[1] for item in shuff]
        training_count = 0
        training_errors = 0
        fitting_count = 0
        fitting_errors = 0
        for j in range(sample_count):
            output = network.forward(j)
            network.backward(j)
            output = [int(i + 0.5) for i in output]
            target = [int(i) for i in training_tag_[j]]
            for bit in range(len(output)):
                if output[bit] != target[bit]:
                    training_errors += 1
                    break
            # training_errors += norm2(np.array(output) - np.array(training_tag_[j]))
            training_count += 1
            # print(output)
            # print(training_tag_[j])

        for j in range(len(fitting_tag_)):
            output = network.classify(fitting_matrix[j])
            output = [int(i + 0.5) for i in output]
            target = [int(i) for i in fitting_tag_[j]]
            for bit in range(len(output)):
                if output[bit] != target[bit]:
                    fitting_errors += 1
                    break
            # fitting_errors += norm2(np.array(output) - np.array(fitting_tag_[j]))
            fitting_count += 1
        training_error = str(training_errors / training_count)
        fitting_error = str(fitting_errors / fitting_count)
        print('(' + str(int(i/cycle_count*100)) + '%) ' + 'training error ratio = ' + training_error, end='')
        print('\t fitting error ratio = ' + fitting_error)
        network.dump_weight()
        with open('plot', 'a') as fr:
            fr.write(training_error)
            fr.write(',')
            fr.write(fitting_error)
            fr.write('\n')
        # print(network.delta_)


if __name__ == '__main__':
    # main()
    # training_matrix = np.array([[0, 0],
    #                             [0, 1],
    #                             [1, 0],
    #                             [1, 1]])
    # training_tag_ = np.array([[0],
    #                             [1],
    #                             [1],
    #                             [0]])
    # fitting_matrix = np.array([[0, 0],
    #                             [0, 1],
    #                             [1, 0],
    #                             [1, 1]])
    # fitting_tag_ = np.array([[0],
    #                           [0],
    #                           [0],
    #                           [1]])
    #
    # network = Network()
    # network.load_matrix(np.array(training_matrix)).load_tag(np.array(training_tag_)).set_structure([3])
    # for j in range(10000):
    #     for i in range(len(training_matrix)):
    #         print(network.forward(i))
    #         network.backward(i)
    # # print(network.x_)
    #         # print(network.delta_)
    training_matrix = []
    fitting_matrix = []
    training_tag_ = []
    fitting_tag_ = []
    for tag in os.listdir('../training'):
        files_ = os.listdir('../training' + '/' + tag)
        tag_temp = [float(i) for i in bin(ord(tag))[2:]]
        if len(tag_temp) < 7:
            tag_temp.insert(0, 0.0)
        for sample_file in range(len(files_)):
            sample = []
            with open('../training' + '/' + tag + '/' + files_[sample_file]) as fr:
                for char in fr.readline().strip():
                    sample.append(float(char))
            if sample_file < 0.7 * len(files_):
                training_matrix.append(sample)
                training_tag_.append(tag_temp)
            else:
                fitting_matrix.append(sample)
                fitting_tag_.append(tag_temp)
    network = Network()
    network.load_matrix(np.array(training_matrix)).load_tag(np.array(training_tag_)).set_structure([40, 20]).load_weight()
    for file in os.listdir('../training_ori'):
        sample_ = img2Vector('../training_ori/' + file)
        name = ''
        for sample in sample_:
            output = network.classify(np.reshape(np.array(sample), (network.structure[0], 1)))
            output = [int(item + 0.5) for item in output]
            count = 0
            for index in range(len(output)):
                count += 2**(6-index) * output[index]
            output = chr(count)
            name += output
        print(name)
        os.rename('../training_ori/' + file, '../training_ori/' + name + '.gif')
