"""
@author: Jiale Xu
@date: 2017/10/05
@desc: Scraper for sina weibo.
"""
import re
import requests
from exceptions import MethodParamError
from weibo.items import WeiboUserItem, WeiboContentItem, WeiboRepostContentItem
from base_spider import SocialMediaSpider
from configs import weibo_user_fans_url, weibo_user_follow_url, weibo_user_info_url, \
    weibo_user_profile_url, weibo_user_weibo_url, log_path, log_weibo


if log_weibo:
    import logging
    import datetime
    log_file = log_path + "/weibo-log-%s.log" % (datetime.date.today())
    logging.basicConfig(filename=log_file, format="%(asctime)s - %(name)s - %(levelname)s - %(module)s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S %p", level=10)


class WeiboSpider(SocialMediaSpider):
    def __init__(self):
        self.cookies = {}
        self.scraped_infos = {}
        self.scraped_follows = {}
        self.scraped_fans = {}
        self.scraped_weibos = {}

    def scrape_user_info(self, id):
        if not isinstance(id, int):
            raise MethodParamError('Parameter \'id\' isn\'t an instance of type \'int\'!')
        if log_weibo:
            logging.info('Scraping info of weibo user: %d...' % id)
        item = WeiboUserItem()
        item.id = id
        item.profile_url = 'https://weibo.com/u/{uid}'.format(uid=id)

        # 通过主页请求获取关注数、粉丝数、头像url
        response = requests.get(weibo_user_profile_url.format(uid1=id, uid2=id))
        result = response.json()
        item.follow_count = result.get('userInfo').get('follow_count')
        item.fans_count = result.get('userInfo').get('followers_count')
        item.avatar_url = result.get('userInfo').get('profile_image_url')

        # 通过详细资料请求获取详细资料
        response = requests.get(weibo_user_info_url.format(uid1=id, uid2=id))
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
        response = requests.get(weibo_user_weibo_url.format(uid1=id, uid2=id, page=1))
        result = response.json()
        item.weibo_count = result.get('cardlistInfo').get('total')
        if log_weibo:
            logging.info('Succeed in scraping info of weibo user: %d.' % id)
        self.scraped_infos[id] = item
        return item

    def scrape_user_follows(self, id, number=0):
        if not isinstance(id, int):
            raise MethodParamError('Parameter \'id\' isn\'t an instance of type \'int\'!')
        if not isinstance(number, int):
            raise MethodParamError('Parameter \'number\' isn\'t an instance of type \'int\'!')
        if log_weibo:
            logging.info('Scraping follows of weibo user: %d...' % id)
        response = requests.get(weibo_user_follow_url.format(uid=id, page=1))
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
            response = requests.get(weibo_user_follow_url.format(uid=id, page=position))
            result = response.json()
            for card in result.get('cards'):
                if finish_count >= need_count:
                    break
                user = card.get('user')
                item = WeiboUserItem()
                item.id = user.get('id')
                item.profile_url = 'https://weibo.com/u/{uid}'.format(uid=item.id)
                item.name = user.get('screen_name')
                item.gender = '男' if user.get('gender') == 'm' else '女'
                item.avatar_url = user.get('profile_image_url')
                item.description = user.get('description')
                item.weibo_count = user.get('statuses_count')
                item.follow_count = user.get('follow_count')
                item.fans_count = user.get('followers_count')
                response_info = requests.get(weibo_user_info_url.format(uid1=item.id, uid2=item.id))
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
        if log_weibo:
            logging.info('Succeed in scraping follows of weibo user: %d.' % id)
        self.scraped_follows[id] = follows
        return follows

    def scrape_user_fans(self, id, number=0):
        if not isinstance(id, int):
            raise MethodParamError('Parameter \'id\' isn\'t an instance of type \'int\'!')
        if not isinstance(number, int):
            raise MethodParamError('Parameter \'number\' isn\'t an instance of type \'int\'!')
        if log_weibo:
            logging.info('Scraping fans of weibo user: %d...' % id)
        response = requests.get(weibo_user_fans_url.format(uid=id, page=1))
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
            response = requests.get(weibo_user_fans_url.format(uid=id, page=position))
            result = response.json()
            for card in result.get('cards'):
                if finish_count >= need_count:
                    break
                user = card.get('user')
                item = WeiboUserItem()
                item.id = user.get('id')
                item.profile_url = 'https://weibo.com/u/{uid}'.format(uid=item.id)
                item.name = user.get('screen_name')
                item.gender = '男' if user.get('gender') == 'm' else '女'
                item.avatar_url = user.get('profile_image_url')
                item.description = user.get('description')
                item.weibo_count = user.get('statuses_count')
                item.follow_count = user.get('follow_count')
                item.fans_count = user.get('followers_count')
                response_info = requests.get(weibo_user_info_url.format(uid1=item.id, uid2=item.id))
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
        if log_weibo:
            logging.info('Succeed in scraping follows of weibo user: %d.' % id)
        self.scraped_fans[id] = fans
        return fans

    def scrape_user_weibo(self, id, number=0):
        if not isinstance(id, int):
            raise MethodParamError('Parameter \'id\' isn\'t an instance of type \'int\'!')
        if not isinstance(number, int):
            raise MethodParamError('Parameter \'number\' isn\'t an instance of type \'int\'!')
        if log_weibo:
            logging.info('Scraping weibos of weibo user: %d...' % id)
        response = requests.get(weibo_user_weibo_url.format(uid1=id, uid2=id, page=1))
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
            response = requests.get(weibo_user_weibo_url.format(uid1=id, uid2=id, page=position))
            result = response.json()
            for card in result.get('cards'):
                if finish_count >= need_count:
                    break
                if card.get('card_type') != 9:
                    continue
                mblog = card.get('mblog')
                if 'retweeted_status' in mblog.keys():      # 转发微博
                    item = WeiboRepostContentItem()
                    retweet = mblog.get('retweeted_status')
                    item.content = retweet.get('text')
                    item.source_id = retweet.get('bid')
                    if 'pics' in retweet.keys():
                        for pic in retweet.get('pics'):
                            item.pictures.append(pic.get('url'))
                    if 'page_info' in retweet.keys():
                        item.media_pic = retweet.get('page_info').get('page_pic').get('url')
                        page_url = retweet.get('page_info').get('page_url')
                        if re.match(r'http://media\.weibo\.cn/article\?.*id=\d+', page_url):    # 移动端文章链接打不开，将其换为PC端链接
                            article_id = re.search(r'http://media\.weibo\.cn/article\?.*id=(\d+)', page_url).group(1)
                            item.media_url = 'https://weibo.com/ttarticle/p/show?id={id}'.format(id=article_id)
                        else:
                            item.media_url = page_url
                    if retweet.get('user') is not None:     # 原微博可能已被删除
                        item.source_url = 'https://weibo.com/{uid}/{bid}'.format(uid=retweet.get('user').get('id'),
                                                                                 bid=item.source_id)
                        item.source_owner.id = retweet.get('user').get('id')
                        item.source_owner.name = retweet.get('user').get('screen_name')
                        item.source_owner.avatar_url = retweet.get('user').get('profile_image_url')
                        item.source_owner.profile_url = 'https://weibo.com/u/{uid}'.format(uid=item.source_owner.id)
                    item.repost_reason = mblog.get('text')
                else:
                    item = WeiboContentItem()
                    item.content = mblog.get('text')
                    if 'pics' in mblog.keys():
                        for pic in mblog.get('pics'):
                            item.pictures.append(pic.get('url'))
                    if 'page_info' in mblog.keys():
                        item.media_pic = mblog.get('page_info').get('page_pic').get('url')
                        page_url = mblog.get('page_info').get('page_url')
                        if re.match(r'http://media\.weibo\.cn/article\?.*id=\d+', page_url):  # 移动端文章链接打不开，将其换为PC端链接
                            article_id = re.search(r'http://media\.weibo\.cn/article\?.*id=(\d+)', page_url).group(1)
                            item.media_url = 'https://weibo.com/ttarticle/p/show?id={id}'.format(id=article_id)
                        else:
                            item.media_url = page_url
                item.id = mblog.get('bid')
                item.order = int(mblog.get('id'))
                item.owner.id = mblog.get('user').get('id')
                item.owner.name = mblog.get('user').get('screen_name')
                item.owner.avatar_url = mblog.get('user').get('profile_image_url')
                item.owner.profile_url = 'https://weibo.com/u/{uid}'.format(uid=item.owner.id)
                item.url = 'https://weibo.com/{uid}/{bid}'.format(uid=item.owner.id, bid=item.id)
                item.time = mblog.get('created_at')
                item.source = mblog.get('source')
                weibos.append(item)
                finish_count += 1
        if log_weibo:
            logging.info('Succeed in scraping weibos of weibo user: %d.' % id)
        self.scraped_weibos[id] = weibos
        return weibos
