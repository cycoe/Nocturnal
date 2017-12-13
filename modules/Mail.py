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
        mail_host = MisUtils.host
        sender = MisUtils.sender
        password = MisUtils.emailPassword
        receiver = MisUtils.confDict['receiver']

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
            print(Logger.log(String['have_send_a_mail'], subContent_=[String['to_mail'] + receiver], level=Logger.error))
            Mail.connectedToMail = True
        except smtplib.SMTPException:
            print(Logger.log(String['failed_send_email'], subContent_=[String['check_your_email_address'] + MisUtils.confDict['receiver']], level=Logger.error))
            Mail.connectedToMail = False
        except UnicodeDecodeError:
            print(Logger.log(String['cannot_handle_decode'], subContent_=[String['check_your_computer_name']], level=Logger.warning))
            Mail.connectedToMail = False
