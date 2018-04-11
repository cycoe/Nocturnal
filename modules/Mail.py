#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
import re

from email.mime.text import MIMEText
from email.utils import formataddr
from modules.Logger import Logger
from modules.Config import Config
from modules.String import String


class Mail(object):

    CONNECTED_TO_MAIL = True
    HAVE_SEND_A_MAIL = 1
    FAILED_SEND_EMAIL = 2
    CANNOT_HANDLE_DECODE = 3
    HOST_ERROR = 4
    ADDRESS_DOESNT_EXIST = 5

    @staticmethod
    def send_mail(subject, content):
        receiver = Config.user['receiver']
        sender = Config.user['sender']
        sender_password = Config.user['sender_password']
        sender_host = Config.user['sender_host']
        sender_port = Config.user['sender_port']

        message = MIMEText(content, 'html', 'utf-8')
        message['From'] = formataddr(['class_robber', sender])
        message['To'] = formataddr(['class_robber', receiver])
        message['subject'] = subject

        try:
            server = smtplib.SMTP()
            server.connect(sender_host, int(sender_port))
            server.login(sender, sender_password)
            server.sendmail(sender, [receiver], message.as_string())
            server.quit()
            print(Logger.log(String['have_send_a_mail'], [String['to_mail'] + receiver], Logger.error))
            Mail.CONNECTED_TO_MAIL = True
            return Mail.HAVE_SEND_A_MAIL
        except smtplib.SMTPException:
            print(Logger.log(String['failed_send_email'], [String['check_your_email_address']], Logger.error))
            Mail.CONNECTED_TO_MAIL = False
            return Mail.FAILED_SEND_EMAIL
        except UnicodeDecodeError:
            print(Logger.log(String['cannot_handle_decode'], [String['check_your_computer_name']], Logger.error))
            Mail.CONNECTED_TO_MAIL = False
            return Mail.CANNOT_HANDLE_DECODE
        except ConnectionRefusedError:
            print(Logger.log(String['host_error'], [String['check_your_host']], Logger.error))
            Mail.CONNECTED_TO_MAIL = False
            return Mail.HOST_ERROR
        except OSError:
            print(Logger.log(String['address_doesnt_exist'], Logger.error))
            Mail.CONNECTED_TO_MAIL = False
            return Mail.ADDRESS_DOESNT_EXIST

    @staticmethod
    def setEmailInfo(input_method, output_method):
        if Config.check_config_file():
            Config.load_user_config()

        for item in list(Config.user.keys())[2:]:
            current = Config.user[item]
            while True:
                buffer = input_method(item, current)
                if not buffer and current:
                    break
                elif re.search(Config.pattern[item], buffer):
                    Config.user[item] = buffer
                    break
                else:
                    output_method(String['check_spell'])

        # for item in list(MisUtils.confDict.keys())[2:]:
        #     current = MisUtils.confDict[item]
        #     while True:
        #         buffer = input('> ' + String[item] + '(' + String['current'] + ': ' + current + '): ')
        #         if not buffer and current:
        #             break
        #         elif re.search(MisUtils.pattern[item], buffer):
        #             MisUtils.confDict[item] = buffer
        #             break
        #         else:
        #             print(Logger.log(String['check_spell'], level=Logger.warning))