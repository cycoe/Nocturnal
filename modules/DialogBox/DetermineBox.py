#!/usr/bin/python
# -*- coding: utf-8 -*-

from .BaseBox import BaseBox


class DetermineBox(BaseBox):

    def __init__(self, title):
        super(DetermineBox, self).__init__(title)
        self.pattern = 'yes|no'
