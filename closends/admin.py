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
    listdisplay = ('username', 'email', 'isstaff')
    inlines = (UserInfoInline,)


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    inlines = (WebsiteInline, FriendInline)


class WebsiteAdmin(admin.ModelAdmin):
    listdisplay = ('username', 'site', 'authcode')


class FriendAdmin(admin.ModelAdmin):
    listdisplay = ('username', 'nickname', 'group')
    inlines = (TiebaContentInline, WeiboContentInline, ZhihuContentInline,)


class WeiboContentAdmin(admin.ModelAdmin):
    listdisplay = ('nickname', 'content', 'pub_date')
    inlines = (ImageInline,)


class ZhihuContentAdmin(admin.ModelAdmin):
    listdisplay = ('nickname', 'content', 'pub_date')
    inlines = (ImageInline,)


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
