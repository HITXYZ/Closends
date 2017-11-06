"""
    @author: Jiale Xu
    @date: 2017/11/01
    @desc: Scraper for zhihu
"""
import csv
import datetime
import logging
import requests
from zhihu.items import ZhihuUserItem, ZhihuEducationItem, ZhihuEmploymentItem
from exceptions import SpiderItemError


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
}

user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'

user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,' \
             'following_count,following_topic_count,following_question_count,following_favlists_count,' \
             'following_columns_count,answer_count,articles_count,question_count,favorited_count,is_bind_sina,' \
             'sina_weibo_url,sina_weibo_name,show_sina_weibo,thanked_count,description'
follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge'
followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge'

log_file = "../logs/zhihu/zhihu-log-%s.log" % (datetime.date.today())
logging.basicConfig(filename=log_file, format="%(asctime)s - %(name)s - %(levelname)s - %(module)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S %p", level=10)


class ZhihuSpider:
    def __init__(self):
        self.info = None
        self.follows = None
        self.followers = None
        self.follows_user = None
        self.followers_user = None

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
        self.info = item
        return item

    def scrape_follows(self, user=None, number=None):
        if user is None:
            return []
        logging.info('Scraping follows of zhihu user: %s...' % user)
        response = requests.get(follows_url.format(user=user, include=follows_query, offset=0, limit=20), headers=headers)
        if response.status_code == 404:     # 用户不存在或账号被封禁
            logging.warning('404 error. The user doesn\'t exist or has been blocked.')
            return []
        result = response.json()
        total = result.get('paging').get('totals')
        if number is None or number <= 0:
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
        self.follows = follows
        self.follows_user = user
        return follows

    def scrape_followers(self, user=None, number=None):
        if user is None:
            return []
        logging.info('Scraping followers of zhihu user: %s...' % user)
        response = requests.get(followers_url.format(user=user, include=followers_query, offset=0, limit=20), headers=headers)
        if response.status_code == 404:     # 用户不存在或账号被封禁
            logging.warning('404 error. The user doesn\'t exist or has been blocked.')
            return []
        result = response.json()
        total = result.get('paging').get('totals')
        if number is None or number <= 0:
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
        self.followers = followers
        self.followers_user = user
        return followers

    def save_info(self, directory='./products/'):
        if not isinstance(self.info, ZhihuUserItem):
            raise SpiderItemError('\'self.info\' is not an instance of ZhihuUserItem!')
        csv_file = open(directory + str(self.info.name) + '-info.csv', 'w')
        writer = csv.writer(csv_file)
        writer.writerow(('ID', '用户名', '性别', '头像链接', '行业', '一句话描述', '个人介绍', '提问数', '回答数',
                         '文章数', '被赞同数', '被感谢数', '被收藏数', '关注数', '粉丝数', '关注话题数', '关注专栏数',
                         '关注问题数', '关注收藏夹数', '教育经历', '职业经历', '居住地'))
        info = self.info
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
        logging.info('Succeed in saving info of zhihu user: %s.' % self.info.name)

    def save_follows(self, directory='./products/'):
        if not isinstance(self.follows, list):
            raise SpiderItemError('\'self.follows\' is not a list!')
        if self.follows_user is None:
            raise SpiderItemError('Haven\'t scraped follows of any zhihu user!')
        csv_file = open(directory + str(self.follows_user) + '-follows.csv', 'w')
        writer = csv.writer(csv_file)
        writer.writerow(('ID', '用户名', '性别', '头像链接', '行业', '一句话描述', '个人介绍', '提问数', '回答数',
                         '文章数', '被赞同数', '被感谢数', '被收藏数', '关注数', '粉丝数', '关注话题数', '关注专栏数',
                         '关注问题数', '关注收藏夹数', '教育经历', '职业经历', '居住地'))
        for info in self.follows:
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
        logging.info('Succeed in saving follows of zhihu user: %s.' % self.follows_user)

    def save_followers(self, directory='./products/'):
        if not isinstance(self.followers, list):
            raise SpiderItemError('\'self.followers\' is not a list!')
        if self.followers_user is None:
            raise SpiderItemError('Haven\'t scraped followers of any zhihu user!')
        csv_file = open(directory + str(self.followers_user) + '-followers.csv', 'w')
        writer = csv.writer(csv_file)
        writer.writerow(('ID', '用户名', '性别', '头像链接', '行业', '一句话描述', '个人介绍', '提问数', '回答数',
                         '文章数', '被赞同数', '被感谢数', '被收藏数', '关注数', '粉丝数', '关注话题数', '关注专栏数',
                         '关注问题数', '关注收藏夹数', '教育经历', '职业经历', '居住地'))
        for info in self.followers:
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
        logging.info('Succeed in saving followers of zhihu user: %s.' % self.followers_user)


if __name__ == '__main__':
    spider = ZhihuSpider()
    info = spider.scrape_info(user='qing-shen-jue-qian')
    print(info)
    spider.save_info()
    follows = spider.scrape_follows(user='qing-shen-jue-qian', number=20)
    for follow in follows:
        print(follow)
    spider.save_follows()
    followers = spider.scrape_followers(user='qing-shen-jue-qian', number=20)
    for follower in followers:
        print(follower)
    spider.save_followers()
