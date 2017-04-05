import smtplib

scroll_template = \
    'From: {0}\n' \
    'To: {1}\n' \
    'Subject: {2}\n{3}'


def send_message(receivers, subject, msg):
    if not receivers.__iter__() or len(receivers) < 1:
        raise TypeError('receivers must be iterable with at least one e-mail address')
    msg_sender = 'weavers.pigeon@gmail.com'
    msg = scroll_template.format(msg_sender, ','.join(receivers), subject, msg)
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login(msg_sender, 'Wre8t5naWe=#')
    smtp.sendmail(msg_sender, receivers, msg)
    smtp.close()


def alert_tower(msg):
    send_message(['natanael.delatorre@jato.com'], 'Alert', msg)
