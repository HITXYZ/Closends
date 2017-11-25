"""
@author: Jiale Xu
@date: 2017/11/25
@desc: Test weibo spider.
"""
from weibo.spider import WeiboSpider


spider = WeiboSpider()


def scrape_user_info_test(id):
    info = spider.scrape_user_info(id)
    print(info)


def scrape_user_follows_test(id, number):
    follows = spider.scrape_user_follows(id, number)
    for follow in follows:
        print(follow)


def scrape_user_fans_test(id, number):
    fans = spider.scrape_user_fans(id, number)
    for fan in fans:
        print(fan)


def scrape_user_weibo_test(id, number):
    weibos = spider.scrape_user_weibo(id, number)
    for weibo in weibos:
        print(weibo)


scrape_user_info_test(5648343109)
scrape_user_follows_test(5648343109, 10)
scrape_user_fans_test(5648343109, 10)
scrape_user_weibo_test(5648343109, 10)
