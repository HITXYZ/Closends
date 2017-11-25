"""
@author: Jiale Xu
@date: 2017/11/25
@desc: Test tieba spider.
"""
from tieba.spider import TiebaSpider


spider = TiebaSpider()


def scrape_user_info_test(user):
    info = spider.scrape_user_info(user)
    print(info)


def scrape_user_forums_test(user):
    forums = spider.scrape_user_forums(user)
    for forum in forums:
        print(forum)


def scrape_user_posts_test(user, number):
    posts = spider.scrape_user_posts(user, number)
    for post in posts:
        print(post)


scrape_user_info_test('愛你沒法說')
scrape_user_forums_test('愛你沒法說')
scrape_user_posts_test('愛你沒法說', 10)
