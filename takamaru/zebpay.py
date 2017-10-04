# -*- coding: utf-8 -*-

from takamaru import Zebpay, Hawk
from constants import BUY_THRESHOLD, SELL_THRESHOLD, ZEBPAY_RECIPIENTS, ZEBPAY_URL


def main():
    z_instance = Zebpay()
    hawk = Hawk()

    buy_price, sell_price = z_instance.get_price()
    if buy_price:
        subject = "Buy price less than {threshold}: Current: {buy_price}".format(
                                                    threshold=BUY_THRESHOLD,
                                                    buy_price=buy_price
                                                )
        body = "Buy price has dropped below the threshold value check {url}".format(
                                                    url=ZEBPAY_URL
                                                )
        for r in ZEBPAY_RECIPIENTS:
            hawk.gmail_hawk(subject=subject, source='zebpay',
                            body=body, recipients=[r])

    if sell_price:
        subject = "Sell price more than {threshold}: Current: {sell_price}".format(
                                                    threshold=SELL_THRESHOLD,
                                                    buy_price=sell_price
                                                )
        body = "Sell price has gone above the threshold value check {url}".format(
                                                    url=ZEBPAY_URL
                                                )
        for r in ZEBPAY_RECIPIENTS:
            hawk.gmail_hawk(subject=subject, source='zebpay',
                            body=body, recipients=[r])


if __name__ == '__main__':
    main()
