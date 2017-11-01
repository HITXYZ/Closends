"""
    @author: Jiale Xu
    @date: 2017/11/01
    @desc: Scraper for zhihu
"""
import datetime
import logging
import requests
from exceptions import SpiderInitError


headers = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Referer': 'http://www.zhihu.com/',
    'Host': 'www.zhihu.com',
    'rememberme': 'true'
}


class ZhihuSpider:
    def __init__(self, account=None, password=None):
        if account is None or password is None:
            raise SpiderInitError()
        self.account = account
        self.password = password

