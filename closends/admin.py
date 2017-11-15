from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class UserInfoInline(admin.StackedInline):
    model = UserInfo


class WebsiteInline(admin.StackedInline):
    model = Website


class FriendInline(admin.StackedInline):
    model = Friend


class ImageInline(admin.StackedInline):
    model = Image


class TiebaContentInline(admin.StackedInline):
    model = TiebaContent


class WeiboContentInline(admin.StackedInline):
    model = WeiboContent


class ZhihuContentInline(admin.StackedInline):
    model = ZhihuContent


class MyUserAdmin(UserAdmin):
    # list_display = ('username', 'email', 'is_staff')
    inlines = (UserInfoInline,)


class UserInfoAdmin(admin.ModelAdmin):
    # list_display = ('__str__',)
    inlines = (WebsiteInline, FriendInline)


class WebsiteAdmin(admin.ModelAdmin):
    pass
    # list_display = ('username', 'site', 'authcode')


class FriendAdmin(admin.ModelAdmin):
    # list_display = ('username', 'nickname', 'group')
    inlines = (TiebaContentInline, WeiboContentInline, ZhihuContentInline,)


class WeiboContentAdmin(admin.ModelAdmin):
    list_display = ('friend_nickname', 'pub_date', 'content_section', 'is_repost')
    list_filter = ['is_repost']

class ZhihuContentAdmin(admin.ModelAdmin):
    pass
    # list_display = ('nickname', 'content', 'pub_date')


class TiebaContentAdmin(admin.ModelAdmin):
    pass


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(WeiboContent, WeiboContentAdmin)
admin.site.register(ZhihuContent, ZhihuContentAdmin)
admin.site.register(TiebaContent, TiebaContentAdmin)
admin.site.register(Image, ImageAdmin)
