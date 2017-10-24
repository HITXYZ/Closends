# -*- coding:utf-8 -*-
"""
    @author: Jiale Xu
    @date: 2017/10/05
    @desc: scraper of sina weibo
"""
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
from exception import LoginError
from items import WeiboUserItem


class WeiboSpider:
    def __init__(self, account, password):
        self.id = None
        self.account = account
        self.password = password
        self.driver = webdriver.PhantomJS("../phantomjs")
        self.user_agent = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        ]
        self.follow_id = []
        self.fans_id = []
        self.is_login = False

    def login(self):
        self.driver.maximize_window()
        self.driver.get("https://weibo.cn/pub/")
        wait = WebDriverWait(self.driver, 5)

        # Wap版微博登录入口
        login_entrance = self.driver.find_element_by_link_text("登录")
        login_entrance.click()
        wait.until(ec.visibility_of_element_located((By.ID, "loginName")))

        # 定位登录元素
        act_field = self.driver.find_element_by_id("loginName")
        pwd_field = self.driver.find_element_by_id("loginPassword")
        submit = self.driver.find_element_by_id("loginAction")
        act_field.clear()
        pwd_field.clear()

        # 登录
        act_field.send_keys(self.account)
        pwd_field.send_keys(self.password)
        submit.click()

        # 获取登录用户id
        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "tip2")))
        bs = BeautifulSoup(self.driver.page_source, "lxml")
        tip = bs.find("div", {"class": "tip2"}).a
        self.id = re.search(r"/(\d+)/profile", tip.attrs["href"]).group(1)
        self.is_login = True

    def scrape_self(self):
        if not self.is_login:
            raise LoginError()
        self.driver.get("http://weibo.cn/")
        bs = BeautifulSoup(self.driver.page_source, "lxml")

        # 获取用户id，微博数，关注数，粉丝数
        tips = bs.find("div", {"class": "tip2"}).findAll("a")
        weibo_number = re.search(r".*\[(\d+)\]", tips[0].get_text()).group(1)
        follow_number = re.search(r".*\[(\d+)\]", tips[1].get_text()).group(1)
        fans_number = re.search(r".*\[(\d+)\]", tips[2].get_text()).group(1)
        print weibo_number, follow_number, fans_number

        # 进入详细资料页面
        self.driver.get("https://weibo.cn/%s/info" % self.id)
        wait1 = WebDriverWait(self.driver, 5)
        wait1.until(ec.visibility_of_element_located((By.CLASS_NAME, "tip")))

        # 获取用户昵称，性别，地址，生日，简介
        bs = BeautifulSoup(self.driver.page_source, "lxml")
        detail = str(bs.find("div", text="基本信息").next_sibling)
        user_name = re.search(r"昵称</a>:(.+?)<br/>", detail).group(1)
        sex = re.search(r"性别</a>:(.+?)<br/>", detail).group(1)
        address = re.search(r"地区</a>:(.+?)<br/>", detail).group(1)
        birthday = re.search(r"生日</a>:(.+?)<br/>", detail).group(1)
        synopsis = re.search(r"简介</a>:(.+?)<br/>", detail).group(1)
        print user_name, sex, address, birthday, synopsis

        item = WeiboUserItem()
        item["user_id"] = self.id
        item["user_name"] = user_name
        item["sex"] = sex
        item["address"] = address
        item["birthday"] = birthday
        item["synopsis"] = synopsis
        item["weibo_number"] = weibo_number
        item["follow_number"] = follow_number
        item["fans_number"] = fans_number
        print item
        return item

    def scrape_follows(self):
        if not self.is_login:
            raise LoginError()
        self.driver.get("https://weibo.cn/%s/follow" % self.id)


if __name__ == "__main__":
    spider = WeiboSpider("15544404545", "XJL970928wb")
    spider.login()
    spider.scrape_self()
