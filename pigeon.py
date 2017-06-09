#!/usr/bin/env python

import smtplib
import credential

scroll_template = \
    'From: {0}\n' \
    'To: {1}\n' \
    'Subject: {2}\n.\n{3}'


def send_message(receivers, subject, msg):
    if not receivers.__iter__() or len(receivers) < 1:
        raise TypeError('receivers must be iterable with at least one e-mail address')
    cred = credential.get_credential(owner='weaver', subject='gmail')
    msg_sender = cred['username']
    msg = scroll_template.format(msg_sender, ','.join(receivers), subject, msg)
    smtp = smtplib.SMTP_SSL(cred['address'], cred['port'])
    smtp.login(msg_sender, cred['password'])
    smtp.sendmail(msg_sender, receivers, msg)
    smtp.close()


def alert_tower(msg):
    send_message(['natanael.delatorre@jato.com'], 'Alert', msg)
