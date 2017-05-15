import configparser

import praw

from constants import CONFIG_FILE, SUBREDDITS, QUERIES


class Reddit(object):

    def __init__(self, *args, **kwargs):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        client_id = config['KEYS']['CLIENT_ID']
        client_secret = config['KEYS']['CLIENT_SECRET']
        username = config['CREDENTIALS']['USERNAME']
        password = config['CREDENTIALS']['PASSWORD']

        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  username=username,
                                  password=password)

    def search(self, hot=False, *args, **kwargs):
        query = lambda q: '+'.join(q)
        results = []

        if hot:
            for s in SUBREDDITS:
                submissions = self.reddit.subreddit(s).hot(limit=3)
                results.append(submissions)

        else:
            sub = self.reddit.subreddits(query(SUBREDDITS))

            for q in QUERIES:
                submissions = sub.search(query=query(q),
                                         time_filter='day',
                                         limit=3)
                results.append(submissions)

        return results


if __name__ == '__name__':
    pass
