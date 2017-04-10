#!/usr/bin/env python

import smtplib
import credentials

scroll_template = \
    'From: {0}\n' \
    'To: {1}\n' \
    'Subject: {2}\n{3}'


def send_message(receivers, subject, msg):
    if not receivers.__iter__() or len(receivers) < 1:
        raise TypeError('receivers must be iterable with at least one e-mail address')
    credential = credentials.credentials_dict['gmail']
    msg_sender = credential.username
    msg = scroll_template.format(msg_sender, ','.join(receivers), subject, msg)
    smtp = smtplib.SMTP_SSL(credential.ipAddress, credential.port)
    smtp.login(msg_sender, credential.pwd)
    smtp.sendmail(msg_sender, receivers, msg)
    smtp.close()


def alert_tower(msg):
    send_message(['natanael.delatorre@jato.com'], 'Alert', msg)
