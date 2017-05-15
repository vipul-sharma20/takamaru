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
                                  password=password,
                                  user_agent='script by /u/{}'.format(username))

    def search(self, hot=False, *args, **kwargs):
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
                                         time_filter='day',
                                         limit=3)
                results.append(submissions)

        return results


if __name__ == '__main__':
    r_instance = Reddit()
    posts_no_hot = r_instance.search()
    posts_hot = r_instance.search(hot=True)
    for pnh in posts_no_hot:
        for p in pnh:
            print(p.title)
    for ph in posts_hot:
        for p in ph:
            print(p.title)
