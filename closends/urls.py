from .views import *
from django.conf.urls import url, include

app_name = 'closends'
urlpatterns = [
    url(r'^$', to_login, name='to_login'),
    url(r'^to_register$', to_register, name='to_register'),
]