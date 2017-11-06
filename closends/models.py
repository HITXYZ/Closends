import os
from django.db import models
from django.contrib.auth.models import User

marks = {'QQ': 'QQ', '微博': '微博', '知乎': '知乎'}
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class UserInfo(models.Model):
    def __str__(self):
        return self.user.username

    user = models.OneToOneField(User)
    head_img = models.ImageField(blank=True, upload_to=BASE_DIR+'/media/head')


class Website(models.Model):
    """用户各网站授权码"""

    def __str__(self):
        return marks[self.site]

    def username(self):
        return self.user.user.username

    site_choices = (('QQ', 'QQ'), ('微博', '微博'), ('知乎', '知乎'))
    site = models.CharField(max_length=2, default='QQ', choices=site_choices)
    authcode = models.CharField(max_length=20)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)


class Friend(models.Model):
    """用户好友"""

    def __str__(self):
        return self.nickname

    def username(self):
        return self.user.user.username

    group_choices = (('未分组', '未分组'), ('家人', '家人'), ('好友', '好友'), ('同学', '同学'))
    nickname = models.CharField(max_length=30)
    group = models.CharField(max_length=3, default='未分组', choices=group_choices)
    qq_mark = models.CharField(max_length=11)
    weibo_mark = models.CharField(max_length=20)
    zhihu_mark = models.CharField(max_length=20)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)


class QQContent(models.Model):
    """QQ动态"""

    def __str__(self):
        return self.content[:20]

    def nickname(self):
        return self.friend.nickname

    content = models.TextField()
    video_url = models.URLField(default="http://")
    publish_date = models.DateField('date published')
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)


class WeiboContent(models.Model):
    """微博动态"""

    def __str__(self):
        return self.content[:20]

    def nickname(self):
        return self.friend.nickname

    content = models.TextField()
    video_url = models.URLField(default="http://")
    publish_date = models.DateField('date published')
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)


class ZhihuContent(models.Model):
    """微博动态"""

    def __str__(self):
        return self.content[:20]

    def nickname(self):
        return self.friend.nickname

    content = models.TextField()
    video_url = models.URLField(default="http://")
    publish_date = models.DateField('date published')
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)


class Image(models.Model):
    """所有动态的图片及链接"""

    def __str__(self):
        return self.image_url

    image = models.ImageField()
    image_url = models.URLField(max_length=50, default="http://")
    content_qq = models.ForeignKey(QQContent, on_delete=models.CASCADE)
    content_weibo = models.ForeignKey(WeiboContent, on_delete=models.CASCADE)
    content_zhihu = models.ForeignKey(ZhihuContent, on_delete=models.CASCADE)
