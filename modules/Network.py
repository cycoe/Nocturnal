#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import os
from .img2Vector import img2Vector


def ReLU(sigma):
    for index in range(len(sigma)):
        for bit in range(len(sigma[0])):
            if sigma[index][bit] < 0:
                sigma[index][bit] = 0
    return sigma


def ReLU_diff(sigma):
    for index in range(len(sigma)):
        for bit in range(len(sigma[0])):
            if sigma[index][bit] > 0:
                sigma[index][bit] = 1
            else:
                sigma[index][bit] = 0
    return sigma


def ELU(sigma, alpha):
    for index in range(len(sigma)):
        for bit in range(len(sigma[0])):
            if sigma[index][bit] < 0:
                alpha * (np.exp(sigma[index][bit]) - 1)
    return sigma


def ELU_diff(sigma, alpha):
    for index in range(len(sigma)):
        for bit in range(len(sigma[0])):
            if sigma[index][bit] >= 0:
                sigma[index][bit] = 1
            else:
                sigma[index][bit] += alpha
    return sigma


def tanh(sigma):
    return np.tanh(sigma)


def tanh_diff(sigma):
    return 1 - sigma * sigma


def norm2(point):
    """
    欧几里得范数

    :param point: 输出向量
    :return: 范数值
    """
    return np.vdot(point, point)


def get_distance(point1, point2):
    distance = 0
    for index in range(len(point1)):
        distance += (point1[index] - point2[index]) ** 2
    return distance


def classify(output, tag_set):
    """
    分类函数
    :param output: 输出向量
    :param tag_set: 类别向量的集合
    :return: 类别
    """
    min_index = 0
    for index in range(len(tag_set)):
        if get_distance(output, tag_set[index]) < get_distance(output, tag_set[min_index]):
            min_index = index
    return tag_set[min_index]


class Network(object):

    def __init__(self):
        self.structure = []
        self.weight_ = []
        self.delta_weight = []
        self.x_ = []
        self.matrix_ = []
        self.tag_ = []
        self.tag_set = []
        self.delta_ = []
        self.rate = 0.01
        self.push = 0.007
        self.count = 0
        self.error = 0
        self.active = tanh
        self.active_diff = tanh_diff

    def load_matrix(self, matrix_):
        self.matrix_ = np.array(matrix_)
        return self

    def load_tag(self, tag_):
        tag_set = []
        for tag in tag_:
            if tag not in tag_set:
                tag_set.append(tag)
        self.tag_set = np.array(tag_set)
        self.tag_ = np.array(tag_)
        return self

    def set_structure(self, structure):
        """
        initiate the structure, weight matrix and delta weight matrix of NN
        :param structure: <list[int]>
        :return: self
        """
        self.structure = structure
        for index in range(len(structure) - 1):
            self.weight_.append(np.random.random((structure[index + 1], structure[index] + 1)) * 0.2 - 0.1)
            self.delta_weight.append(0)
        self.x_ = [0 for i in range(len(structure))]
        self.delta_ = [0 for i in range(len(structure) - 1)]

        return self

    def forward(self, sample_index):
        """
        forward propagation of outputs
        :param sample_index: <int> index of sample
        :return: the distance between output and tag
        """
        for index in range(len(self.structure)):
            if index == 0:
                self.x_[index] = np.reshape(self.matrix_[sample_index], (self.structure[index], 1))
            else:
                self.x_[index] = self.active(np.reshape(np.dot(self.weight_[index - 1], np.insert(self.x_[index - 1], -1, 1)), (self.structure[index], 1)))
        self.error = norm2(self.x_[-1] - self.tag_[sample_index])

        return classify(self.x_[-1], self.tag_set)

    def backward(self, sample_index):
        """
        backward propagation of errors
        :param sample_index: <int> index of sample
        :return: self
        """
        for index in range(len(self.structure) - 2, -1, -1):
            output = self.x_[index + 1]
            if index == len(self.structure) - 2:
                delta = np.reshape((np.reshape(self.tag_[sample_index], (self.structure[index + 1], 1)) - output) * self.active_diff(output), (self.structure[index + 1], 1))
            else:
                delta = np.reshape(self.active_diff(output) * np.dot(np.delete(self.weight_[index + 1], -1, 1).T, self.delta_[index + 1]), (self.structure[index + 1], 1))
            self.delta_weight[index] = self.rate * np.outer(delta, np.insert(self.x_[index], -1, 1)) + self.push * self.delta_weight[index]
            self.delta_[index] = delta
            self.weight_[index] += self.delta_weight[index]
            self.count += 1

        return self

    def classify(self, sample):
        """
        find the nearest tag of output
        :param sample: <array[float]> sample to classify
        :return: <array[float]> the predicted tag of the sample
        """
        for index in range(len(self.structure)):
            if index == 0:
                self.x_[index] = np.reshape(sample, (self.structure[index], 1))
            else:
                self.x_[index] = self.active(np.reshape(np.dot(self.weight_[index - 1], np.insert(self.x_[index - 1], -1, 1)), (self.structure[index], 1)))

        return classify(self.x_[-1], self.tag_set)

    def dump_weight(self):
        """
        dump weight matrix to file
        :return: self
        """
        if not os.path.exists('weight'):
            os.mkdir('weight')
        for index in range(len(self.weight_)):
            np.save('weight' + os.path.sep + str(index), self.weight_[index])

        return self

    def load_weight(self):
        """
        load weight matrix from file
        :return: self
        """
        if not os.path.exists('weight'):
            return False
        for index in range(len(self.weight_)):
            weight = np.load('weight' + os.path.sep + str(index) + '.npy')
            if np.shape(self.weight_[index]) == np.shape(weight):
                self.weight_[index] = weight


# def main():
#     full_matrix = []
#     full_tag_ = []
#     for image_file in os.listdir('../sample'):
#         vectors_ = img2Vector('../sample/' + image_file, image_file[:4])
#         if vectors_:
#             for index in range(4):
#                 full_matrix.append(vectors_[index])
#                 tag = [int(item) for item in str(bin(ord(image_file[index])))[2:]]
#                 if len(tag) < 7:
#                     tag.insert(0, 0)
#                 full_tag_.append(tag)
#     training_ratio = int(len(full_matrix) * 0.7)
#     fitting_ratio = len(full_matrix) - training_ratio
#     training_matrix = [full_matrix[index] for index in range(training_ratio)]
#     training_tag_ = [full_tag_[index] for index in range(training_ratio)]
#     fitting_matrix = [full_matrix[index] for index in range(training_ratio, len(full_matrix))]
#     fitting_tag_ = [full_tag_[index] for index in range(training_ratio, len(full_tag_))]
#
#     network = Network()
#     network.load_matrix(training_matrix).load_tag(training_tag_).set_structure([300, 200, 100, 7]).load_weight()
#
#     cycle_count = 5000
#     for i in range(cycle_count):
#         training_errors = 0
#         fitting_errors = 0
#         for j in range(training_ratio):
#             output = network.forward(j)
#             network.backward(j)
#             for index in range(len(output)):
#                 if output[index] != training_tag_[j][index]:
#                     training_errors += 1
#                     break
#
#         for j in range(fitting_ratio):
#             output = network.classify(fitting_matrix[j])
#             for index in range(len(output)):
#                 if output[index] != fitting_tag_[j][index]:
#                     fitting_errors += 1
#                     break
#
#         training_error = str(training_errors / training_ratio)
#         fitting_error = str(fitting_errors / fitting_ratio)
#         print('(' + str(int(i/cycle_count*100)) + '%) ' + 'training error ratio = ' + training_error, end='')
#         print('\t fitting error ratio = ' + fitting_error)
#         network.dump_weight()

    #     with open('plot', 'a') as fr:
    #         fr.write(training_error)
    #         fr.write(',')
    #         fr.write(fitting_error)
    #         fr.write('\n')
    #     # print(network.delta_)


if __name__ == '__main__':
    main()
