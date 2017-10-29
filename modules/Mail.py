#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from modules.Logger import Logger
from Config import Config


class Mail(object):

    @staticmethod
    def send_mail(content):
        mail_host = Config.confDict['host']
        sender = Config.confDict['sender']
        password = Config.confDict['emailPassword']
        receiver = Config.confDict['receiver']

        message = MIMEText(content, 'html', 'utf-8')
        message['From'] = formataddr(['cycoe', sender])
        message['To'] = formataddr(['cycoe', receiver])
        message['subject'] = 'Robbed a new speech!'

        try:
            server = smtplib.SMTP()
            server.connect(mail_host, 25)
            server.login(sender, password)
            server.sendmail(sender, [receiver], message.as_string())
            server.quit()
            print(Logger.log('Sent a mail to your mailbox', subContent_=['mail: ' + receiver], level=Logger.warning))
        except smtplib.SMTPException:
            print(Logger.log('failed to send a mail', level=Logger.warning))