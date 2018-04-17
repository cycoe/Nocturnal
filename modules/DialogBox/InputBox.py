#!/usr/bin/python
# -*- coding: utf-8 -*-

from .BaseBox import BaseBox


class InputBox(BaseBox):

    def __init__(self, title=None):
        super(InputBox, self).__init__(title)
