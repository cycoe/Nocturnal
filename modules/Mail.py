#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


class Mail(object):

    mail_host = 'smtp.163.com'

    sender = 'a871873687@163.com'
    password = 'zhiwen.COM'
    receiver = '871873687@qq.com'

    @staticmethod
    def send_mail(content):
        message = MIMEText(content, 'HTML', 'utf-8')
        message['From'] = formataddr(['cycoe', Mail.sender])
        message['To'] = formataddr(['cycoe', Mail.receiver])
        message['subject'] = 'Robbed a new speech!'

        try:
            server = smtplib.SMTP()
            server.connect(Mail.mail_host, 25)
            server.login(Mail.sender, Mail.password)
            server.sendmail(Mail.sender, [Mail.receiver], message.as_string())
            server.quit()
            print("Done")
        except smtplib.SMTPException:
            print("failed")