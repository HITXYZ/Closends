"""
@author: Jiale Xu
@date: 2017/11/01
@desc: Scraper for zhihu.
"""

import csv
import re
import time
import requests
from bs4 import BeautifulSoup
from closends.spider.zhihu_items import *
from closends.spider.base_exceptions import MethodParamError
from closends.spider.base_spider import SocialMediaSpider
from closends.spider.base_configs import zhihu_activity_url, zhihu_answer_query, zhihu_answer_url, zhihu_followers_query, \
    zhihu_followers_url, zhihu_follows_query, zhihu_follows_url, zhihu_headers, zhihu_question_answers_url, \
    zhihu_question_query, zhihu_question_url, zhihu_user_answers_url, zhihu_user_query, zhihu_user_questions_url, \
    zhihu_user_url, log_path, log_zhihu

if log_zhihu:
    import logging
    import datetime

    log_file = log_path + "/zhihu-log-%s.log" % (datetime.date.today())
    logging.basicConfig(filename=log_file, format="%(asctime)s - %(name)s - %(levelname)s - %(module)s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S %p", level=10)


class ZhihuSpider(SocialMediaSpider):
    def __init__(self):
        self.scraped_infos = {}
        self.scraped_follows = {}
        self.scraped_followers = {}
        self.scraped_questions = {}
        self.scraped_user_questions = {}
        self.scraped_answers = {}
        self.scraped_question_answers = {}
        self.scraped_user_answers = {}

    def scrape_user_info(self, user):
        if not isinstance(user, str):
            raise MethodParamError('Parameter \'user\' isn\'t an instance of type \'str\'!')
        if log_zhihu:
            logging.info('Scraping info of zhihu user: %s...' % user)
        response = requests.get(zhihu_user_url.format(user=user, include=zhihu_user_query), headers=zhihu_headers)
        if response.status_code == 404:  # 用户不存在或账号被封禁
            if log_zhihu:
                logging.warning('404 error. The user doesn\'t exist or has been blocked.')
            return None
        result = response.json()
        if result.get('error') is not None:  # 身份未经过验证
            if log_zhihu:
                logging.warning('Your identity hasn\'t been confirmed.')
            return None

        item = ZhihuUserItem()
        item.id = result.get('id')
        item.name = result.get('name')
        item.gender = result.get('gender')
        item.avatar_url = result.get('avatar_url')
        if 'business' in result.keys():
            item.business = result.get('business').get('name')
        item.headline = result.get('headline')
        item.description = result.get('description')
        item.question_count = result.get('question_count')
        item.answer_count = result.get('answer_count')
        item.article_count = result.get('articles_count')
        item.voteup_count = result.get('voteup_count')
        item.thanked_count = result.get('thanked_count')
        item.favorited_count = result.get('favorited_count')
        item.following_count = result.get('following_count')
        item.follower_count = result.get('follower_count')
        item.following_topic_count = result.get('following_topic_count')
        item.following_column_count = result.get('following_columns_count')
        item.following_question_count = result.get('following_question_count')
        item.following_favlist_count = result.get('following_favlists_count')
        educations = result.get('educations')
        if educations is not None:
            for education in educations:
                edu_item = ZhihuEducationItem()
                edu_item.school = education.get('school').get('name')
                if 'major' in education.keys():
                    edu_item.major = education.get('major').get('name')
                item.educations.append(edu_item)
        employments = result.get('employments')
        if employments is not None:
            for employment in employments:
                emp_item = ZhihuEmploymentItem()
                if 'company' in employment.keys():
                    emp_item.company = employment.get('company').get('name')
                if 'job' in employment.keys():
                    emp_item.job = employment.get('job').get('name')
                item.employments.append(emp_item)
        locations = result.get('locations')
        if locations is not None:
            for location in locations:
                item.locations.append(location.get('name'))
        if log_zhihu:
            logging.info('Succeed in scraping info of zhihu user: %s.' % user)
        self.scraped_infos[user] = item
        return item

    def scrape_user_follows(self, user, number=0):
        if not isinstance(user, str):
            raise MethodParamError('Parameter \'user\' isn\'t an instance of type \'str\'!')
        if not isinstance(number, int):
            raise MethodParamError('Parameter \'number\' isn\'t an instance of type \'int\'!')
        if log_zhihu:
            logging.info('Scraping follows of zhihu user: %s...' % user)
        response = requests.get(zhihu_follows_url.format(user=user, include=zhihu_follows_query, offset=0, limit=20),
                                headers=zhihu_headers)
        if response.status_code == 404:  # 用户不存在或账号被封禁
            if log_zhihu:
                logging.warning('404 error. The user doesn\'t exist or has been blocked.')
            return []
        result = response.json()
        total = result.get('paging').get('totals')
        if number <= 0:
            need_count = 10
        else:
            need_count = number if number < total else total
        finish_count = 0
        url_tokens = []
        for data in result.get('data'):
            if finish_count >= need_count:
                break
            url_tokens.append(data.get('url_token'))
            finish_count += 1
        if finish_count < need_count:
            while not result.get('paging').get('is_end'):
                if finish_count >= need_count:
                    break
                next_page = result.get('paging').get('next')
                result = requests.get(next_page, headers=zhihu_headers).json()
                for data in result.get('data'):
                    if finish_count >= need_count:
                        break
                    url_tokens.append(data.get('url_token'))
                    finish_count += 1
        follows = []
        for url_token in url_tokens:
            item = self.scrape_user_info(user=url_token)
            follows.append(item)
        if log_zhihu:
            logging.info('Succeed in scraping follows of zhihu user: %s.' % user)
        self.scraped_follows[user] = follows
        return follows

    def scrape_user_fans(self, user, number=0):
        if not isinstance(user, str):
            raise MethodParamError('Parameter \'user\' isn\'t an instance of type \'str\'!')
        if not isinstance(number, int):
            raise MethodParamError('Parameter \'number\' isn\'t an instance of type \'int\'!')
        if log_zhihu:
            logging.info('Scraping followers of zhihu user: %s...' % user)
        response = requests.get(zhihu_followers_url.format(user=user, include=zhihu_followers_query, offset=0, limit=20), headers=zhihu_headers)
        if response.status_code == 404:  # 用户不存在或账号被封禁
            if log_zhihu:
                logging.warning('404 error. The user doesn\'t exist or has been blocked.')
            return []
        result = response.json()
        total = result.get('paging').get('totals')
        if number <= 0:
            need_count = 10
        else:
            need_count = number if number < total else total
        finish_count = 0
        url_tokens = []
        for data in result.get('data'):
            if finish_count >= need_count:
                break
            url_tokens.append(data.get('url_token'))
            finish_count += 1
        if finish_count < need_count:
            while not result.get('paging').get('is_end'):
                if finish_count >= need_count:
                    break
                next_page = result.get('paging').get('next')
                result = requests.get(next_page, headers=zhihu_headers).json()
                for data in result.get('data'):
                    if finish_count >= need_count:
                        break
                    url_tokens.append(data.get('url_token'))
                    finish_count += 1
        fans = []
        for url_token in url_tokens:
            item = self.scrape_user_info(user=url_token)
            fans.append(item)
        if log_zhihu:
            logging.info('Succeed in scraping followers of zhihu user: %s.' % user)
        self.scraped_followers[user] = fans
        return fans

    def scrape_user_activities(self, user):
        if not isinstance(user, str):
            raise MethodParamError('Parameter \'user\' isn\'t an instance of type \'str\'!')
        if log_zhihu:
            logging.info('Scraping activities of zhihu user: %s...' % user)
        timestamp = int(time.time())
        response = requests.get(zhihu_activity_url.format(user=user, limit=10, after=timestamp), headers=zhihu_headers)
        result = response.json()
        activities = []
        for data in result.get('data'):
            item = ZhihuActivityItem()
            item.id = int(data.get('id'))
            item.verb = data.get('verb')
            item.create_time = time.ctime(data.get('created_time'))
            item.actor = data.get('actor').get('url_token')
            target = data.get('target')
            if item.verb == 'QUESTION_CREATE' or item.verb == 'QUESTION_FOLLOW':  # 关注了问题，添加了问题
                item.target_user_name = target.get('author').get('name')
                item.target_user_avatar = target.get('author').get('avatar_url')
                item.target_user_headline = target.get('author').get('headline')
                item.target_user_url = 'https://www.zhihu.com/people/{user}/activities'.format(
                    user=target.get('author').get('url_token'))
                item.target_title = target.get('title')
                item.target_title_url = 'https://www.zhihu.com/question/{id}'.format(id=target.get('id'))
            elif item.verb == 'ANSWER_VOTE_UP' or item.verb == 'ANSWER_CREATE':  # 赞同了回答，回答了问题
                item.target_user_name = target.get('author').get('name')
                item.target_user_avatar = target.get('author').get('avatar_url')
                item.target_user_headline = target.get('author').get('headline')
                item.target_user_url = 'https://www.zhihu.com/people/{user}/activities'.format(
                    user=target.get('author').get('url_token'))
                item.target_title = target.get('question').get('title')
                item.target_title_url = 'https://www.zhihu.com/question/{id}'.format(id=target.get('question').get('id'))
                item.target_content = target.get('excerpt')
                item.target_content_url = 'https://www.zhihu.com/question/{qid}/answer/{aid}'.format(
                    qid=target.get('question').get('id'), aid=target.get('id'))
                item.thumbnail = target.get('thumbnail')
            elif item.verb == 'MEMBER_VOTEUP_ARTICLE' or item.verb == 'MEMBER_CREATE_ARTICLE':  # 赞了文章，发表了文章
                item.target_user_name = target.get('author').get('name')
                item.target_user_avatar = target.get('author').get('avatar_url')
                item.target_user_headline = target.get('author').get('headline')
                item.target_user_url = 'https://www.zhihu.com/people/{user}/activities'.format(
                    user=target.get('author').get('url_token'))
                item.target_title = target.get('title')
                item.target_title_url = 'https://zhuanlan.zhihu.com/p/{id}'.format(id=target.get('id'))
                item.target_content = target.get('excerpt')
                item.target_content_url = 'https://zhuanlan.zhihu.com/p/{id}'.format(id=target.get('id'))
                item.thumbnail = target.get('image_url')
            elif item.verb == 'TOPIC_FOLLOW' or item.verb == 'TOPIC_CREATE':  # 关注了话题，创建了话题
                item.target_title = target.get('name')
                item.target_title_url = item.target_title_url = 'https://www.zhihu.com/topic/{id}'.format(
                    id=target.get('id'))
                item.thumbnail = target.get('avatar_url')
            elif item.verb == 'MEMBER_FOLLOW_COLUMN' or item.verb == 'MEMBER_CREATE_COLUMN':  # 关注了收藏夹，创建了收藏夹
                item.target_user_name = target.get('author').get('name')
                item.target_user_avatar = target.get('author').get('avatar_url')
                item.target_user_headline = target.get('author').get('headline')
                item.target_user_url = 'https://www.zhihu.com/people/{user}/activities'.format(
                    user=target.get('author').get('url_token'))
                item.target_title = target.get('title')
                item.target_title_url = 'https://zhuanlan.zhihu.com/{id}'.format(id=target.get('id'))
                item.thumbnail = target.get('image_url')
            elif item.verb == 'MEMBER_CREATE_PIN' or item.verb == 'MEMBER_FOLLOW_PIN':  # 发布了想法，关注了想法
                item.target_user_name = target.get('author').get('name')
                item.target_user_avatar = target.get('author').get('avatar_url')
                item.target_user_headline = target.get('author').get('headline')
                item.target_user_url = 'https://www.zhihu.com/people/{user}/activities'.format(
                    user=target.get('author').get('url_token'))
                item.target_content = target.get('excerpt_new')
                item.target_content_url = 'https://www.zhihu.com/pin/{id}'.format(id=target.get('id'))
            item.action_text = data.get('action_text')
            activities.append(item)
        if log_zhihu:
            logging.info('Succeed in scraping activities of zhihu user: %s.' % user)
        return activities

    def scrape_question_by_id(self, id=0):
        if not isinstance(id, int):
            raise MethodParamError('Parameter \'id\' isn\'t an instance of type \'int\'!')
        if log_zhihu:
            logging.info('Scraping question of id: %d...' % id)
        response = requests.get(zhihu_question_url.format(id=id, include=zhihu_question_query), headers=zhihu_headers)
        if response.status_code == 404:
            if log_zhihu:
                logging.warning('404 error. The question doesn\'t exist.')
            return None
        result = response.json()
        item = ZhihuQuestionItem()
        item.id = result.get('id')
        item.title = result.get('title')
        item.create_time = time.ctime(result.get('created'))
        item.update_time = time.ctime(result.get('updated_time'))
        page = requests.get('https://www.zhihu.com/question/%d' % id, headers=zhihu_headers)
        bs = BeautifulSoup(page.text, 'lxml')
        content_div = bs.find('div', {'class': 'QuestionRichText'})
        if content_div is not None:
            item.content = re.search(r'<span.*?>(.*)</span>', str(content_div.div.span)).group(1)
        item.follower_count = result.get('follower_count')
        item.visit_count = result.get('visit_count')
        item.comment_count = result.get('comment_count')
        topics = result.get('topics')
        if topics is not None:
            for topic in topics:
                item.topics.append(topic.get('name'))
        if log_zhihu:
            logging.info('Succeed in scraping question of id: %d.' % id)
        self.scraped_questions[id] = item
        return item

    def scrape_questions_by_user(self, user, number=0):
        if not isinstance(user, str):
            raise MethodParamError('Parameter \'user\' isn\'t an instance of type \'str\'!')
        if not isinstance(number, int):
            raise MethodParamError('Parameter \'number\' isn\'t an instance of type \'int\'!')
        if log_zhihu:
            logging.info('Scraping questions of zhihu user: %s...' % user)
        response = requests.get(zhihu_user_questions_url.format(user=user, offset=0, limit=20), headers=zhihu_headers)
        if response.status_code == 404:  # 用户不存在或账号被封禁
            if log_zhihu:
                logging.warning('404 error. The user doesn\'t exist or has been blocked.')
            return []
        result = response.json()
        total = result.get('paging').get('totals')
        if number <= 0:
            need_count = 10
        else:
            need_count = number if number < total else total
        finish_count = 0
        question_ids = []
        for data in result.get('data'):
            if finish_count >= need_count:
                break
            question_ids.append(data.get('id'))
            finish_count += 1
        if finish_count < need_count:
            position = 0
            while not result.get('paging').get('is_end'):
                if finish_count >= need_count:
                    break
                position += 20
                next_page = zhihu_user_questions_url.format(user=user, offset=position, limit=20)
                result = requests.get(next_page, headers=zhihu_headers).json()
                for data in result.get('data'):
                    if finish_count >= need_count:
                        break
                    question_ids.append(data.get('id'))
                    finish_count += 1
        questions = []
        for question_id in question_ids:
            item = self.scrape_question_by_id(id=question_id)
            questions.append(item)
        if log_zhihu:
            logging.info('Succeed in scraping questions of zhihu user: %s.' % user)
        self.scraped_user_questions[user] = questions
        return questions

    def scrape_answer_by_id(self, id):
        if not isinstance(id, int):
            raise MethodParamError('Parameter \'id\' isn\'t an instance of type \'int\'!')
        if log_zhihu:
            logging.info('Scraping answer of id: %d...' % id)
        response = requests.get(zhihu_answer_url.format(id=id, include=zhihu_answer_query), headers=zhihu_headers)
        if response.status_code == 404:
            if log_zhihu:
                logging.warning('404 error. The answer doesn\'t exist.')
            return None
        result = response.json()
        item = ZhihuAnswerItem()
        item.id = result.get('id')
        item.author = result.get('author').get('name')
        item.question_id = result.get('question').get('id')
        item.create_time = time.ctime(result.get('created_time'))
        item.update_time = time.ctime(result.get('updated_time'))
        page = requests.get('https://www.zhihu.com/question/%d/answer/%d' % (item.question_id, id), headers=zhihu_headers)
        bs = BeautifulSoup(page.text, 'lxml')
        content_span = bs.find('div', {'class': 'RichContent'}).div.span
        content = re.search(r'<span.*?>(.*)</span>', str(content_span)).group(1)
        item.content = content
        item.voteup_count = result.get('voteup_count')
        item.comment_count = result.get('comment_count')
        if log_zhihu:
            logging.info('Succeed in scraping answer of id: %d.' % id)
        self.scraped_answers[id] = item
        return item

    def scrape_answers_by_question(self, id, number=0):
        if not isinstance(id, int):
            raise MethodParamError('Parameter \'id\' isn\'t an instance of type \'int\'!')
        if not isinstance(number, int):
            raise MethodParamError('Parameter \'number\' isn\'t an instance of type \'int\'!')
        if log_zhihu:
            logging.info('Scraping answers of question: %d...' % id)
        response = requests.get(zhihu_question_answers_url.format(id=id, offset=0, limit=20), headers=zhihu_headers)
        if response.status_code == 404:  # 问题不存在
            if log_zhihu:
                logging.warning('404 error. The question doesn\'t exist.')
            return []
        result = response.json()
        total = result.get('paging').get('totals')
        if number <= 0:
            need_count = 10
        else:
            need_count = number if number < total else total
        finish_count = 0
        answer_ids = []
        for data in result.get('data'):
            if finish_count >= need_count:
                break
            answer_ids.append(data.get('id'))
            finish_count += 1
        if finish_count < need_count:
            while not result.get('paging').get('is_end'):
                if finish_count >= need_count:
                    break
                next_page = result.get('paging').get('next')
                result = requests.get(next_page, headers=zhihu_headers).json()
                for data in result.get('data'):
                    if finish_count >= need_count:
                        break
                    answer_ids.append(data.get('id'))
                    finish_count += 1
        answers = []
        for answer_id in answer_ids:
            item = self.scrape_answer_by_id(id=answer_id)
            answers.append(item)
        if log_zhihu:
            logging.info('Succeed in scraping answers of question: %d.' % id)
        self.scraped_question_answers[id] = answers
        return answers

    def scrape_answers_by_user(self, user, number=0):
        if not isinstance(user, str):
            raise MethodParamError('Parameter \'user\' isn\'t an instance of type \'str\'!')
        if not isinstance(number, int):
            raise MethodParamError('Parameter \'number\' isn\'t an instance of type \'int\'!')
        if log_zhihu:
            logging.info('Scraping answers of zhihu user: %s...' % user)
        response = requests.get(zhihu_user_answers_url.format(user=user, offset=0, limit=20), headers=zhihu_headers)
        if response.status_code == 404:  # 用户不存在或账号被封禁
            if log_zhihu:
                logging.warning('404 error. The user doesn\'t exist or has been blocked.')
            return []
        result = response.json()
        total = result.get('paging').get('totals')
        if number <= 0:
            need_count = 10
        else:
            need_count = number if number < total else total
        finish_count = 0
        answer_ids = []
        for data in result.get('data'):
            if finish_count >= need_count:
                break
            answer_ids.append(data.get('id'))
            finish_count += 1
        if finish_count < need_count:
            position = 0
            while not result.get('paging').get('is_end'):
                if finish_count >= need_count:
                    break
                position += 20
                next_page = zhihu_user_answers_url.format(user=user, offset=position, limit=20)
                result = requests.get(next_page, headers=zhihu_headers).json()
                for data in result.get('data'):
                    if finish_count >= need_count:
                        break
                    answer_ids.append(data.get('id'))
                    finish_count += 1
        answers = []
        for answer_id in answer_ids:
            item = self.scrape_answer_by_id(id=answer_id)
            answers.append(item)
        if log_zhihu:
            logging.info('Succeed in scraping answers of zhihu user: %s.' % user)
        self.scraped_user_answers[user] = answers
        return answers

    def save_user_info(self, user=None, directory='./products/'):
        if self.scraped_infos == {}:  # 未爬取过任何用户信息
            if log_zhihu:
                logging.warning('Haven\'t scraped info of any zhihu user.')
            return
        if user is None:  # 保存所有爬取过的用户信息
            csv_file = open(directory + 'all-user-info.csv', 'w')
            writer = csv.writer(csv_file)
            writer.writerow(('ID', '用户名', '性别', '头像链接', '行业', '一句话描述', '个人介绍', '提问数', '回答数',
                             '文章数', '被赞同数', '被感谢数', '被收藏数', '关注数', '粉丝数', '关注话题数', '关注专栏数',
                             '关注问题数', '关注收藏夹数', '教育经历', '职业经历', '居住地'))
            for name in self.scraped_infos.keys():
                info = self.scraped_infos.get(name)
                if not isinstance(info, ZhihuUserItem):
                    continue
                if info.gender == 0:
                    gender = '女'
                elif info.gender == 1:
                    gender = '男'
                else:
                    gender = '未知'
                writer.writerow((info.id, info.name, gender, info.avatar_url, info.business, info.headline,
                                 info.description, info.question_count, info.answer_count, info.article_count,
                                 info.voteup_count, info.thanked_count, info.favorited_count, info.following_count,
                                 info.follower_count, info.following_topic_count, info.following_column_count,
                                 info.following_question_count, info.following_favlist_count,
                                 '; '.join([str(edu) for edu in info.educations]),
                                 '; '.join([str(emp) for emp in info.employments]),
                                 '; '.join([str(loc) for loc in info.locations])))
            csv_file.close()
            if log_zhihu:
                logging.info('Succeed in saving infos of all scraped zhihu users.')
            return

        info = self.scraped_infos.get(user)
        if not isinstance(info, ZhihuUserItem):
            raise MethodParamError('\'info\' isn\'t an instance of ZhihuUserItem.')
        csv_file = open(directory + str(info.name) + '-info.csv', 'w')
        writer = csv.writer(csv_file)
        writer.writerow(('ID', '用户名', '性别', '头像链接', '行业', '一句话描述', '个人介绍', '提问数', '回答数',
                         '文章数', '被赞同数', '被感谢数', '被收藏数', '关注数', '粉丝数', '关注话题数', '关注专栏数',
                         '关注问题数', '关注收藏夹数', '教育经历', '职业经历', '居住地'))
        if info.gender == 0:
            gender = '女'
        elif info.gender == 1:
            gender = '男'
        else:
            gender = '未知'
        writer.writerow((info.id, info.name, gender, info.avatar_url, info.business, info.headline,
                         info.description, info.question_count, info.answer_count, info.article_count,
                         info.voteup_count, info.thanked_count, info.favorited_count, info.following_count,
                         info.follower_count, info.following_topic_count, info.following_column_count,
                         info.following_question_count, info.following_favlist_count,
                         '; '.join([str(edu) for edu in info.educations]),
                         '; '.join([str(emp) for emp in info.employments]),
                         '; '.join([str(loc) for loc in info.locations])))
        csv_file.close()
        if log_zhihu:
            logging.info('Succeed in saving info of zhihu user: %s.' % info.name)

    def save_user_follows(self, user, directory='./products/'):
        if self.scraped_follows == {}:
            if log_zhihu:
                logging.warning('Haven\'t scraped follows of any zhihu user.')
            return
        infos = self.scraped_follows.get(user)
        if not isinstance(infos, list):
            raise MethodParamError('Haven\'t scraped follows of zhihu user: %s' % user)
        csv_file = open(directory + str(user) + '-follows.csv', 'w')
        writer = csv.writer(csv_file)
        writer.writerow(('ID', '用户名', '性别', '头像链接', '行业', '一句话描述', '个人介绍', '提问数', '回答数',
                         '文章数', '被赞同数', '被感谢数', '被收藏数', '关注数', '粉丝数', '关注话题数', '关注专栏数',
                         '关注问题数', '关注收藏夹数', '教育经历', '职业经历', '居住地'))
        for info in infos:
            if not isinstance(info, ZhihuUserItem):
                continue
            if info.gender == 0:
                gender = '女'
            elif info.gender == 1:
                gender = '男'
            else:
                gender = '未知'
            writer.writerow((info.id, info.name, gender, info.avatar_url, info.business, info.headline,
                             info.description, info.question_count, info.answer_count, info.article_count,
                             info.voteup_count, info.thanked_count, info.favorited_count, info.following_count,
                             info.follower_count, info.following_topic_count, info.following_column_count,
                             info.following_question_count, info.following_favlist_count,
                             '; '.join([str(edu) for edu in info.educations]),
                             '; '.join([str(emp) for emp in info.employments]),
                             '; '.join([str(loc) for loc in info.locations])))
        csv_file.close()
        if log_zhihu:
            logging.info('Succeed in saving follows of zhihu user: %s.' % user)

    def save_user_fans(self, user, directory='./products/'):
        if self.scraped_followers == {}:
            if log_zhihu:
                logging.warning('Haven\'t scraped followers of any zhihu user.')
            return
        infos = self.scraped_followers.get(user)
        if not isinstance(infos, list):
            raise MethodParamError('Haven\'t scraped followers of zhihu user: %s' % user)
        csv_file = open(directory + str(user) + '-followers.csv', 'w')
        writer = csv.writer(csv_file)
        writer.writerow(('ID', '用户名', '性别', '头像链接', '行业', '一句话描述', '个人介绍', '提问数', '回答数',
                         '文章数', '被赞同数', '被感谢数', '被收藏数', '关注数', '粉丝数', '关注话题数', '关注专栏数',
                         '关注问题数', '关注收藏夹数', '教育经历', '职业经历', '居住地'))
        for info in infos:
            if not isinstance(info, ZhihuUserItem):
                continue
            if info.gender == 0:
                gender = '女'
            elif info.gender == 1:
                gender = '男'
            else:
                gender = '未知'
            writer.writerow((info.id, info.name, gender, info.avatar_url, info.business, info.headline,
                             info.description, info.question_count, info.answer_count, info.article_count,
                             info.voteup_count, info.thanked_count, info.favorited_count, info.following_count,
                             info.follower_count, info.following_topic_count, info.following_column_count,
                             info.following_question_count, info.following_favlist_count,
                             '; '.join([str(edu) for edu in info.educations]),
                             '; '.join([str(emp) for emp in info.employments]),
                             '; '.join([str(loc) for loc in info.locations])))
        csv_file.close()
        if log_zhihu:
            logging.info('Succeed in saving followers of zhihu user: %s.' % user)


if __name__ == '__main__':
    spider = ZhihuSpider()
    activities = spider.scrape_user_activities('miloyip')
    for activity in activities:
        print(activity)
