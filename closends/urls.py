from .views import *
from django.conf.urls import url, include

settingpatterns = [
    url(r'index$', user_info, name='setting_index'),
    url(r'user_info$', user_info, name='user_info'),
    url(r'user_binding$', user_binding, name='user_binding'),
    url(r'user_binding/qq_binding$', qq_binding, name='qq_binding'),
    url(r'user_binding/weibo_binding$', weibo_binding, name='weibo_binding'),
    url(r'user_binding/zhihu_binding$', zhihu_binding, name='zhihu_binding'),
    url(r'user_binging/qq_unbinding$', qq_unbinding, name='qq_unbinding'),
    url(r'user_binging/weibo_unbinding$', weibo_unbinding, name='weibo_unbinding'),
    url(r'user_binging/zhihu_unbinding$', zhihu_unbinding, name='zhihu_unbinding'),
    url(r'friend_manage$', friend_manage, name='friend_manage'),
    url(r'friend_manage/add_group$', add_group, name='add_group'),
    url(r'friend_manage/add_friend$', add_friend, name='add_friend'),
    url(r'friend_manage/add_qq_friend$', add_qq_friend, name='add_qq_friend'),
    url(r'friend_manage/get_group_friends/(?P<group>\w+)/(?P<page>[0-9]+)$', get_group_friends, name='get_group_friends'),
]


authcodepatterns = [
    url(r'github_code/(?P<code>\w+)/$', get_github_code, name='get_github_code'),
]

app_name = 'closends'
urlpatterns = [
    url(r'^$', to_login, name='to_login'),
    url(r'^to_register$', to_register, name='to_register'),
    url(r'^username_login$', username_login, name='username_lgoin'),
    url(r'^email_login$', email_login, name='email_lgoin'),
    url(r'^register$', register, name='register'),

    url(r'^index$', index, name='index'),
    url(r'^logout$', user_logout, name='logout'),
    url(r'^set/', include(settingpatterns, namespace='setting')),
    url(r'^authcode/', include(authcodepatterns, namespace='authcode')),
]