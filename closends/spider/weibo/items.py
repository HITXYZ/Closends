"""
    @author: Jiale Xu
    @date: 2017/10/23
    @desc: Items of weibo scraping
"""
from base_item import SocialMediaItem


# 微博条目基类
class WeiboItem(SocialMediaItem):
    pass


# 微博用户信息条目类
class WeiboUserItem(WeiboItem):
    def __init__(self):
        self.id = None              # 用户ID
        self.name = None            # 用户名
        self.gender = None          # 性别
        self.avatar_url = None      # 头像链接
        self.location = None        # 所在地
        self.description = None     # 个人简介
        self.signup_time = None     # 注册时间
        self.weibo_count = 0        # 微博数
        self.follow_count = 0       # 关注数
        self.fans_count = 0         # 粉丝数

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


# 微博内容条目类
class WeiboContentItem(WeiboItem):
    def __init__(self):
        self.id = None          # 微博ID
        self.owner = 0          # 博主
        self.time = None        # 时间
        self.content = None     # 内容
        self.source = None      # 来源
        self.pictures = []      # 图片列表

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


# 微博转发内容条目类
class WeiboRepostContentItem(WeiboContentItem):
    def __init__(self):
        WeiboContentItem.__init__(self)
        self.source_id = None           # 原博ID
        self.source_owner = 0           # 原博主
        self.source_time = None         # 原博时间
        self.source_content = None      # 原博内容
        self.source_pictures = []       # 原博图片列表

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
