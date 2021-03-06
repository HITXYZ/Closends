from .views import *
from django.conf.urls import url, include

setting_patterns = [
    url(r'index$', person_info.user_info, name='setting_index'),

    # personal info
    url(r'user_info$', person_info.user_info, name='user_info'),
    url(r'user_info/set_head_image$', person_info.set_head_image, name='set_head_image'),
    url(r'user_info/update_username$', person_info.update_username, name='update_username'),

    url(r'user_binding$', user_binding.user_binding, name='user_binding'),

    # weibo binding
    url(r'user_binding/query_weibo_user$', user_binding.query_weibo_user, name='query_weibo_user'),
    url(r'user_binding/weibo_binding$', user_binding.weibo_binding, name='weibo_binding'),
    url(r'user_binding/weibo_unbinding$', user_binding.weibo_unbinding, name='weibo_unbinding'),
    url(r'user_binding/query_bound_weibo_info$', user_binding.query_bound_weibo_info, name='query_bound_weibo_info'),

    # zhihu binding
    url(r'user_binding/query_zhihu_user$', user_binding.query_zhihu_user, name='query_zhihu_user'),
    url(r'user_binding/zhihu_binding$', user_binding.zhihu_binding, name='zhihu_binding'),
    url(r'user_binding/zhihu_unbinding$', user_binding.zhihu_unbinding, name='zhihu_unbinding'),
    url(r'user_binding/query_bound_zhihu_info$', user_binding.query_bound_zhihu_info, name='query_bound_zhihu_info'),

    # tieba binding
    url(r'user_binding/query_tieba_user$', user_binding.query_tieba_user, name='query_tieba_user'),
    url(r'user_binding/tieba_binding$', user_binding.tieba_binding, name='tieba_binding'),
    url(r'user_binding/tieba_unbinding$', user_binding.tieba_unbinding, name='tieba_unbinding'),
    url(r'user_binding/query_bound_tieba_info$', user_binding.query_bound_tieba_info, name='query_bound_tieba_info'),

    # group manage
    url(r'friend_manage$', friend_manage.friend_manage, name='friend_manage'),
    url(r'friend_manage/add_group$', friend_manage.add_group, name='add_group'),
    url(r'friend_manage/delete_group$', friend_manage.delete_group, name='delete_group'),
    url(r'friend_manage/get_group_friends/(?:group-(?P<group>\d+))/(?:page-(?P<page>\d+)/)$', friend_manage.get_group_friends, name='get_group_friends'),

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

    # tieba accounts manage
    url(r'friend_manage/delete_friend_tieba$', friend_manage.delete_friend_tieba, name='delete_friend_tieba'),
    url(r'friend_manage/add_found_friend_tieba$', friend_manage.add_found_friend_tieba, name='add_found_friend_tieba'),
    url(r'friend_manage/query_exist_friend_tieba$', friend_manage.query_exist_friend_tieba, name='query_exist_friend_tieba'),

]

content_patterns = [
    url(r'query_all/(?:page-(?P<page>\d+)/)$', main_page.query_all, name='index'),
    url(r'query_by_group/(?:group-(?P<group>\d+))/(?:page-(?P<page>\d+)/)$', main_page.query_by_group, name='query_by_group'),
    url(r'query_by_platform/(?P<platform>\w+)/(?:page-(?P<page>\d+)/)', main_page.query_by_platform, name='query_by_platform'),
    url(r'query_by_topic/(?:topic-(?P<topic>\w+))/(?:page-(?P<page>\d+)/)', main_page.query_by_topic, name='query_by_topic'),
]

app_name = 'closends'
urlpatterns = [
    url(r'^$', login_register.to_login, name='to_login'),
    url(r'^to_register$', login_register.to_register, name='to_register'),
    url(r'^username_login$', login_register.username_login, name='username_lgoin'),
    url(r'^email_login$', login_register.email_login, name='email_lgoin'),
    url(r'^register$', login_register.register, name='register'),
    url(r'^logout$', login_register.user_logout, name='logout'),

    url(r'^index/', include(content_patterns, namespace='content')),
    url(r'^setting/', include(setting_patterns, namespace='setting')),
    url(r'^friend_index/(?P<friend>\w+)/(?:page-(?P<page>\d+)/)$', friend_index.friend_index, name='friend_index'),
]
