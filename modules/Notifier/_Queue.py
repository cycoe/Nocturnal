#!/usr/bin/python
# -*- coding: utf-8 -*-


class Queue(object):

    def __init__(self):
        self.queue = []

    def get_length(self):
        """
        获得队列的长度
        :return: <int> 返回队列的长度
        """
        return len(self.queue)

    def push(self, content):
        """
        将元素压入队列的开头
        :param content: 需要压入队列的元素
        :return:
        """
        self.queue.insert(0, content)

    def insert(self, index, content):
        """
        向队列的任意位置插入元素
        :param index: 插入的索引
        :param content: 插入的内容
        :return: 是否插入成功，若索引超出范围则返回 False
        """
        if index in range(self.get_length()+1):
            self.queue.insert(index, content)
            return True
        return False

    def pop(self, num=1):
        """
        弹出队尾的若干个元素
        :param num: 弹出的元素个数
        :return: <List> 弹出的元素列表
        """
        if num in range(1, self.get_length()+1):
            content = self.queue[-num:]
            del(self.queue[-num:])
        else: content = None
        return content

    def pop_all(self):
        """
        弹出队列中所有的元素
        :return: <List> 弹出的元素列表
        """
        return self.pop(self.get_length())

    def append(self, content):
        """
        在队列尾插入元素
        :param content: 需要插入的内容
        :return:
        """
        self.queue.append(content)

    def delete(self, index):
        """
        删除任意位置的元素
        :param index:
        :return:
        """
        if index in range(self.get_length()):
            del(self.queue[index])
            return True
        return False

    def print(self):
        print(self.queue)
