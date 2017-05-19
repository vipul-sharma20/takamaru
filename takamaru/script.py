# -*- coding: utf-8 -*-

from takamaru import Reddit, Hawk


def main():
    r_instance = Reddit()
    posts_no_hot = r_instance.search()
    posts_hot = r_instance.search(hot=True)
    hawk = Hawk()

    for ph in posts_hot:
        hawk.gmail_hawk(subject="Popular Reddit Posts", body=ph)

    # for pnh in posts_no_hot:
    #    hawk.gmail_hawk(subject="Top Posts", body=pnh)


if __name__ == '__main__':
    main()
