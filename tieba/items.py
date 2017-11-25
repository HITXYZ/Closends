"""
@author: Jiale Xu
@date: 2017/11/20
@desc: Items for tieba scraping
"""
from base_item import SocialMediaItem


class TiebaItem(SocialMediaItem):
    pass


class TiebaUserItem(TiebaItem):
    def __init__(self):
        self.name = ''
        self.sex = ''
        self.tieba_age = 0
        self.avatar_url = ''
        self.follow_count = 0
        self.fans_count = 0
        self.forum_count = 0
        self.post_count = 0

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
        self.time = 0
        self.title = ''
        self.title_url = ''
        self.content = ''
        self.content_url = ''
        self.forum = ''
        self.forum_url = ''

    def __str__(self):
        string = ''
        string += 'Time: ' + str(self.time) + '\n'
        string += 'Title: ' + str(self.title) + '\n'
        string += 'Title Url: ' + str(self.title_url) + '\n'
        string += 'Content: ' + str(self.content) + '\n'
        string += 'Content Url: ' + str(self.content_url) + '\n'
        string += 'Forum: ' + str(self.forum) + '\n'
        string += 'Forum Url: ' + str(self.forum_url) + '\n'
        return string

    def __hash__(self):
        return hash(self.title)
