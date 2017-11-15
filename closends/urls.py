from .views import *
from django.conf.urls import url, include

settingpatterns = [
    url(r'index$', person_info.user_info, name='setting_index'),

    # personal info
    url(r'user_info$', person_info.user_info, name='user_info'),
    url(r'user_info/set_head_image$', person_info.set_head_image, name='set_head_image'),
    url(r'user_info/update_username$', person_info.update_username, name='update_username'),

    # weibo binding
    url(r'user_binding$', user_binding.user_binding, name='user_binding'),
    url(r'user_binding/query_weibo_user$', user_binding.query_weibo_user, name='query_weibo_user'),
    url(r'user_binding/weibo_binding$', user_binding.weibo_binding, name='weibo_binding'),
    url(r'user_binding/weibo_unbinding$', user_binding.weibo_unbinding, name='weibo_unbinding'),
    url(r'user_binding/query_bound_weibo_info$', user_binding.query_bound_weibo_info, name='query_bound_weibo_info'),

    # zhihu binding
    url(r'user_binding/query_zhihu_user$', user_binding.query_zhihu_user, name='query_zhihu_user'),
    url(r'user_binding/zhihu_binding$', user_binding.zhihu_binding, name='zhihu_binding'),
    url(r'user_binding/zhihu_unbinding$', user_binding.zhihu_unbinding, name='zhihu_unbinding'),
    url(r'user_binding/query_bound_zhihu_info$', user_binding.query_bound_zhihu_info, name='query_bound_zhihu_info'),

    # group manage
    url(r'friend_manage$', friend_manage.friend_manage, name='friend_manage'),
    url(r'friend_manage/add_group$', friend_manage.add_group, name='add_group'),
    url(r'friend_manage/get_group_friends/(?P<group>\w+)/(?P<page>[0-9]+)$', friend_manage.get_group_friends, name='get_group_friends'),

    # friend manage
    url(r'friend_manage/add_friend$', friend_manage.add_friend, name='add_friend'),
    url(r'friend_manage/delete_friend$', friend_manage.delete_friend, name='delete_friend'),
    url(r'friend_manage/add_friend_info$', friend_manage.add_friend_info, name='add_friend_info'),
    url(r'friend_manage/query_friend_info$', friend_manage.query_friend_info, name='query_friend_info'),
    url(r'friend_manage/update_friend_info$', friend_manage.update_friend_info, name='update_friend_info'),

    # weibo accounts manage
    url(r'friend_manage/delete_friend_weibo$', friend_manage.delete_friend_weibo, name='delete_friend_weibo'),
    url(r'friend_manage/add_found_friend_weibo$', friend_manage.add_found_friend_weibo, name='add_found_friend_weibo'),
    url(r'friend_manage/query_exist_friend_weibo$', friend_manage.query_exist_friend_weibo, name='query_exist_friend_weibo'),

    # zhihu accounts manage
    url(r'friend_manage/delete_friend_zhihu$', friend_manage.delete_friend_zhihu, name='delete_friend_zhihu'),
    url(r'friend_manage/add_found_friend_zhihu$', friend_manage.add_found_friend_zhihu, name='add_found_friend_zhihu'),
    url(r'friend_manage/query_exist_friend_zhihu$', friend_manage.query_exist_friend_zhihu, name='query_exist_friend_zhihu'),
]


app_name = 'closends'
urlpatterns = [
    url(r'^$', login_register.to_login, name='to_login'),
    url(r'^to_register$', login_register.to_register, name='to_register'),
    url(r'^username_login$', login_register.username_login, name='username_lgoin'),
    url(r'^email_login$', login_register.email_login, name='email_lgoin'),
    url(r'^register$', login_register.register, name='register'),
    url(r'^logout$', login_register.user_logout, name='logout'),

    url(r'^index/(?:page-(?P<page>\d+)/)?$', main_page.index, name='index'),
    url(r'^setting/', include(settingpatterns, namespace='setting')),
]
