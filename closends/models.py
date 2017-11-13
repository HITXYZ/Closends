import os
from django.db import models
from django.contrib.auth.models import User

marks = {'weibo': '微博', 'zhihu': '知乎', 'tieba': '贴吧'}
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class UserInfo(models.Model):
    def __str__(self):
        return self.user.username

    def image_name(self):
        if not self.head_img.name:
            return 'default_head.svg'
        return self.head_img.name.split('/')[-1]

    user = models.OneToOneField(User)
    head_img = models.ImageField(blank=True, upload_to=BASE_DIR + '/media/head')
    group_list = models.CharField(default='未分组', max_length=1024)


class Website(models.Model):
    """用户各网站授权码"""

    def __str__(self):
        return marks[self.site]

    def username(self):
        return self.user.user.username

    site_choices = (('weibo', '微博'), ('zhihu', '知乎'), ('tieba', '贴吧'))
    site = models.CharField(max_length=5, default='weibo', choices=site_choices)
    account = models.CharField(max_length=50)
    link = models.CharField(max_length=100)
    head = models.CharField(max_length=100)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)


class Friend(models.Model):
    """用户好友"""

    def __str__(self):
        return self.nickname

    def username(self):
        return self.user.user.username

    def image_name(self):
        if not self.head_img.name:
            return 'default_head.svg'
        return self.head_img.name.split('/')[-1]

    def weibo_is_blank(self):
        return not self.weibo_account

    def zhihu_is_blank(self):
        return not self.zhihu_account

    def tieba_is_blank(self):
        return not self.tieba_account

    group_choices = (('group_0', '未分组'), ('group_1', '家人'), ('group_2', '好友'), ('group_3', '同学'))
    nickname = models.CharField(max_length=30)
    head_img = models.ImageField(blank=True, upload_to=BASE_DIR + '/media/head')
    group = models.CharField(max_length=10, default='group_0', choices=group_choices)

    weibo_account = models.CharField(max_length=20, blank=True)
    weibo_link = models.CharField(max_length=100, blank=True)
    weibo_head = models.CharField(max_length=100, blank=True)

    zhihu_account = models.CharField(max_length=20, blank=True)
    zhihu_link = models.CharField(max_length=100, blank=True)
    zhihu_head = models.CharField(max_length=100, blank=True)
    zhihu_detail = models.CharField(max_length=200, blank=True)

    tieba_account = models.CharField(max_length=20, blank=True)
    tieba_link = models.CharField(max_length=100, blank=True)
    tieba_head = models.CharField(max_length=100, blank=True)

    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)


# class QQContent(models.Model):
#     """QQ动态"""
#
#     def __str__(self):
#         return self.content[:20]
#
#     def nickname(self):
#         return self.friend.nickname
#
#     content = models.TextField()
#     video_url = models.URLField(blank=True)
#     publish_date = models.DateField('date published')
#     friend = models.ForeignKey(Friend, on_delete=models.CASCADE)


class WeiboContent(models.Model):
    """微博动态"""

    def __str__(self):
        return self.content[:20]

    def nickname(self):
        return self.friend.nickname

    # basic post
    pub_date = models.DateField('date published')
    src_url = models.CharField(max_length=100)
    content = models.TextField()

    # check video/image or is reposted
    is_repost = models.BooleanField()
    has_image = models.BooleanField()
    video_image = models.CharField(max_length=100, blank=True)

    # original author
    origin_account = models.CharField(max_length=20, blank=True)
    origin_link = models.CharField(max_length=100, blank=True)

    # original post
    origin_pub_date = models.DateField('date_published')
    origin_src_url = models.CharField(max_length=100, blank=True)
    origin_content = models.TextField(blank=True)
    origin_has_image = models.BooleanField(blank=True)
    origin_video_image = models.CharField(max_length=100, blank=True)

    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)


class ZhihuContent(models.Model):
    """知乎动态"""

    def __str__(self):
        return self.content[:20]

    def nickname(self):
        return self.friend.nickname

    pub_date = models.DateField('date published')
    title = models.CharField(max_length=50)
    title_link = models.CharField(max_length=100)
    cover_image = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)


class TiebaContent(models.Model):
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)


class Image(models.Model):
    """所有动态的图片及链接"""

    def __str__(self):
        return self.image_url

    image_url = models.URLField(max_length=100, blank=True)
    content_weibo = models.ForeignKey(WeiboContent, on_delete=models.CASCADE)
    content_zhihu = models.ForeignKey(ZhihuContent, on_delete=models.CASCADE)
    content_tieba = models.ForeignKey(TiebaContent, on_delete=models.CASCADE)
