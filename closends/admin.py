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


class QQContentInline(admin.StackedInline):
    model = QQContent


class WeiboContentInline(admin.StackedInline):
    model = WeiboContent


class ZhihuContentInline(admin.StackedInline):
    model = ZhihuContent


class MyUserAdmin(UserAdmin):
    listdisplay = ('username', 'email', 'isstaff')
    inlines = (UserInfoInline,)


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    inlines = (WebsiteInline, FriendInline)


class WebsiteAdmin(admin.ModelAdmin):
    listdisplay = ('username', 'site', 'authcode')


class FriendAdmin(admin.ModelAdmin):
    listdisplay = ('username', 'nickname', 'group')
    inlines = (QQContentInline, WeiboContentInline, ZhihuContentInline,)


class QQContentAdmin(admin.ModelAdmin):
    listdisplay = ('nickname', 'content', 'publishdate')
    inlines = (ImageInline,)


class WeiboContentAdmin(admin.ModelAdmin):
    listdisplay = ('nickname', 'content', 'publishdate')
    inlines = (ImageInline,)


class ZhihuContentAdmin(admin.ModelAdmin):
    listdisplay = ('nickname', 'content', 'publishdate')
    inlines = (ImageInline,)


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(QQContent, QQContentAdmin)
admin.site.register(WeiboContent, WeiboContentAdmin)
admin.site.register(ZhihuContent, ZhihuContentAdmin)
admin.site.register(Image, ImageAdmin)
