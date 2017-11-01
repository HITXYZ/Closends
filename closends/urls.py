from .views import *
from django.conf.urls import url, include

app_name = 'closends'
urlpatterns = [
    url(r'^$', index, name='index'),
]