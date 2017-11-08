"""
    @author: Jiale Xu
    @date: 2017/10/23
    @desc: Items of weibo scraping
"""
from base_item import SocialMediaItem


class WeiboItem(SocialMediaItem):
    pass


class WeiboUserItem(WeiboItem):
    def __init__(self):
        self.id = None
        self.name = None
        self.gender = None
        self.avatar_url = None
        self.location = None
        self.description = None
        self.signup_time = None
        self.weibo_count = 0
        self.follow_count = 0
        self.fans_count = 0

    def __str__(self):
        string = ''
        string += 'ID: ' + str(self.id) + '\n'
        string += 'Name: ' + str(self.name) + '\n'
        string += 'Gender: ' + str(self.gender) + '\n'
        string += 'Avatar Url: ' + str(self.avatar_url) + '\n'
        string += 'Location: ' + str(self.location) + '\n'
        string += 'Description: ' + str(self.description) + '\n'
        string += 'Sign-up Time: ' + str(self.signup_time) + '\n'
        string += 'Weibo Count: ' + str(self.weibo_count) + '\n'
        string += 'Following Count: ' + str(self.follow_count) + '\n'
        string += 'Fans Count: ' + str(self.fans_count) + '\n'
        return string

    def __hash__(self):
        return hash(self.id)


class WeiboContentItem(WeiboItem):
    def __init__(self):
        self.id = None
        self.owner = 0
        self.time = None
        self.content = None
        self.source = None
        self.pictures = []

    def __str__(self):
        string = ''
        string += 'ID: ' + str(self.id) + '\n'
        string += 'Owner: ' + str(self.owner) + '\n'
        string += 'Time: ' + str(self.time) + '\n'
        string += 'Content: ' + str(self.content) + '\n'
        string += 'Source: ' + str(self.source) + '\n'
        string += 'Pictures: ' + '; '.join(str(pic) for pic in self.pictures) + '\n'
        return string

    def __hash__(self):
        return hash(self.id)


class WeiboRepostContentItem(WeiboContentItem):
    def __init__(self):
        WeiboContentItem.__init__(self)
        self.source_id = None
        self.source_owner = 0
        self.source_time = None
        self.source_content = None
        self.source_pictures = []

    def __str__(self):
        string = WeiboContentItem.__str__(self)
        string += 'Source ID: ' + str(self.source_id) + '\n'
        string += 'Source Owner: ' + str(self.source_owner) + '\n'
        string += 'Source Time: ' + str(self.source_time) + '\n'
        string += 'Source Content: ' + str(self.source_content) + '\n'
        string += 'Source Pictures: ' + '; '.join([str(pic) for pic in self.source_pictures])
        return string

    def __hash__(self):
        return hash(self.id)
