#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyqrcode
from PIL import Image

from .Config import Config


class Qrcode(object):

    @staticmethod
    def create_qrcode_img():
        wechat_qrcode = pyqrcode.create(Config.wechat_uri)
        alipay_qrcode = pyqrcode.create(Config.alipay_uri)
        wechat_qrcode.png(Config.file_name['wechat_qrcode_img'], scale=10)
        alipay_qrcode.png(Config.file_name['alipay_qrcode_img'], scale=10)

    @staticmethod
    def show_qrcode(img_path):
        img = Image.open(img_path)
        img.show()