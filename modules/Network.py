import numpy as np

# from modules.Node import Node


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
        self.x_ = []
        self.matrix_ = []
        self.tag_ = []
        self.delta_ = []
        self.output = None
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
        self.x_ = [0 for i in range(len(self.weight_) + 1)]
        self.delta_ = [0 for i in range(len(self.weight_))]
        return self

    def forward(self, sample_index):
        for index in range(len(self.weight_) + 1):
            if index == 0:
                self.x_[index] = self.matrix_[sample_index]
            else:
                self.x_[index] = sigmoid(np.dot(self.weight_[index - 1], self.x_[index - 1]))
        # print(self.x_)
        # print(self.weight_)
        return self

    def backward(self, sample_index):
        for index in range(len(self.weight_) - 1, -1, -1):
            output = self.x_[index + 1]
            if index == len(self.weight_) - 1:
                delta = (self.tag_[sample_index] - output) * output * (1 - output)
            else:
                delta = output * (1 - output) * np.dot(self.weight_[index + 1], self.delta_[index + 1])
            self.delta_[index] = delta
            self.weight_[index] += self.rate * np.outer(delta, self.x_[index])
        print(self.delta_)


def main():
    network = Network()
    network.load_matrix().load_tag().set_structure([2]).forward(0).backward(0)


if __name__ == '__main__':
    main()
