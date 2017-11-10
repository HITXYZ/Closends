"""
    @author: Jiale Xu
    @date: 2017/10/05
    @desc: Scraper for sina weibo
"""
import datetime
import logging
import os
import requests
from bs4 import BeautifulSoup
from urllib.request import quote
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from exceptions import LoginError, MethodParamError
from weibo.items import WeiboUserItem, WeiboContentItem, WeiboRepostContentItem
from base_spider import SocialMediaSpider


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

user_info_container = 230283
user_weibo_container = 107603
user_follow_container = 100505
user_fans_container = 100505

login_url = 'https://passport.weibo.cn/signin/login'
user_profile_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid1}&luicode=10000012&type=uid&value={uid2}'
user_info_url = 'https://m.weibo.cn/api/container/getIndex?containerid=230283{uid1}_-_INFO' \
                '&title=%25E5%259F%25BA%25E6%259C%25AC%25E4%25BF%25A1%25E6%2581%25AF&luicode=10000011' \
                '&lfid=230283{uid2}'
user_weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid1}' \
                 '&luicode=10000012&containerid=107603{uid2}&page={page}'
user_follow_url = 'https://m.weibo.cn/api/container/getSecond?containerid=100505{uid}_-_FOLLOWERS&page={page}'
user_fans_url = 'https://m.weibo.cn/api/container/getSecond?containerid=100505{uid}_-_FANS&page={page}'
search_url = 'http://s.weibo.com/user/{user}&Refer=weibo_user'

log_file = "./logs/weibo-log-%s.log" % (datetime.date.today())
logging.basicConfig(filename=log_file, format="%(asctime)s - %(name)s - %(levelname)s - %(module)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S %p", level=10)


class WeiboSpider(SocialMediaSpider):
    def __init__(self):
        self.cookies = {}
        self.scraped_infos = {}
        self.scraped_follows = {}
        self.scraped_fans = {}
        self.scraped_weibos = {}

    def scrape_info(self, id=None):
        if not isinstance(id, int):
            raise MethodParamError('Parameter \'id\' isn\'t an instance of type \'int\'!')
        logging.info('Scraping info of weibo user: %d...' % id)
        item = WeiboUserItem()
        item.id = id

        # 通过主页请求获取关注数、粉丝数、头像url
        response = requests.get(user_profile_url.format(uid1=id, uid2=id))
        result = response.json()
        item.follow_count = result.get('userInfo').get('follow_count')
        item.fans_count = result.get('userInfo').get('followers_count')
        item.avatar_url = result.get('userInfo').get('profile_image_url')

        # 通过详细资料请求获取详细资料
        response = requests.get(user_info_url.format(uid1=id, uid2=id))
        result = response.json()
        for card in result.get('cards'):
            if card.get('card_type') != 11:
                continue
            for card_inner in card.get('card_group'):
                if card_inner.get('card_type') != 41:
                    continue
                item_name = card_inner.get('item_name')
                item_content = card_inner.get('item_content')
                if item_name == '昵称':
                    item.name = item_content
                elif item_name == '性别':
                    item.gender = item_content
                elif item_name == '所在地':
                    item.location = item_content
                elif item_name == '简介':
                    item.description = item_content
                elif item_name == '注册时间':
                    item.signup_time = item_content

        # 通过用户微博请求获取用户微博数
        response = requests.get(user_weibo_url.format(uid1=id, uid2=id, page=1))
        result = response.json()
        item.weibo_count = result.get('cardlistInfo').get('total')
        logging.info('Succeed in scraping info of weibo user: %d.' % id)
        self.scraped_infos[id] = item
        return item

    def scrape_follows(self, id=None, number=0):
        if not isinstance(id, int):
            raise MethodParamError('Parameter \'id\' isn\'t an instance of type \'int\'!')
        if not isinstance(number, int):
            raise MethodParamError('Parameter \'number\' isn\'t an instance of type \'int\'!')
        logging.info('Scraping follows of weibo user: %d...' % id)
        response = requests.get(user_follow_url.format(uid=id, page=1))
        result = response.json()
        total = result.get('count')
        if number <= 0:
            need_count = 10
        else:
            need_count = number if number < total else total
        finish_count = 0
        follows = []
        position = 0
        while finish_count < need_count:
            position += 1
            response = requests.get(user_follow_url.format(uid=id, page=position))
            result = response.json()
            for card in result.get('cards'):
                if finish_count >= need_count:
                    break
                user = card.get('user')
                item = WeiboUserItem()
                item.id = user.get('id')
                item.name = user.get('screen_name')
                item.gender = '男' if user.get('gender') == 'm' else '女'
                item.avatar_url = user.get('profile_image_url')
                item.description = user.get('description')
                item.weibo_count = user.get('statuses_count')
                item.follow_count = user.get('follow_count')
                item.fans_count = user.get('followers_count')
                response_info = requests.get(user_info_url.format(uid1=item.id, uid2=item.id))
                result_info = response_info.json()
                for card in result_info.get('cards'):
                    if card.get('card_type') != 11:
                        continue
                    for card_inner in card.get('card_group'):
                        if card_inner.get('card_type') != 41:
                            continue
                        item_name = card_inner.get('item_name')
                        item_content = card_inner.get('item_content')
                        if item_name == '所在地':
                            item.location = item_content
                        elif item_name == '注册时间':
                            item.signup_time = item_content
                follows.append(item)
                finish_count += 1
        logging.info('Succeed in scraping follows of weibo user: %d.' % id)
        self.scraped_follows[id] = follows
        return follows

    def scrape_fans(self, id=None, number=0):
        if not isinstance(id, int):
            raise MethodParamError('Parameter \'id\' isn\'t an instance of type \'int\'!')
        if not isinstance(number, int):
            raise MethodParamError('Parameter \'number\' isn\'t an instance of type \'int\'!')
        logging.info('Scraping fans of weibo user: %d...' % id)
        response = requests.get(user_fans_url.format(uid=id, page=1))
        result = response.json()
        total = result.get('count')
        if number <= 0:
            need_count = 10
        else:
            need_count = number if number < total else total
        finish_count = 0
        fans = []
        position = 0
        while finish_count < need_count:
            position += 1
            response = requests.get(user_fans_url.format(uid=id, page=position))
            result = response.json()
            for card in result.get('cards'):
                if finish_count >= need_count:
                    break
                user = card.get('user')
                item = WeiboUserItem()
                item.id = user.get('id')
                item.name = user.get('screen_name')
                item.gender = '男' if user.get('gender') == 'm' else '女'
                item.avatar_url = user.get('profile_image_url')
                item.description = user.get('description')
                item.weibo_count = user.get('statuses_count')
                item.follow_count = user.get('follow_count')
                item.fans_count = user.get('followers_count')
                response_info = requests.get(user_info_url.format(uid1=item.id, uid2=item.id))
                result_info = response_info.json()
                for card in result_info.get('cards'):
                    if card.get('card_type') != 11:
                        continue
                    for card_inner in card.get('card_group'):
                        if card_inner.get('card_type') != 41:
                            continue
                        item_name = card_inner.get('item_name')
                        item_content = card_inner.get('item_content')
                        if item_name == '所在地':
                            item.location = item_content
                        elif item_name == '注册时间':
                            item.signup_time = item_content
                fans.append(item)
                finish_count += 1
        logging.info('Succeed in scraping follows of weibo user: %d.' % id)
        self.scraped_fans[id] = fans
        return fans

    def scrape_weibo(self, id=None, number=0):
        if not isinstance(id, int):
            raise MethodParamError('Parameter \'id\' isn\'t an instance of type \'int\'!')
        if not isinstance(number, int):
            raise MethodParamError('Parameter \'number\' isn\'t an instance of type \'int\'!')
        logging.info('Scraping weibos of weibo user: %d...' % id)
        response = requests.get(user_weibo_url.format(uid1=id, uid2=id, page=1))
        result = response.json()
        total = result.get('cardlistInfo').get('total')
        if number <= 0:
            need_count = 10
        else:
            need_count = number if number < total else total
        finish_count = 0
        weibos = []
        position = 0
        while finish_count < need_count:
            position += 1
            response = requests.get(user_weibo_url.format(uid1=id, uid2=id, page=position))
            result = response.json()
            for card in result.get('cards'):
                if finish_count >= need_count:
                    break
                if card.get('card_type') != 9:
                    continue
                mblog = card.get('mblog')
                if 'retweeted_status' in mblog.keys():
                    item = WeiboRepostContentItem()
                    retweet = mblog.get('retweeted_status')
                    item.source_id = retweet.get('id')
                    if retweet.get('user') is not None:     # 原微博可能已被删除
                        item.source_owner = retweet.get('user').get('id')
                    item.source_time = retweet.get('created_at')
                    item.source_content = retweet.get('text')
                    if 'pics' in retweet.keys():
                        for pic in retweet.get('pics'):
                            item.source_pictures.append(pic.get('url'))
                else:
                    item = WeiboContentItem()
                item.id = mblog.get('id')
                item.owner = mblog.get('user').get('id')
                item.time = mblog.get('created_at')
                item.content = mblog.get('text')
                if 'pics' in mblog.keys():
                    for pic in mblog.get('pics'):
                        item.pictures.append(pic.get('url'))
                item.source = mblog.get('source')
                weibos.append(item)
                finish_count += 1
        logging.info('Succeed in scraping weibos of weibo user: %d.' % id)
        self.scraped_weibos[id] = weibos
        return weibos

    def search_user(self, user=None, number=1):
        if user is None:
            raise MethodParamError('The user name can\'t be empty!')
        driver = webdriver.PhantomJS(executable_path='../phantomjs', service_log_path=os.path.devnull)
        driver.get(search_url.format(user=quote(user)))
        wait = WebDriverWait(driver, 3)
        try:
            wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'pl_personlist')))
        except TimeoutException:    # 未查找到用户
            return []
        items = driver.find_elements_by_class_name('list_person')
        if len(items) >= number:    # 截取前number个搜索结果
            items = items[:number]
        return [item.get_attribute('innerHTML') for item in items]

if __name__ == '__main__':
    spider = WeiboSpider()
    # info = spider.scrape_info(5648343109)
    # follows = spider.scrape_follows(5648343109, 20)
    # fans = spider.scrape_fans(5648343109, 20)
    # weibos = spider.scrape_weibo(3087483957, 20)
    users = spider.search_user('于晟建', 3)

    # print(info)
    # for follow in follows:
    #     print(follow)
    # for fan in fans:
    #     print(fans)
    # for weibo in weibos:
    #     print(weibo)
    for user in users:
        print(user)