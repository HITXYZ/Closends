from django.db import models
from django.contrib.auth.models import User

marks = {'1': 'QQ', '2': '微信', '3': '微博'}

class Website(models.Model):
    """用户各网站授权码"""
    def __str__(self):
        return marks[self.type]

    def username(self):
        return self.user.username

    choice_in_type = (('1', 'QQ'), ('2', '微信'), ('3', '微博'))
    type = models.CharField(max_length=1, default='1', choices=choice_in_type)
    authcode = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Friend(models.Model):
    """用户好友"""
    def __str__(self):
        return self.name

    def username(self):
        return self.user.username

    group_choices = (('1', '未分组'), ('2', '家人'), ('3', '好友'))
    name = models.CharField(max_length=30)
    group = models.CharField(max_length=2, default='1', choices=group_choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Identifier(models.Model):
    """用户好友各网站标识"""
    def __str__(self):
        return marks[self.website] + '_' + self.identifier

    def friend_name(self):
        return self.friend.name

    choice_in_type = (('1', 'QQ'), ('2', '微信'), ('3', '微博'))
    website = models.CharField(max_length=1, default='1', choices=choice_in_type)
    identifier = models.CharField(max_length=30)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)

class Content(models.Model):
    """所有网站动态内容"""
    def __str__(self):
        return self.content[:20]

    content = models.TextField(max_length=200)
    video_url = models.URLField(max_length=50, default="http://")
    publish_date = models.DateField('date published')
    identifier = models.ForeignKey(Identifier, on_delete=models.CASCADE)

class Image(models.Model):
    """所有动态的图片及链接"""
    def __str__(self):
        return self.image_url

    image = models.ImageField()
    image_url = models.URLField(max_length=50, default="http://")
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
