#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from modules.Logger import Logger
from modules.MisUtils import MisUtils
from modules.String import String


class Mail(object):

    connectedToMail = True

    @staticmethod
    def send_mail(subject, content):
        receiver = MisUtils.confDict['receiver']
        sender = MisUtils.confDict['sender']
        sender_password = MisUtils.confDict['sender_password']
        sender_host = MisUtils.confDict['sender_host']
        sender_port = MisUtils.confDict['sender_port']

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
            Mail.connectedToMail = True
        except smtplib.SMTPException:
            print(Logger.log(String['failed_send_email'], [String['check_your_email_address']], Logger.error))
            Mail.connectedToMail = False
        except UnicodeDecodeError:
            print(Logger.log(String['cannot_handle_decode'], [String['check_your_computer_name']], Logger.error))
            Mail.connectedToMail = False
        except ConnectionRefusedError:
            print(Logger.log(String['host_error'], [String['check_your_host']], Logger.error))
            Mail.connectedToMail = False
        except OSError:
            print(Logger.log(String['address_doesnt_exist'], Logger.error))
            Mail.connectedToMail = False
