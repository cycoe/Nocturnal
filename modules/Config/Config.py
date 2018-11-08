#!/usr/bin/python
# -*- coding: utf-8 -*-

import platform
import os

from modules.FileUtils import check_file_exists, load_dict, dump_dict


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
        'user_config': 'robber.conf',                # file path of user config
        'report_blacklist': 'blacklist.cache',       # file path of report blacklist
        'grade_cache': 'grade.cache',                # cache file of fetched grade
        'class_key_cache': 'class.cache',            # file to store keywords of selecting class
        'encrypt_key_path': 'encrypt.key',           # store the key to decrypt
        'wechat_qrcode_img': 'wechat.png',           # image file to show wechat pay qrcode
        'alipay_qrcode_img': 'alipay.png',           # image file to show alipay qrcode
        'wechat_mine_qrcode_img': 'wechat_mine.png', # image file to show qrcode of mine
        'log': 'Nocturnal.log',                      # log file of Nocturnal
    }

    # software running parameters
    report_refresh_relay = 10  # relay between report request
    class_refresh_relay = 1  # relay between rob class request
    grade_refresh_relay = 300  # relay between fetch grade request
    wechat_push_relay = 1  # relay between wechat notification
    animation_relay = 0.5  # relay between wait animation frame
    machine_relay = 0.1  # relay between frames of status machine
    connect_timeout = 300  # timeout of request connection
    max_attempt = 100  # max request times before give up

    # uri of donate qrcode
    wechat_uri = 'wxp://f2f0PYx27X0CWU1yiBhSKeHHgYzfA27iOicM'
    alipay_uri = 'HTTPS://QR.ALIPAY.COM/FKX01669SBV7NA4ALTVPE8'
    wechat_mine_uri = 'https://u.wechat.com/EIA-YeYzBhVKqbbEGfcaR_8'

    # logging format pattern
    log_format = '%(asctime)s %(levelname)s %(funcName)s No.%(lineno)d | %(threadName)s | %(message)s'

    # encrypt key
    encrypt_key = '123456'

    # user parameters
    user = {
        'userName': '',
        'password': '',
        'receiver': '',
        'sender': 'class_robber@cycoe.cc',
        'sender_password': 'class_robber',
        'sender_host': 'smtp.ym.163.com',
        'sender_port': '25',
    }

    # patterns to check users' parameters input is legal or not
    pattern = {
        'receiver': '.+@.+(\..+)+',
        'sender': '.+@.+(\..+)+',
        'sender_password': '.*',
        'sender_host': 'smtp(\..+)+',
        'sender_port': '\d{1, 5}',
    }

    # @staticmethod
    # def init_cache_directory():
    #     """
    #     create cache directory if it is not exist
    #     and add a directory prefix before file name
    #     must be executed after imported
    #     :return: None
    #     """
    #     if not os.path.exists(Config.cache_directory):
    #         os.mkdir(Config.cache_directory)
    #     for key in Config.file_name.keys():
    #         Config.file_name[key] += Config.cache_directory

    @staticmethod
    def check_config_file():
        return check_file_exists(Config.file_name['user_config'])

    @staticmethod
    def load_user_config():
        config = load_dict(Config.file_name['user_config'])
        if config:
            Config.user = config
            return True
        else:
            return False

    @staticmethod
    def dump_user_config():
        dump_dict(Config.user, Config.file_name['user_config'])
