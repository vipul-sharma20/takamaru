# -*- coding: utf-8 -*-

import base64
import configparser
from functools import wraps

import praw
from twilio.rest import Client

from constants import CONFIG_FILE, SUBREDDITS, QUERIES, TABLE_ROWS, \
        TABLE_COLUMNS, EMAIL_TEMPLATE, ANCHOR_TAG
from tasks import send_email


def prepare_message(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        body = kwargs.get('body')
        subject = kwargs.get('subject')
        rows = []
        for submission in body:
            columns = []
            anchor_tag = ANCHOR_TAG.format(href=submission.shortlink,
                                           content=submission.title)
            columns.append(TABLE_COLUMNS.format(content=anchor_tag, width='80%'))
            columns.append(TABLE_COLUMNS.format(content=submission.score, width='20%'))
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
                                         limit=6)
                results.append(submissions)

        return results


class Hawk(object):

    def twilio_hawk(self):
        account = self.config['TWILIO']['ACCOUNT']
        token = self.config['TWILIO']['TOKEN']

    @prepare_message
    def gmail_hawk(self, subject, body):
        send_email.delay(subject, body)

