"""
    @author: Jiale Xu
    @date: 2017/10/05
    @desc: Scraper for sina weibo
"""
import re
import traceback

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from exceptions import LoginError
from weibo.items import WeiboUserItem, WeiboContentItem, WeiboRepostContentItem


class WeiboSpider:
    def __init__(self, account, password):
        self.id = None
        self.account = account
        self.password = password
        self.driver = webdriver.PhantomJS('../phantomjs')
        self.item = None
        self.follow_id = {}
        self.fans_id = {}
        self.is_login = False

    def login(self):
        wait = WebDriverWait(self.driver, 5)
        self.driver.maximize_window()
        self.driver.get('https://weibo.cn/pub/')

        # Wap版微博登录入口
        login_entrance = self.driver.find_element_by_link_text('登录')
        login_entrance.click()
        wait.until(ec.visibility_of_element_located((By.ID, 'loginName')))

        # 模拟登录
        self.driver.find_element_by_id('loginName').clear()
        self.driver.find_element_by_id('loginName').send_keys(self.account)
        self.driver.find_element_by_id('loginPassword').clear()
        self.driver.find_element_by_id('loginPassword').send_keys(self.password)
        self.driver.find_element_by_id('loginAction').click()

        # 获取登录用户id
        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'tip2')))
        bs = BeautifulSoup(self.driver.page_source, 'lxml')
        tip = bs.find('div', {'class': 'tip2'}).a
        self.id = re.search(r'/(\d+)/profile', tip.attrs['href']).group(1)
        self.is_login = True

    def scrape_self_info(self):
        if not self.is_login:
            raise LoginError
        wait = WebDriverWait(self.driver, 5)
        self.driver.get('http://weibo.cn/')
        bs = BeautifulSoup(self.driver.page_source, 'lxml')

        # 获取用户id，微博数，关注数，粉丝数
        tips = bs.find('div', {'class': 'tip2'}).find_all('a')
        weibo_number = int(re.search(r'.*\[(\d+)\]', tips[0].get_text()).group(1))
        follow_number = int(re.search(r'.*\[(\d+)\]', tips[1].get_text()).group(1))
        fans_number = int(re.search(r'.*\[(\d+)\]', tips[2].get_text()).group(1))

        # 进入详细资料页面
        self.driver.get('https://weibo.cn/%s/info' % self.id)
        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'tip')))
        bs = BeautifulSoup(self.driver.page_source, 'lxml')

        # 获取用户昵称，性别，地址，生日，简介
        detail = str(bs.find('div', text='基本信息').next_sibling)
        user_name = re.search(r'昵称</a>:(.+?)<br/>', detail).group(1)
        sex = re.search(r'性别</a>:(.+?)<br/>', detail).group(1)
        address = re.search(r'地区</a>:(.+?)<br/>', detail).group(1)
        birthday = re.search(r'生日</a>:(.+?)<br/>', detail).group(1)
        synopsis = re.search(r'简介</a>:(.+?)<br/>', detail).group(1)

        item = WeiboUserItem()
        item.id = self.id
        item.name = user_name
        item.sex = sex
        item.address = address
        item.birthday = birthday
        item.synopsis = synopsis
        item.weibo_number = weibo_number
        item.follow_number = follow_number
        item.fans_number = fans_number
        print(item)
        self.item = item
        return item

    def scrape_follow_id(self, id=None):
        if not self.is_login:
            raise LoginError
        if id is None:
            id = self.id
        self.follow_id = {}
        wait = WebDriverWait(self.driver, 5)
        self.driver.get('https://weibo.cn/%s/follow' % id)
        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'pa')))
        bs = BeautifulSoup(self.driver.page_source, 'lxml')

        page_number = int(bs.find(id='pagelist').form.div.input.attrs['value'])
        follow_tables = bs.find_all('table')
        for table in follow_tables:
            link = table.find('td').next_sibling.a
            name = link.get_text()
            uid_match = re.search(r'weibo.cn/u/(.+)', link.attrs['href'])
            if uid_match is not None:
                uid = uid_match.group(1)
            else:
                uid = re.search(r'weibo.cn/(.+)', link.attrs['href']).group(1)
            self.follow_id[uid] = name

        for i in range(2, page_number + 1):
            self.driver.get('https://weibo.cn/%s/follow?page=%d' % (id, i))
            wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'pa')))
            bs = BeautifulSoup(self.driver.page_source, 'lxml')

            follow_tables = bs.find_all('table')
            for table in follow_tables:
                link = table.find('td').next_sibling.a
                name = link.get_text()
                uid_match = re.search(r'weibo.cn/u/(.+)', link.attrs['href'])
                if uid_match is not None:
                    uid = uid_match.group(1)
                else:
                    uid = re.search(r'weibo.cn/(.+)', link.attrs['href']).group(1)
                self.follow_id[uid] = name
        print(self.follow_id)
        return self.follow_id

    def scrape_fans_id(self, id=None):
        if not self.is_login:
            raise LoginError
        if id is None:
            id = self.id
        self.fans_id = {}
        wait = WebDriverWait(self.driver, 5)
        self.driver.get('https://weibo.cn/%s/fans' % id)
        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'pa')))
        bs = BeautifulSoup(self.driver.page_source, 'lxml')

        page_number = int(bs.find(id='pagelist').form.div.input.attrs['value'])
        fans_tables = bs.find_all('table')
        for table in fans_tables:
            link = table.find('td').next_sibling.a
            name = link.get_text()
            uid_match = re.search(r'weibo.cn/u/(.+)', link.attrs['href'])
            if uid_match is not None:
                uid = uid_match.group(1)
            else:
                uid = re.search(r'weibo.cn/(.+)', link.attrs['href']).group(1)
            self.fans_id[uid] = name

        for i in range(2, page_number + 1):
            self.driver.get('https://weibo.cn/%s/fans?page=%d' % (id, i))
            wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'pa')))
            bs = BeautifulSoup(self.driver.page_source, 'lxml')

            fans_tables = bs.find_all('table')
            for table in fans_tables:
                link = table.find('td').next_sibling.a
                name = link.get_text()
                uid_match = re.search(r'weibo.cn/u/(.+)', link.attrs['href'])
                if uid_match is not None:
                    uid = uid_match.group(1)
                else:
                    uid = re.search(r'weibo.cn/(.+)', link.attrs['href']).group(1)
                self.fans_id[uid] = name
        print(self.fans_id)
        return self.fans_id

    def scrape_info(self, id=None):
        if not self.is_login:
            raise LoginError
        if id is None:
            return None
        wait = WebDriverWait(self.driver, 5)
        self.driver.get('http://weibo.cn/u/%s' % id)
        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'tip2')))
        bs = BeautifulSoup(self.driver.page_source, 'lxml')

        # 获取用户id，微博数，关注数，粉丝数
        tip2 = bs.find('div', {'class': 'tip2'})
        tips = tip2.find_all('a')
        weibo_number = int(re.search(r'.*\[(\d+)\]', tip2.span.get_text()).group(1))
        follow_number = int(re.search(r'.*\[(\d+)\]', tips[0].get_text()).group(1))
        fans_number = int(re.search(r'.*\[(\d+)\]', tips[1].get_text()).group(1))

        # 进入详细资料页面
        self.driver.get('https://weibo.cn/%s/info' % id)
        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'tip')))
        bs = BeautifulSoup(self.driver.page_source, 'lxml')

        # 获取用户昵称，性别，地址，生日，简介
        detail = str(bs.find('div', text='基本信息').next_sibling)
        user_name = re.search(r'昵称:(.+?)<br/>', detail).group(1)
        sex = re.search(r'性别:(.+?)<br/>', detail).group(1)
        address = re.search(r'地区:(.+?)<br/>', detail).group(1)
        birthday = re.search(r'生日:(.+?)<br/>', detail).group(1)
        synopsis = re.search(r'简介:(.+?)<br/>', detail).group(1)

        item = WeiboUserItem()
        item.id = id
        item.name = user_name
        item.sex = sex
        item.address = address
        item.birthday = birthday
        item.synopsis = synopsis
        item.weibo_number = weibo_number
        item.follow_number = follow_number
        item.fans_number = fans_number
        print(item)
        return item

    def scrape_weibo(self, id=None, number=10):
        if not self.is_login:
            raise LoginError
        if id is None or number is None or number <= 0:
            return []
        weibo_list = []
        wait = WebDriverWait(self.driver, 5)
        self.driver.get('https://weibo.cn/u/%s' % id)
        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'pms')))
        bs = BeautifulSoup(self.driver.page_source, 'lxml')

        tip2 = bs.find('div', {'class': 'tip2'})
        weibo_number = int(re.search(r'.*\[(\d+)\]', tip2.span.get_text()).group(1))
        page_number = int(bs.find(id='pagelist').form.div.input.attrs['value'])
        scrape_number = number if number < weibo_number else weibo_number

        finish_number = 0
        page_index = 1
        while finish_number < scrape_number and page_index <= page_number:
            weibo_divs = bs.find_all('div', {'class': 'c'})[1:-2]
            for weibo_div in weibo_divs:
                divs = weibo_div.find_all('div')
                if len(divs) == 1:      # 原创微博，无图
                    content_span = divs[0].find('span', {'class': 'ctt'})
                    time_span = divs[0].find('span', {'class': 'ct'})
                    item = WeiboContentItem()
                    item.owner = id
                    item.time = time_span.get_text()
                    item.content = re.search(r'<span class=\'ctt\'>(.*)</span>', str(content_span)).group(1)
                    print(item)
                    weibo_list.append(item)
                elif len(divs) == 2:
                    if len(divs[0].find_all('span')) == 1:      # 原创微博，有图
                        content_span = divs[0].find('span', {'class': 'ctt'})
                        image_all_a = divs[0].find('a', {'href': re.compile('http://weibo.cn/mblog/picAll/.+')})
                        time_span = divs[1].find('span', {'class': 'ct'})
                        item = WeiboContentItem()
                        item.owner = id
                        item.time = time_span.get_text()
                        item.content = re.search(r'<span class=\'ctt\'>(.*)</span>', str(content_span)).group(1)
                        if image_all_a is None:     # 含有一张图片
                            image_img = divs[1].a.img
                            item.images.append(image_img.attrs['src'])
                        else:       # 含有多张图片
                            self.driver.get(image_all_a.attrs['href'])
                            wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'c')))
                            bs1 = BeautifulSoup(self.driver.page_source, 'lxml')
                            image_divs = bs1.find_all('div')[1:-1]
                            for image_div in image_divs:
                                image_img = image_div.a.img
                                item.images.append(image_img.attrs['src'])
                        print(item)
                        weibo_list.append(item)
                    else:       # 转发微博，无图
                        repost_source_span = divs[0].find('span', {'class': 'cmt'})
                        content_span = divs[0].find('span', {'class': 'ctt'})
                        repost_reason_div = divs[1]
                        time_span = divs[1].find('span', {'class': 'ct'})
                        item = WeiboRepostContentItem()
                        item.content = re.search(r'<span class=\'ctt\'>(.*)</span>', str(content_span)).group(1)
                        item.owner = id
                        item.time = time_span.get_text()
                        item.repost_source = re.search(r'转发了(.*)的微博', str(repost_source_span)).group(1)
                        item.repost_reason = re.search(r'转发理由:</span>(.*)<a href=\'http://weibo.cn/attitude/',
                                                          str(repost_reason_div)).group(1)
                        print(item)
                        weibo_list.append(item)
                else:       # 转发微博，有图
                    repost_source_span = divs[0].find('span', {'class': 'cmt'})
                    content_span = divs[0].find('span', {'class': 'ctt'})
                    image_all_a = divs[0].find('a', {'href': re.compile('http://weibo.cn/mblog/picAll/.+')})
                    repost_reason_div = divs[2]
                    time_span = divs[2].find('span', {'class': 'ct'})
                    item = WeiboRepostContentItem()
                    item.content = re.search(r'<span class=\'ctt\'>(.*)</span>', str(content_span)).group(1)
                    item.owner = id
                    item.time = time_span.get_text()
                    item.repost_source = re.search(r'转发了(.*)的微博', str(repost_source_span)).group(1)
                    item.repost_reason = re.search(r'转发理由:</span>(.*)<a href=\'http://weibo.cn/attitude/',
                                                      str(repost_reason_div)).group(1)
                    if image_all_a is None:     # 含有一张图片
                        image_img = divs[1].a.img
                        item.images.append(image_img.attrs['src'])
                    else:   # 含有多张图片
                        self.driver.get(image_all_a.attrs['href'])
                        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'c')))
                        bs1 = BeautifulSoup(self.driver.page_source, 'lxml')
                        image_divs = bs1.find_all('div')[1:-1]
                        for image_div in image_divs:
                            image_img = image_div.a.img
                            item.images.append(image_img.attrs['src'])
                    print(item)
                    weibo_list.append(item)

                finish_number += 1
                if finish_number >= scrape_number:
                    break
            if finish_number < scrape_number and page_index < page_number:
                page_index += 1
                self.driver.get('https://weibo.cn/u/%s?page=%d' % (id, page_index))
                wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'pms')))
                bs = BeautifulSoup(self.driver.page_source, 'lxml')
        return weibo_list

    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    spider = WeiboSpider('******', '******')
    try:
        spider.login()
        spider.scrape_self_info()
        spider.scrape_follow_id()
        spider.scrape_fans_id()
        spider.scrape_follow_id('5884913735')
        spider.scrape_fans_id('5884913735')
        spider.scrape_info('5782276689')
        spider.scrape_weibo('5782276689', 10)
    except Exception:
        traceback.print_exc()
    finally:
        spider.quit()
