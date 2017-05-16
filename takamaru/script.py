# -*- coding: utf-8 -*-

from takamaru import Reddit


def main():
    r_instance = Reddit()
    posts_no_hot = r_instance.search()
    posts_hot = r_instance.search(hot=True)

    for pnh in posts_no_hot:
        for p in pnh:
            print(p.title)

    for ph in posts_hot:
        for p in ph:
            print(p.title)


if __name__ == '__main__':
    main()
