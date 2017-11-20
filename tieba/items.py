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
        self.tieba_age = 0
        self.follow_count = 0
        self.fans_count = 0
        self.forum_count = 0
        self.post_count = 0
        self.comment_count = 0
        self.posts = []
        self.comments = []

    def __str__(self):
        string = ''
        string += 'Name: ' + str(self.name) + '\n'
        string += 'Tieba Age: ' + str(self.tieba_age) + '\n'
        string += 'Follow Count: ' + str(self.follow_count) + '\n'
        string += 'Fans Count: ' + str(self.fans_count) + '\n'
        string += 'Forum Count: ' + str(self.forum_count) + '\n'
        string += 'Post Count: ' + str(self.post_count) + '\n'
        string += 'Comment Count: ' + str(self.comment_count) + '\n'
        string += 'Posts: ' + '; '.join(str(post) for post in self.posts)
        string += 'Comments: ' + '; '.join(str(comment) for comment in self.comments)
        return string

    def __hash__(self):
        return hash(self.name)
