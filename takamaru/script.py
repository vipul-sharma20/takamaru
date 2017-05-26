# -*- coding: utf-8 -*-

from takamaru import Reddit, Hawk


def main():
    r_instance = Reddit()
    posts_hot = r_instance.search(hot=True)
    hawk = Hawk()

    for ph in posts_hot:
        hawk.gmail_hawk(subject="Popular Reddit Posts", body=ph)


if __name__ == '__main__':
    main()
