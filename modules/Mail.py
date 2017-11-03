#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from modules.Logger import Logger
from Config import Config


class Mail(object):

    connectedToMail = True

    @staticmethod
    def send_mail(subject, content):
        mail_host = Config.host
        sender = Config.sender
        password = Config.emailPassword
        receiver = Config.confDict['receiver']

        message = MIMEText(content, 'html', 'utf-8')
        message['From'] = formataddr(['class_robber', sender])
        message['To'] = formataddr(['class_robber', receiver])
        message['subject'] = subject

        try:
            server = smtplib.SMTP()
            server.connect(mail_host, 25)
            server.login(sender, password)
            server.sendmail(sender, [receiver], message.as_string())
            server.quit()
            print(Logger.log('Have Send a mail to your mailbox', subContent_=['To mail: ' + receiver], level=Logger.error))
            Mail.connectedToMail = True
        except smtplib.SMTPException:
            print(Logger.log('Failed to send a mail', subContent_=['Check your receive email address'], level=Logger.error))
            Mail.connectedToMail = False
        except UnicodeDecodeError:
            print(Logger.log('Cannot handle the decode', subContent_=['Please check your computer name whether English'], level=Logger.warning))
            Mail.connectedToMail = False