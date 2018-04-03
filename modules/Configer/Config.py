#!/usr/bin/python
# -*- coding: utf-8 -*-

import platform
import os


class Config(object):
    """管理配置的类"""

    # software information
    version = 'V 4.0'  # 版本号
    author = 'Cycoe'  # 作者
    platform = platform.system()  # runtime platform, windows or linux

    # cache directory of all cache files
    cache_directory = 'cache'
    # cache and other files' name
    file_name = {
        'config_file': 'robber.conf',  # file path of config file
        'report_blacklist': 'blacklist.cache',  # file path of report blacklist
        'grade_cache': 'grade.cache',  # cache file of fetched grade
        'class_key_cache': 'class.cache',  # file to store keywords of selecting class
        'wechat_qrcode_img': 'wechat.png',
        'alipay_qrcode_img': 'alipay.png',
    }

    # software running parameters
    report_refresh_relay = 10  # relay between report request
    wechat_push_relay = 1  # relay between wechat notification
    animation_relay = 0.5  # relay between wait animation frame
    connect_timeout = 300  # timeout of request connection
    max_attempt = 100  # max request times before give up

    # uri of donate qrcode
    wechat_uri = 'wxp://f2f0PYx27X0CWU1yiBhSKeHHgYzfA27iOicM'
    alipay_uri = 'HTTPS://QR.ALIPAY.COM/FKX01669SBV7NA4ALTVPE8'


    @staticmethod
    def init_cache_directory():
        """
        create cache directory if it is not exist
        and add a directory prefix before file name
        :return: None
        """
        if not os.path.exists(Config.cache_directory):
            os.mkdir(Config.cache_directory)
        for key in Config.file_name.keys():
            Config.file_name[key] += Config.cache_directory