"""
@author: Jiale Xu
@date: 2017/11/25
@desc: Test zhihu spider.
"""
import time
from zhihu.spider import ZhihuSpider


spider = ZhihuSpider()


def scrape_user_info_test(user):
    info = spider.scrape_user_info(user)
    print(info)


def scrape_user_follows_test(user, number):
    follows = spider.scrape_user_follows(user, number)
    for follow in follows:
        print(follow)


def scrape_user_fans_test(user, number):
    fans = spider.scrape_user_fans(user, number)
    for fan in fans:
        print(fan)


def scrape_user_activities_test(user, after, number):
    activities = spider.scrape_user_activities(user, after, number)
    for activity in activities:
        print(activity)


def scrape_question_by_id_test(id):
    question = spider.scrape_question_by_id(id)
    print(question)


def scrape_questions_by_user_test(user, number):
    questions = spider.scrape_questions_by_user(user, number)
    for question in questions:
        print(question)


def scrape_answer_by_id_test(id):
    answer = spider.scrape_answer_by_id(id)
    print(answer)


def scrape_answers_by_question_test(id, number):
    answers = spider.scrape_answers_by_question(id, number)
    for answer in answers:
        print(answer)


def scrape_answers_by_user_test(user, number):
    answers = spider.scrape_answers_by_user(user, number)
    for answer in answers:
        print(answer)


scrape_user_info_test('excited-vczh')
scrape_user_follows_test('excited-vczh', 10)
scrape_user_fans_test('excited-vczh', 10)
scrape_user_activities_test('excited-vczh', int(time.time()), 15)
scrape_question_by_id_test(58035825)
scrape_questions_by_user_test('excited-vczh', 10)
scrape_answer_by_id_test(265325555)
scrape_answers_by_question_test(58035825, 10)
scrape_answers_by_user_test('excited-vczh', 10)
