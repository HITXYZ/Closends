from .views import *
from django.conf.urls import url, include

settingpatterns = [
    url(r'user_info$', user_info, name='user_info'),
    url(r'user_binding$', user_binding, name='user_binding'),
    url(r'friend_manage$', friend_manage, name='friend_manage'),
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