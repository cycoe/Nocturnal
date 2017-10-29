#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from modules.Logger import Logger
from Config import Config


class Mail(object):

    mail_host = Config.confDict['host']

    sender = Config.confDict['sender']
    password = Config.confDict['emailPassword']
    receiver = Config.confDict['receiver']

    @staticmethod
    def send_mail(content):
        message = MIMEText(content, 'HTML', 'utf-8')
        message['From'] = formataddr(['cycoe', Mail.sender])
        message['To'] = formataddr(['cycoe', Mail.receiver])
        message['subject'] = 'Robbed a new speech!'

        try:
            server = smtplib.SMTP()
            server.connect(Mail.mail_host, int(Config.confDict['port']))
            server.login(Mail.sender, Mail.password)
            server.sendmail(Mail.sender, [Mail.receiver], message.as_string())
            server.quit()
            print(Logger.log('Sent a mail to your mailbox', subContent_=['mail: ' + Mail.receiver], level=Logger.warning))
        except smtplib.SMTPException:
            print(Logger.log('failed to send a mail', level=Logger.warning))