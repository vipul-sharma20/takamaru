# -*- coding: utf-8 -*-

import base64
import configparser
from functools import wraps
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import praw
from twilio.rest import Client

from constants import CONFIG_FILE, SUBREDDITS, QUERIES, RECEPIENTS, \
        SMTP_SERVER, SMTP_PORT, TABLE_ROWS, TABLE_COLUMNS, EMAIL_TEMPLATE


def prepare_message(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        body = kwargs.get('body')
        subject = kwargs.get('subject')
        rows = []
        for submission in body:
            columns = []
            columns.append(TABLE_COLUMNS.format(content=submission.title, width='80%'))
            columns.append(TABLE_COLUMNS.format(content=submission.shortlink, width='20%'))
            rows.append(TABLE_ROWS.format(content=''.join(columns)))
        body = EMAIL_TEMPLATE.format(rows=''.join(rows))
        return func(self, body=body, subject=subject)
    return wrapper


class Reddit(object):

    def __init__(self, *args, **kwargs):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        client_id = config['REDDIT']['CLIENT_ID']
        client_secret = config['REDDIT']['CLIENT_SECRET']
        username = config['CREDENTIALS']['USERNAME']
        password = base64.b64decode(config['CREDENTIALS']['PASSWORD'])

        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  username=username,
                                  password=password,
                                  user_agent='script by /u/{}'.format(username))

    def search(self, hot=False, time_filter='day', *args, **kwargs):
        query = lambda q: '+'.join(q)
        results = []

        if hot:
            for s in SUBREDDITS:
                submissions = self.reddit.subreddit(s).hot(limit=3)
                results.append(submissions)

        else:
            sub = self.reddit.subreddit(query(SUBREDDITS))

            for q in QUERIES:
                submissions = sub.search(query=query(q),
                                         time_filter=time_filter,
                                         limit=3)
                results.append(submissions)

        return results


class Hawk(object):

    def __init__(self, *args, **kwargs):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_FILE)

    def twilio_hawk(self):
        account = self.config['TWILIO']['ACCOUNT']
        token = self.config['TWILIO']['TOKEN']

    @prepare_message
    def gmail_hawk(self, subject, body):
        gmail_user = self.config['GMAIL']['USER']
        gmail_pwd = base64.b64decode(self.config['GMAIL']['PASSWORD']).decode('UTF-8')

        try:
            msg = MIMEMultipart()
            msg['From'] = gmail_user
            msg['To'] = ', '.join(RECEPIENTS)
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'html'))

            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()

            server.login(gmail_user, gmail_pwd)
            text = msg.as_string()
            server.sendmail(gmail_user, RECEPIENTS, text)
            server.quit()

        except smtplib.SMTPException:
            print("failed to send e-mail")

