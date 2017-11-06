from .views import *
from django.conf.urls import url, include

app_name = 'closends'
urlpatterns = [
    url(r'^$', to_login, name='to_login'),
    url(r'^to_register$', to_register, name='to_register'),

    url(r'^username_login$', username_login, name='username_lgoin'),
    url(r'^email_login$', email_login, name='email_lgoin'),
    url(r'^register$', register, name='register'),

    url(r'^index$', index, name="index"),
]