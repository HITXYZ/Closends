# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class UserItem(Item):
    username = Field()
    sex = Field()
    location = Field()
    following_num = Field()
    follower_num = Field()
    weibo_num = Field()