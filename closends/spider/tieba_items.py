"""
@author: Jiale Xu
@date: 2017/11/20
@desc: Items for tieba scraping.
"""

from time import strftime, localtime
from closends.spider.base_item import SocialMediaItem


class TiebaItem(SocialMediaItem):
    pass


class TiebaUserItem(TiebaItem):
    def __init__(self):
        self.name = ''  # 百度ID
        self.sex = ''  # 性别
        self.tieba_age = 0  # 吧龄
        self.avatar_url = ''  # 头像链接
        self.follow_count = 0  # 关注数
        self.fans_count = 0  # 粉丝数
        self.forum_count = 0  # 关注的吧数
        self.post_count = 0  # 发帖数

    def __str__(self):
        string = ''
        string += 'Name: ' + str(self.name) + '\n'
        string += 'Sex: ' + str(self.sex) + '\n'
        string += 'Tieba Age: ' + str(self.tieba_age) + '\n'
        string += 'Avatar Url: ' + str(self.avatar_url) + '\n'
        string += 'Follow Count: ' + str(self.follow_count) + '\n'
        string += 'Fans Count: ' + str(self.fans_count) + '\n'
        string += 'Forum Count: ' + str(self.forum_count) + '\n'
        string += 'Post Count: ' + str(self.post_count) + '\n'
        return string

    def __hash__(self):
        return hash(self.name)


class TiebaPostItem(TiebaItem):
    def __init__(self):
        self.time = 0  # 发帖时间
        self.title = ''  # 帖子标题
        self.title_url = ''  # 帖子链接
        self.content = ''  # 帖子内容
        self.content_url = ''  # 内容链接
        self.forum = ''  # 贴吧名
        self.forum_url = ''  # 贴吧链接

    def __str__(self):
        string = ''
        string += 'Time: ' + strftime("%Y-%m-%d %H:%M:%S", localtime(self.time)) + '\n'
        string += 'Title: ' + str(self.title) + '\n'
        string += 'Title Url: ' + str(self.title_url) + '\n'
        string += 'Content: ' + str(self.content) + '\n'
        string += 'Content Url: ' + str(self.content_url) + '\n'
        string += 'Forum: ' + str(self.forum) + '\n'
        string += 'Forum Url: ' + str(self.forum_url) + '\n'
        return string

    def convert_format(self):
        tieba = {}
        tieba['pub_date'] = strftime("%Y-%m-%d %H:%M:%S", localtime(self.time))
        tieba['forum'] = str(self.forum)
        tieba['forum_url'] = str(self.forum_url)
        tieba['title'] = str(self.title)
        tieba['title_url'] = str(self.title_url)
        tieba['content'] = str(self.content)
        tieba['content_url'] = str(self.content_url)
        return tieba

    def __hash__(self):
        return hash(self.title)
