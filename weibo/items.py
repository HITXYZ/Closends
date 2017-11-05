"""
    @author: Jiale Xu
    @date: 2017/10/23
    @desc: Items of weibo scraping
"""
from items import ScrapeItem


class WeiboItem(ScrapeItem):
    pass


class WeiboUserItem(WeiboItem):
    def __init__(self):
        self.id = None
        self.name = None
        self.sex = None
        self.address = None
        self.birthday = None
        self.synopsis = None
        self.weibo_number = 0
        self.follow_number = 0
        self.fans_number = 0

    def __str__(self):
        string = ''
        string += 'ID: ' + str(self.id) + '\n'
        string += 'Name: ' + str(self.name) + '\n'
        string += 'Sex: ' + str(self.sex) + '\n'
        string += 'Address: ' + str(self.address) + '\n'
        string += 'Birthday: ' + str(self.birthday) + '\n'
        string += 'Synopsis: ' + str(self.synopsis) + '\n'
        string += 'Weibo Number: ' + str(self.weibo_number) + '\n'
        string += 'Follow Number: ' + str(self.follow_number) + '\n'
        string += 'Fans Number: ' + str(self.follow_number) + '\n'
        return string

    def __hash__(self):
        return hash(self.id)


class WeiboContentItem(WeiboItem):
    def __init__(self):
        self.owner = None
        self.time = None
        self.content = None
        self.images = []

    def __str__(self):
        string = ''
        string += 'Owner: ' + str(self.owner) + '\n'
        string += 'Time: ' + str(self.time) + '\n'
        string += 'Content: ' + str(self.content) + '\n'
        return string

    def __hash__(self):
        return hash(self.content)


class WeiboRepostContentItem(WeiboContentItem):
    def __init__(self):
        WeiboContentItem.__init__(self)
        self.repost_source = None
        self.repost_reason = None

    def __str__(self):
        string = WeiboContentItem.__str__(self)
        string += 'Repost Source: ' + str(self.repost_source) + '\n'
        string += 'Repost Reason: ' + str(self.repost_reason) + '\n'
        return string

    def __hash__(self):
        return hash(str(self.content) + str(self.repost_reason))
