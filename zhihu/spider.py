"""
    @author: Jiale Xu
    @date: 2017/11/01
    @desc: Scraper for zhihu
"""
import csv
import re
import time
import datetime
import logging
import requests
from bs4 import BeautifulSoup
from zhihu.items import *
from exceptions import MethodParamError
from base_spider import SocialMediaSpider


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
}

user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
activity_url = 'https://www.zhihu.com/api/v4/members/{user}/activities?limit={limit}&after_id={after}&desktop=True'
question_url = 'https://www.zhihu.com/api/v4/questions/{id}?include={include}'
user_questions_url = 'https://www.zhihu.com/api/v4/members/{user}/questions?offset={offset}&limit={limit}'
answer_url = 'https://www.zhihu.com/api/v4/answers/{id}?include={include}'
user_answers_url = 'https://www.zhihu.com/api/v4/members/{user}/answers?offset={offset}&limit={limit}'
question_answers_url = 'https://www.zhihu.com/api/v4/questions/{id}/answers?offset={offset}&limit={limit}'

user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,' \
             'following_count,following_topic_count,following_question_count,following_favlists_count,' \
             'following_columns_count,answer_count,articles_count,question_count,favorited_count,is_bind_sina,' \
             'sina_weibo_url,sina_weibo_name,show_sina_weibo,thanked_count,description'
follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge'
followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge'
question_query = 'comment_count,follower_count,visit_count,topics'
answer_query = 'voteup_count,comment_count'

log_file = "./logs/zhihu-log-%s.log" % (datetime.date.today())
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

    def scrape_info(self, user=None):
        if user is None:
            return None
        logging.info('Scraping info of zhihu user: %s...' % user)
        print(user_url.format(user=user, include=user_query))
        response = requests.get(user_url.format(user=user, include=user_query), headers=headers)
        if response.status_code == 404:     # 用户不存在或账号被封禁
            logging.warning('404 error. The user doesn\'t exist or has been blocked.')
            return None
        result = response.json()
        if result.get('error') is not None: # 身份未经过验证
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
        logging.info('Succeed in scraping info of zhihu user: %s.' % user)
        self.scraped_infos[user] = item
        return item

    def scrape_follows(self, user=None, number=0):
        if user is None:
            return []
        logging.info('Scraping follows of zhihu user: %s...' % user)
        response = requests.get(follows_url.format(user=user, include=follows_query, offset=0, limit=20), headers=headers)
        if response.status_code == 404:     # 用户不存在或账号被封禁
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
                result = requests.get(next_page, headers=headers).json()
                for data in result.get('data'):
                    if finish_count >= need_count:
                        break
                    url_tokens.append(data.get('url_token'))
                    finish_count += 1
        follows = []
        for url_token in url_tokens:
            item = self.scrape_info(user=url_token)
            follows.append(item)
        logging.info('Succeed in scraping follows of zhihu user: %s.' % user)
        self.scraped_follows[user] = follows
        return follows

    def scrape_followers(self, user=None, number=0):
        if user is None:
            return []
        logging.info('Scraping followers of zhihu user: %s...' % user)
        response = requests.get(followers_url.format(user=user, include=followers_query, offset=0, limit=20), headers=headers)
        if response.status_code == 404:     # 用户不存在或账号被封禁
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
                result = requests.get(next_page, headers=headers).json()
                for data in result.get('data'):
                    if finish_count >= need_count:
                        break
                    url_tokens.append(data.get('url_token'))
                    finish_count += 1
        followers = []
        for url_token in url_tokens:
            item = self.scrape_info(user=url_token)
            followers.append(item)
        logging.info('Succeed in scraping followers of zhihu user: %s.' % user)
        self.scraped_followers[user] = followers
        return followers

    def scrape_activities(self, user=None):
        if not isinstance(user, str):
            raise MethodParamError('Parameter \'user\' must be an instance of \'str\'')
        timestamp = int(time.time())
        response = requests.get(activity_url.format(user=user, limit=10, after=timestamp), headers=headers)
        result = response.json()
        activities = []
        for data in result.get('data'):
            item = ZhihuActivityItem()
            item.id = data.get('id')
            item.verb = data.get('verb')
            item.create_time = time.ctime(data.get('created_time'))
            item.actor = data.get('actor').get('url_token')
            target = data.get('target')
            item.target_user_name = target.get('author').get('name')
            item.target_user_avatar = target.get('author').get('avatar_url')
            item.target_user_headline = target.get('author').get('headline')
            item.target_user_url = 'https://www.zhihu.com/people/{user}/activities'.format(user=target.get('author').get('url_token'))
            item.target_title = target.get('title')
            if item.verb == 'MEMBER_VOTEUP_ARTICLE':
                item.target_title_url = 'https://zhuanlan.zhihu.com/p/{id}'.format(id=target.get('id'))
            elif item.verb == 'QUESTION_FOLLOW' or item.verb == 'QUESTION_CREATE':
                item.target_title_url = 'https://www.zhihu.com/question/{id}'.format(id=target.get('id'))
            else:
                item.target_title_url = 'https://www.zhihu.com/question/{id}'.format(id=target.get('question').get('id'))
            if item.verb != 'QUESTION_FOLLOW' and item.verb != 'QUESTION_CREATE':
                item.target_content = target.get('excerpt_new')
                item.target_content_url = 'https://www.zhihu.com/answer/{id}'.format(id=target.get('id'))
            item.action_text = data.get('action_text')
            activities.append(item)
        return activities

    def scrape_question_by_id(self, id=0):
        if id == 0:
            return None
        logging.info('Scraping question of id: %d...' % id)
        response = requests.get(question_url.format(id=id, include=question_query), headers=headers)
        if response.status_code == 404:
            logging.warning('404 error. The question doesn\'t exist.')
            return None
        result = response.json()
        item = ZhihuQuestionItem()
        item.id = result.get('id')
        item.title = result.get('title')
        item.create_time = time.ctime(result.get('created'))
        item.update_time = time.ctime(result.get('updated_time'))
        page = requests.get('https://www.zhihu.com/question/%d' % id, headers=headers)
        bs = BeautifulSoup(page.text, 'lxml')
        content_span = bs.find('div', {'class': 'QuestionRichText'}).div.span
        content = re.search(r'<span.*?>(.*)</span>', str(content_span)).group(1)
        item.content = content
        item.follower_count = result.get('follower_count')
        item.visit_count = result.get('visit_count')
        item.comment_count = result.get('comment_count')
        topics = result.get('topics')
        for topic in topics:
            item.topics.append(topic.get('name'))
        logging.info('Succeed in scraping question of id: %d.' % id)
        self.scraped_questions[id] = item
        return item

    def scrape_questions_by_user(self, user=None, number=0):
        if user is None:
            return []
        logging.info('Scraping questions of zhihu user: %s...' % user)
        response = requests.get(user_questions_url.format(user=user, offset=0, limit=20), headers=headers)
        if response.status_code == 404:     # 用户不存在或账号被封禁
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
                next_page = user_questions_url.format(user=user, offset=position, limit=20)
                result = requests.get(next_page, headers=headers).json()
                for data in result.get('data'):
                    if finish_count >= need_count:
                        break
                    question_ids.append(data.get('id'))
                    finish_count += 1
        questions = []
        for question_id in question_ids:
            item = self.scrape_question_by_id(id=question_id)
            questions.append(item)
        logging.info('Succeed in scraping questions of zhihu user: %s.' % user)
        self.scraped_user_questions[user] = questions
        return questions

    def scrape_answer_by_id(self, id=0):
        if id == 0:
            return None
        logging.info('Scraping answer of id: %d...' % id)
        response = requests.get(answer_url.format(id=id, include=answer_query), headers=headers)
        if response.status_code == 404:
            logging.warning('404 error. The answer doesn\'t exist.')
            return None
        result = response.json()
        item = ZhihuAnswerItem()
        item.id = result.get('id')
        item.author = result.get('author').get('name')
        item.question_id = result.get('question').get('id')
        item.create_time = time.ctime(result.get('created_time'))
        item.update_time = time.ctime(result.get('updated_time'))
        page = requests.get('https://www.zhihu.com/question/%d/answer/%d' % (item.question_id, id), headers=headers)
        bs = BeautifulSoup(page.text, 'lxml')
        content_span = bs.find('div', {'class': 'RichContent'}).div.span
        content = re.search(r'<span.*?>(.*)</span>', str(content_span)).group(1)
        item.content = content
        item.voteup_count = result.get('voteup_count')
        item.comment_count = result.get('comment_count')
        logging.info('Succeed in scraping answer of id: %d.' % id)
        self.scraped_answers[id] = item
        return item

    def scrape_answers_by_question(self, id=0, number=0):
        if id == 0:
            return []
        logging.info('Scraping answers of question: %d...' % id)
        response = requests.get(question_answers_url.format(id=id, offset=0, limit=20), headers=headers)
        if response.status_code == 404:     # 问题不存在
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
                result = requests.get(next_page, headers=headers).json()
                for data in result.get('data'):
                    if finish_count >= need_count:
                        break
                    answer_ids.append(data.get('id'))
                    finish_count += 1
        answers = []
        for answer_id in answer_ids:
            item = self.scrape_answer_by_id(id=answer_id)
            answers.append(item)
        logging.info('Succeed in scraping answers of question: %d.' % id)
        self.scraped_question_answers[id] = answers
        return answers

    def scrape_answers_by_user(self, user=None, number=0):
        if user is None:
            return []
        logging.info('Scraping answers of zhihu user: %s...' % user)
        response = requests.get(user_answers_url.format(user=user, offset=0, limit=20), headers=headers)
        if response.status_code == 404:     # 用户不存在或账号被封禁
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
                next_page = user_answers_url.format(user=user, offset=position, limit=20)
                result = requests.get(next_page, headers=headers).json()
                for data in result.get('data'):
                    if finish_count >= need_count:
                        break
                    answer_ids.append(data.get('id'))
                    finish_count += 1
        answers = []
        for answer_id in answer_ids:
            item = self.scrape_answer_by_id(id=answer_id)
            answers.append(item)
        logging.info('Succeed in scraping answers of zhihu user: %s.' % user)
        self.scraped_user_answers[user] = answers
        return answers

    def save_info(self, user=None, directory='./products/'):
        if self.scraped_infos == {}:  # 未爬取过任何用户信息
            logging.warning('Haven\'t scraped info of any zhihu user.')
            return
        if user is None:    # 保存所有爬取过的用户信息
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
        logging.info('Succeed in saving info of zhihu user: %s.' % info.name)

    def save_user_follows(self, user, directory='./products/'):
        if self.scraped_follows == {}:
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
        logging.info('Succeed in saving follows of zhihu user: %s.' % user)

    def save_user_followers(self, user, directory='./products/'):
        if self.scraped_followers == {}:
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
        logging.info('Succeed in saving followers of zhihu user: %s.' % user)


if __name__ == '__main__':
    spider = ZhihuSpider()
    # info = spider.scrape_info(user='qing-shen-jue-qian')
    # print(info)
    # spider.save_info()

    # follows = spider.scrape_follows(user='qing-shen-jue-qian', number=1)
    # for follow in follows:
    #     print(follow)
    # spider.save_user_follows('qing-shen-jue-qian')

    # followers = spider.scrape_followers(user='qing-shen-jue-qian', number=1)
    # for follower in followers:
    #     print(follower)
    # spider.save_user_followers('qing-shen-jue-qian')

    # question = spider.scrape_question_by_id(67684166)
    # print(question)

    # answer = spider.scrape_answer_by_id(255562932)
    # print(answer)
    activities = spider.scrape_activities('excited-vczh')
    for activity in activities:
        print(activity)