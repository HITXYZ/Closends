from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Website, Friend, Identifier, Content, Image

class WebsiteInline(admin.StackedInline):
    model = Website

class FriendInline(admin.StackedInline):
    model = Friend

class IdentifierInline(admin.StackedInline):
    model = Identifier

class ContentInline(admin.StackedInline):
    model = Content

class ImageInline(admin.StackedInline):
    model = Image

class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('type', 'authcode', 'username')

class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff')
    inlines = (WebsiteInline, FriendInline)

class FriendAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'username')
    inlines = (IdentifierInline, )

class IdentifierAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'website', 'friend_name')
    inlines = (ContentInline, )

class ContentAdmin(admin.ModelAdmin):
    list_display = ("content", 'publish_date', 'identifier')
    inlines = (ImageInline, )

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(Identifier, IdentifierAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Image)
