# -*- coding:utf-8 -*-
"""
    @author: Jiale Xu
    @date: 2017/10/05
    @desc: crawler of sina weibo
"""
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup


class WeiboItem:
    def __init__(self, user_id=None, user_name=None, sex=None, address=None, birthday=None, synopsis=None,
                 weibo_number=None, following_number=None, follower_number=None):
        self.user_id = user_id
        self.user_name = user_name
        self.sex = sex
        self.address = address
        self.birthday = birthday
        self.synopsis = synopsis
        self.weibo_number = weibo_number
        self.following_number = following_number
        self.follower_number = follower_number


class WeiboSpider:
    def __init__(self, account, password):
        self.account = account
        self.password = password
        self.driver = webdriver.PhantomJS("../phantomjs")
        self.user_agent = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        ]

    def login(self):
        self.driver.maximize_window()
        self.driver.get("https://weibo.cn/pub/")

        # Wap版微博登录入口
        login_entrance = self.driver.find_element_by_link_text("登录")
        login_entrance.click()

        # 等待登录页面元素出现
        wait1 = WebDriverWait(self.driver, 5)
        wait1.until(ec.visibility_of_element_located((By.ID, "loginName")))

        # 定位登录元素
        act_field = self.driver.find_element_by_id("loginName")
        pwd_field = self.driver.find_element_by_id("loginPassword")
        submit = self.driver.find_element_by_id("loginAction")

        # 清除用户名与密码输入框内容
        act_field.clear()
        pwd_field.clear()

        # 登录
        act_field.send_keys(self.account)
        pwd_field.send_keys(self.password)
        submit.click()

        wait2 = WebDriverWait(self.driver, 5)
        wait2.until(ec.visibility_of_element_located((By.CLASS_NAME, "tip2")))

    def crawl_self(self):
        bs = BeautifulSoup(self.driver.page_source, "lxml")

        # 获取用户id，微博数，关注数，粉丝数
        tips = bs.find("div", {"class": "tip2"}).findAll("a")
        user_id = re.search(r"/(\d+)/profile", tips[0].attrs["href"]).group(1)
        weibo_number = re.search(r".*\[(\d+)\]", tips[0].get_text()).group(1)
        following_number = re.search(r".*\[(\d+)\]", tips[1].get_text()).group(1)
        follower_number = re.search(r".*\[(\d+)\]", tips[2].get_text()).group(1)
        print user_id, weibo_number, following_number, follower_number

        # 进入详细资料页面
        information_link = self.driver.find_element_by_link_text("详细资料")
        information_link.click()
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

        item = WeiboItem()
        item.user_id = user_id
        item.user_name = user_name
        item.sex = sex
        item.address = address
        item.birthday = birthday
        item.synopsis = synopsis
        item.weibo_number = weibo_number
        item.following_number = following_number
        item.follower_number = follower_number
        return item


if __name__ == "__main__":
    spider = WeiboSpider("15544404545", "XJL970928wb")
    spider.login()
    spider.crawl_self()
