"""
    @author: Jiale Xu
    @date: 2017/10/23
    @desc: Items of weibo scraping
"""

from time import strftime, localtime
from closends.spider.base_item import SocialMediaItem


# 微博条目基类
class WeiboItem(SocialMediaItem):
    pass


# 微博博主信息条目类
class WeiboPosterItem(WeiboItem):
    def __init__(self):
        self.id = 0                 # 用户ID
        self.name = None            # 用户名
        self.avatar_url = None      # 头像链接
        self.profile_url = None     # 主页链接

    def __str__(self):
        string = ''
        string += 'ID: ' + str(self.id) + '\n'
        string += 'Name: ' + str(self.name) + '\n'
        string += 'Avatar Url' + str(self.avatar_url) + '\n'
        string += 'Profile Url' + str(self.profile_url) + '\n'
        return string

    def __hash__(self):
        return hash(self.id)


# 微博用户信息条目类
class WeiboUserItem(WeiboPosterItem):
    def __init__(self):
        WeiboPosterItem.__init__(self)
        self.gender = None          # 性别
        self.location = None        # 所在地
        self.description = None     # 个人简介
        self.signup_time = None     # 注册时间
        self.weibo_count = 0        # 微博数
        self.follow_count = 0       # 关注数
        self.fans_count = 0         # 粉丝数

    def __str__(self):
        string = WeiboPosterItem.__str__(self)
        string += 'Gender: ' + str(self.gender) + '\n'
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
        self.id = 0                     # 微博ID
        self.url = ''                   # 微博链接
        self.owner = WeiboPosterItem()  # 博主
        self.time = 0                   # 时间
        self.content = ''               # 内容
        self.source = ''                # 来源
        self.pictures = []              # 图片列表
        self.media_pic = ''             # 媒体封面截图
        self.media_url = ''             # 媒体内容链接


    def __str__(self):
        string = ''
        string += 'ID: ' + str(self.id) + '\n'
        string += 'Url: ' + str(self.url) + '\n'
        string += 'Owner: ' + str(self.owner.name) + '\n'
        string += 'Time: ' + strftime("%Y-%m-%d %H:%M:%S", localtime(self.time)) + '\n'
        string += 'Content: ' + str(self.content) + '\n'
        string += 'Source: ' + str(self.source) + '\n'
        string += 'Pictures: ' + '; '.join(str(pic) for pic in self.pictures) + '\n'
        string += 'Media Pic: ' + str(self.media_pic) + '\n'
        string += 'Media Url: ' + str(self.media_url) + '\n'
        return string

    def __hash__(self):
        return hash(self.id)

    def convert_format(self):
        weibo = {}
        weibo['pub_date'] = strftime("%Y-%m-%d %H:%M:%S", localtime(self.time))
        weibo['src_url'] = str(self.url)
        weibo['content'] = str(self.content)

        weibo['is_repost'] = False
        weibo['images'] = self.pictures
        weibo['video_image'] = str(self.media_pic)
        return weibo


# 微博转发内容条目类
class WeiboRepostContentItem(WeiboContentItem):
    def __init__(self):
        WeiboContentItem.__init__(self)
        self.source_id = None                   # 原博ID
        self.source_url = None                  # 原博链接
        self.source_owner = WeiboPosterItem()   # 原博主
        self.repost_reason = None               # 转发理由

    def __str__(self):
        string = WeiboContentItem.__str__(self)
        string += 'Source ID: ' + str(self.source_id) + '\n'
        string += 'Source Url: ' + str(self.source_url) + '\n'
        string += 'Source Owner: ' + str(self.source_owner.name) + '\n'
        string += 'Repost Reason: ' + str(self.repost_reason) + '\n'
        return string

    def __hash__(self):
        return hash(self.id)

    def convert_format(self):
        basic = WeiboContentItem.convert_format(self)

        weibo = {}
        weibo['pub_date'] = basic['pub_date']
        weibo['src_url'] = basic['src_url']
        weibo['content'] = str(self.repost_reason)

        weibo['is_repost'] = True
        weibo['images'] = []
        weibo['video_image'] = ""

        weibo['origin_account'] = str(self.source_owner.name)
        weibo['origin_link'] = str(self.source_owner.avatar_url)

        weibo['origin_pub_date'] = ""
        weibo['origin_src_url'] = str(self.source_url)
        weibo['origin_content'] = basic['content']
        weibo['origin_images'] = basic['images']
        weibo['origin_video_image'] = basic['video_image']
        return weibo