# -*- coding:utf-8 -*-
"""
    @author: Jiale Xu
    @date: 2017/10/05
    @desc: crawler of sina weibo
"""

from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy import Request
from SocialMediaCrawler.items import WeiboUserItem


class WeiboSpider(CrawlSpider):
    name = "weibo"
    start_ids = ["5866439255"]

    def start_requests(self):
        for wid in self.start_ids:
            url = "https://weibo.com/u/%s?is_all=1" % wid
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = Selector(response)
        user_item = WeiboUserItem()
        user_item["username"] = \
            selector.xpath('//h1[contains(concat(" ", normalize-space(@class), " "), " username ")]/text()').extract()
        user_item["location"] = \
            selector.xpath('//span[contains(concat(" ", normalize-space(@class), " "), " item_text W_f1 ")]/text()').extract()
        nums = selector.xpath('//strong[contains(concat(" ", normalize-space(@class), " "), " W_f18 ")]/text()').extract()
        user_item["following_num"] = int(nums[0])
        user_item["follower_num"] = int(nums[1])
        user_item["weibo_num"] = int(nums[2])
        print user_item
