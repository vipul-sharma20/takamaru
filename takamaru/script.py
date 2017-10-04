# -*- coding: utf-8 -*-

from takamaru import Reddit, Hawk
from constants import SUBREDDITS, REDDIT_RECIPIENTS


def main():
    r_instance = Reddit()
    posts_hot = r_instance.search(hot=True)
    hawk = Hawk()

    for i, ph in enumerate(posts_hot):
        subject = "Popular Reddit Posts in /r/{sub}".format(sub=SUBREDDITS[i])
        for r in REDDIT_RECIPIENTS:
            hawk.gmail_hawk(subject=subject, source='reddit',
                            body=ph, recipients=[r])


if __name__ == '__main__':
    main()
